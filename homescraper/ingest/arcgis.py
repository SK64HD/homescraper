from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

from .core import FieldValue, Property, Provenance
from .sources import SourceAdapter, SourceRecord


@dataclass(frozen=True)
class ArcGISQueryConfig:
    layer_url: str
    out_fields: tuple[str, ...]
    where: str = "1=1"
    page_size: int = 1000
    timeout_seconds: int = 30


class ArcGISFeatureLayerAdapter(SourceAdapter):
    """Read-only adapter for an ArcGIS Feature/MapServer query endpoint.

    This adapter only performs normal public HTTP GET requests. It does not
    bypass authentication, CAPTCHA, paywalls, bot controls, or rate limits.
    """

    def __init__(self, source: SourceRecord, config: ArcGISQueryConfig):
        self.source = source
        self.config = config
        if not source.api_available:
            raise ValueError("Source must explicitly declare API availability")

    def _request(self, params: dict[str, Any]) -> dict[str, Any]:
        query = urlencode(params)
        request = Request(
            f"{self.config.layer_url}/query?{query}",
            headers={"User-Agent": "homescraper/0.1 (authorized public-data client)"},
        )
        with urlopen(request, timeout=self.config.timeout_seconds) as response:
            payload = json.load(response)
        if "error" in payload:
            raise RuntimeError(f"ArcGIS query failed: {payload['error']}")
        return payload

    def fetch(self) -> Iterable[dict[str, Any]]:
        offset = 0
        fields = ",".join(self.config.out_fields)
        while True:
            payload = self._request(
                {
                    "where": self.config.where,
                    "outFields": fields,
                    "returnGeometry": "false",
                    "resultOffset": offset,
                    "resultRecordCount": self.config.page_size,
                    "f": "json",
                }
            )
            features = payload.get("features", [])
            for feature in features:
                yield feature.get("attributes", {})
            if not payload.get("exceededTransferLimit") or not features:
                break
            offset += len(features)

    def normalize(self, record: dict[str, Any]) -> dict[str, Any]:
        return {key: value.strip() if isinstance(value, str) else value for key, value in record.items()}

    def to_property(self, record: dict[str, Any], retrieved_on: date | None = None) -> Property:
        row = self.normalize(record)
        retrieved = retrieved_on or date.today()
        pin = _text(row.get("PIN"))
        if not pin:
            raise ValueError("Lake County record is missing PIN")
        address = " ".join(
            part for part in (
                _text(row.get("situs_addr_line_1")),
                _text(row.get("situs_addr_line_2")),
                _text(row.get("situs_addr_line_3")),
            ) if part
        )
        city = _text(row.get("situs_addr_city"))
        zip_code = _text(row.get("situs_addr_zip_legdat"))
        owner = _text(row.get("taxpayer_name"))
        mailing = " ".join(
            part for part in (
                _text(row.get("taxpayer_addr_line_1")),
                _text(row.get("taxpayer_addr_line_2")),
                _text(row.get("taxpayer_addr_line_3")),
            ) if part
        )
        provenance = Provenance(
            source=self.source.source_name,
            source_url=self.source.url,
            retrieved_on=retrieved,
            confidence=1.0,
            original_value=json.dumps(row, default=str, sort_keys=True),
        )
        fields = {
            "parcel_id": FieldValue(pin, provenance),
            "owner_name": FieldValue(owner, provenance),
        }
        return Property(
            property_id=f"il-lake-{pin}",
            address=address,
            county="Lake",
            municipality=_text(row.get("MUNI_NAME")),
            zip_code=zip_code,
            parcel_id=pin,
            assessed_value=_decimal(row.get("assess_total_assyr")),
            fields=fields,
        )


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _decimal(value: Any) -> Decimal | None:
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _date_from_arcgis(value: Any) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000).date()
    return date.fromisoformat(str(value)[:10])
