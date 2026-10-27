from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass(frozen=True)
class PropertyIdentity:
    """Deterministic identity candidates; no fuzzy match is accepted automatically."""

    canonical_property_id: str
    parcel_key: str | None
    address_key: str
    owner_key: str | None


@dataclass(frozen=True)
class MatchCandidate:
    candidate_id: str
    score: float
    reasons: tuple[str, ...]


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.upper().strip()
    return re.sub(r"[^A-Z0-9]+", " ", value).strip()


def normalize_parcel(value: str | None) -> str | None:
    normalized = normalize_text(value)
    return normalized or None


def normalize_address(value: str | None) -> str:
    normalized = normalize_text(value)
    replacements = {
        "STREET": "ST",
        "AVENUE": "AVE",
        "ROAD": "RD",
        "DRIVE": "DR",
        "LANE": "LN",
        "COURT": "CT",
        "BOULEVARD": "BLVD",
        "HIGHWAY": "HWY",
        "PARKWAY": "PKWY",
        "PLACE": "PL",
        "CIRCLE": "CIR",
        "NORTH": "N",
        "SOUTH": "S",
        "EAST": "E",
        "WEST": "W",
    }
    tokens = [replacements.get(token, token) for token in normalized.split()]
    return " ".join(tokens)


def canonical_identity(
    property_id: str,
    address: str,
    parcel_id: str | None = None,
    owner_name: str | None = None,
) -> PropertyIdentity:
    parcel_key = normalize_parcel(parcel_id)
    address_key = normalize_address(address)
    owner_key = normalize_text(owner_name) or None
    canonical = f"property:{property_id}" if property_id else f"address:{address_key}"
    return PropertyIdentity(canonical, parcel_key, address_key, owner_key)


def candidate_score(left: PropertyIdentity, right: PropertyIdentity) -> MatchCandidate:
    reasons: list[str] = []
    score = 0.0
    if left.parcel_key and right.parcel_key and left.parcel_key == right.parcel_key:
        score += 0.75
        reasons.append("parcel_exact")
    if left.address_key and right.address_key and left.address_key == right.address_key:
        score += 0.20
        reasons.append("address_exact")
    elif left.address_key and right.address_key:
        similarity = SequenceMatcher(None, left.address_key, right.address_key).ratio()
        if similarity >= 0.92:
            score += 0.10
            reasons.append("address_near")
    if left.owner_key and right.owner_key and left.owner_key == right.owner_key:
        score += 0.05
        reasons.append("owner_exact")
    return MatchCandidate(right.canonical_property_id, min(score, 1.0), tuple(reasons))


def is_safe_auto_match(candidate: MatchCandidate) -> bool:
    """Only an exact parcel match is safe for automatic entity merging."""
    return "parcel_exact" in candidate.reasons
