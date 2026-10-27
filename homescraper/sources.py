from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class SourceRecord:
    source_name: str
    jurisdiction: str
    url: str
    access_method: str
    update_frequency: str | None
    terms_url: str | None
    robots_policy: str | None
    api_available: bool
    cost: str | None
    reliability: float | None
    legal_confidence: float | None


class SourceAdapter:
    """Contract for an authorized source adapter.

    Implementations must document access terms and must not bypass technical
    access controls, authentication, CAPTCHA, paywalls, or rate limits.
    """

    source: SourceRecord

    def fetch(self) -> Iterable[dict]:
        raise NotImplementedError

    def normalize(self, record: dict) -> dict:
        return record

    def validate(self, record: dict) -> list[str]:
        return []


class UnconfiguredSourceAdapter(SourceAdapter):
    def __init__(self, source: SourceRecord):
        self.source = source

    def fetch(self) -> Iterable[dict]:
        raise RuntimeError(
            f"Source adapter '{self.source.source_name}' is not configured. "
            "No live source is assumed or fabricated."
        )
