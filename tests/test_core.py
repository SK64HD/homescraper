from decimal import Decimal

from homescraper.core import (
    DistressSignals,
    distress_score,
    flip_profit,
    motivation_score,
    no_deal_reasons,
    wholesale_mao,
)


def test_distress_score_is_explainable_and_bounded():
    score = distress_score(DistressSignals(tax_delinquency=True, foreclosure=True))
    assert score == 35
    assert 0 <= score <= 100


def test_wholesale_mao():
    assert wholesale_mao(
        Decimal("300000"), Decimal("50000"), Decimal("5000"),
        Decimal("10000"), Decimal("60000"), Decimal("5000")
    ) == Decimal("170000")


def test_flip_profit():
    assert flip_profit(
        Decimal("300000"), Decimal("170000"), Decimal("50000"),
        Decimal("5000"), Decimal("10000"), Decimal("5000"),
        Decimal("18000"), Decimal("7000")
    ) == Decimal("35000")


def test_motivation_does_not_claim_unverified_personal_circumstances():
    result = motivation_score(
        distress=20,
        equity=None,
        ownership_years=None,
        absentee=True,
        vacancy=False,
        failed_listing=False,
    )
    assert result.score > 0
    assert "equity estimate" in result.missing_information
    assert "ownership duration" in result.missing_information


def test_no_deal_engine_flags_low_confidence():
    reasons = no_deal_reasons(
        spread=Decimal("10000"),
        arv_confidence=0.4,
        buyer_demand=0.8,
        title_clear=None,
        legal_risk=0.1,
        data_quality=0.8,
    )
    assert "unreliable ARV" in reasons
