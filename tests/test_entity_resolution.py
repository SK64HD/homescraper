from homescraper.entity_resolution import (
    candidate_score,
    canonical_identity,
    is_safe_auto_match,
    normalize_address,
    normalize_parcel,
)


def test_address_normalization_is_deterministic():
    assert normalize_address("123 Main Street, Apt 2") == "123 MAIN ST APT 2"


def test_parcel_normalization_removes_formatting_noise():
    assert normalize_parcel("08-17-304-014") == "08 17 304 014"


def test_exact_parcel_is_safe_auto_match():
    left = canonical_identity("il-lake-0817304014", "123 Main St", "08-17-304-014", "Jane Doe")
    right = canonical_identity("external-1", "123 MAIN STREET", "08 17 304 014", "JANE DOE")
    candidate = candidate_score(left, right)
    assert candidate.score == 1.0
    assert is_safe_auto_match(candidate)


def test_address_only_match_requires_review():
    left = canonical_identity("a", "123 Main St", None, "Jane Doe")
    right = canonical_identity("b", "123 Main Street", None, "Jane Doe")
    candidate = candidate_score(left, right)
    assert candidate.score > 0
    assert not is_safe_auto_match(candidate)
