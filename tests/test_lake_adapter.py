from __future__ import annotations

from datetime import date
from unittest.mock import patch

from homescraper.counties.lake import lake_county_adapter


SAMPLE = {
    "features": [
        {
            "attributes": {
                "PIN": "0821410004",
                "situs_addr_line_1": "18 N COUNTY ST",
                "situs_addr_line_2": None,
                "situs_addr_line_3": None,
                "situs_addr_city": "WAUKEGAN",
                "situs_addr_zip_legdat": "60085",
                "taxpayer_name": "EXAMPLE OWNER",
                "taxpayer_addr_line_1": "1 MAIN ST",
                "taxpayer_addr_line_2": None,
                "taxpayer_addr_line_3": None,
                "assess_total_assyr": 123456,
                "MUNI_NAME": "WAUKEGAN",
            }
        }
    ],
    "exceededTransferLimit": False,
}


def test_lake_adapter_normalizes_a_record_without_network() -> None:
    adapter = lake_county_adapter()
    with patch.object(adapter, "_request", return_value=SAMPLE):
        records = list(adapter.fetch())

    assert len(records) == 1
    prop = adapter.to_property(records[0], retrieved_on=date(2026, 10, 27))
    assert prop.property_id == "il-lake-0821410004"
    assert prop.parcel_id == "0821410004"
    assert prop.address == "18 N COUNTY ST"
    assert prop.municipality == "WAUKEGAN"
    assert str(prop.assessed_value) == "123456"
    assert prop.fields["owner_name"].provenance.original_value


def test_lake_adapter_paginates_when_arcgis_sets_transfer_limit() -> None:
    adapter = lake_county_adapter()
    first = {"features": [{"attributes": {"PIN": "1"}}], "exceededTransferLimit": True}
    second = {"features": [{"attributes": {"PIN": "2"}}], "exceededTransferLimit": False}

    with patch.object(adapter, "_request", side_effect=[first, second]) as request:
        records = list(adapter.fetch())

    assert [record["PIN"] for record in records] == ["1", "2"]
    assert request.call_count == 2
    assert request.call_args_list[1].args[0]["resultOffset"] == 1
