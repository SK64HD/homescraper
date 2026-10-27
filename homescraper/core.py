from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Literal


@dataclass(frozen=True)
class Provenance:
    source: str
    source_url: str | None
    retrieved_on: date
    confidence: float
    original_value: str

    def __post_init__(self) -> None:
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class FieldValue:
    value: object
    provenance: Provenance


@dataclass
class Property:
    property_id: str
    address: str
    county: str
    municipality: str | None = None
    zip_code: str | None = None
    parcel_id: str | None = None
    property_type: str | None = None
    square_feet: int | None = None
    bedrooms: int | None = None
    bathrooms: float | None = None
    year_built: int | None = None
    assessed_value: Decimal | None = None
    tax_amount: Decimal | None = None
    last_sale_price: Decimal | None = None
    last_sale_date: date | None = None
    fields: dict[str, FieldValue] = field(default_factory=dict)


@dataclass(frozen=True)
class DistressSignals:
    tax_delinquency: bool = False
    long_term_ownership: bool = False
    absentee_owner: bool = False
    out_of_state_owner: bool = False
    code_violations: bool = False
    vacancy: bool = False
    foreclosure: bool = False
    probate: bool = False
    failed_listing: bool = False
    large_price_reduction: bool = False
    high_equity: bool = False


DEFAULT_DISTRESS_WEIGHTS: dict[str, int] = {
    "tax_delinquency": 15,
    "long_term_ownership": 5,
    "absentee_owner": 8,
    "out_of_state_owner": 7,
    "code_violations": 12,
    "vacancy": 15,
    "foreclosure": 20,
    "probate": 10,
    "failed_listing": 7,
    "large_price_reduction": 8,
    "high_equity": 10,
}


def distress_score(signals: DistressSignals, weights: dict[str, int] | None = None) -> int:
    weights = weights or DEFAULT_DISTRESS_WEIGHTS
    return min(100, sum(weight for name, weight in weights.items() if getattr(signals, name, False)))


@dataclass(frozen=True)
class MotivationResult:
    score: float
    reasons: tuple[str, ...]
    confidence: float
    missing_information: tuple[str, ...]


def motivation_score(
    *,
    distress: int,
    equity: float | None,
    ownership_years: float | None,
    absentee: bool,
    vacancy: bool,
    failed_listing: bool,
) -> MotivationResult:
    score = 0.0
    reasons: list[str] = []
    missing: list[str] = []

    score += min(35, distress * 0.35)
    if distress:
        reasons.append("documented distress signals")
    else:
        missing.append("distress evidence")

    if equity is None:
        missing.append("equity estimate")
    else:
        score += min(25, max(0, equity) * 25)
        if equity >= 0.5:
            reasons.append("estimated equity")

    if ownership_years is None:
        missing.append("ownership duration")
    elif ownership_years >= 10:
        score += 10
        reasons.append("long ownership duration")
    elif ownership_years >= 5:
        score += 5

    if absentee:
        score += 10
        reasons.append("absentee ownership")
    if vacancy:
        score += 10
        reasons.append("vacancy signal")
    if failed_listing:
        score += 10
        reasons.append("failed listing signal")

    known = 1.0 - min(1.0, len(missing) / 3)
    return MotivationResult(round(min(100, score), 2), tuple(reasons), round(known, 2), tuple(missing))


@dataclass(frozen=True)
class ValuationRange:
    low: Decimal
    central: Decimal
    high: Decimal
    confidence: float


@dataclass(frozen=True)
class RehabRange:
    low: Decimal
    central: Decimal
    high: Decimal


@dataclass(frozen=True)
class DealAnalysis:
    strategy: Literal["wholesale", "flip", "hold", "pass"]
    acquisition: Decimal
    projected_profit: Decimal | None
    max_acquisition: Decimal | None
    rationale: tuple[str, ...]
    risks: tuple[str, ...]


def wholesale_mao(
    arv: Decimal,
    rehab: Decimal,
    transaction_costs: Decimal,
    holding_costs: Decimal,
    buyer_profit: Decimal,
    disposition_costs: Decimal,
) -> Decimal:
    return arv - rehab - transaction_costs - holding_costs - buyer_profit - disposition_costs


def flip_profit(
    arv: Decimal,
    acquisition: Decimal,
    rehab: Decimal,
    financing: Decimal,
    holding: Decimal,
    closing: Decimal,
    selling: Decimal,
    contingency: Decimal,
) -> Decimal:
    return arv - acquisition - rehab - financing - holding - closing - selling - contingency


def deal_score(
    *,
    discount: float,
    equity: float,
    distress: float,
    motivation: float,
    arv_confidence: float,
    rehab_confidence: float,
    buyer_demand: float,
    liquidity: float,
    legal_risk: float,
    data_quality: float,
    competition: float,
    exit_options: float,
) -> int:
    positive = (
        discount + equity + distress + motivation + arv_confidence + rehab_confidence
        + buyer_demand + liquidity + data_quality + exit_options
    ) / 10
    risk_penalty = (legal_risk + competition) / 2
    return round(max(0, min(100, positive - risk_penalty)))


def no_deal_reasons(
    *,
    spread: Decimal | None,
    arv_confidence: float,
    buyer_demand: float,
    title_clear: bool | None,
    legal_risk: float,
    data_quality: float,
) -> list[str]:
    reasons: list[str] = []
    if spread is not None and spread <= 0:
        reasons.append("insufficient spread")
    if arv_confidence < 0.5:
        reasons.append("unreliable ARV")
    if buyer_demand < 0.3:
        reasons.append("low buyer demand")
    if title_clear is False:
        reasons.append("title requires resolution")
    if legal_risk >= 0.7:
        reasons.append("material legal risk")
    if data_quality < 0.5:
        reasons.append("insufficient data confidence")
    return reasons


ApprovalState = Literal["draft", "pending", "approved", "rejected"]


@dataclass(frozen=True)
class Approval:
    action: str
    state: ApprovalState = "pending"
    reviewer: str | None = None
    reason: str | None = None

    @property
    def can_execute(self) -> bool:
        return self.state == "approved"
