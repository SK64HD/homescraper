from __future__ import annotations

from decimal import Decimal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from homescraper.core import (
    DistressSignals,
    deal_score,
    distress_score,
    no_deal_reasons,
    wholesale_mao,
)

app = FastAPI(title="homescraper", version="0.1.0")


class DistressRequest(BaseModel):
    signals: DistressSignals


class DealScoreRequest(BaseModel):
    discount: float = Field(ge=0, le=100)
    equity: float = Field(ge=0, le=100)
    distress: float = Field(ge=0, le=100)
    motivation: float = Field(ge=0, le=100)
    arv_confidence: float = Field(ge=0, le=100)
    rehab_confidence: float = Field(ge=0, le=100)
    buyer_demand: float = Field(ge=0, le=100)
    liquidity: float = Field(ge=0, le=100)
    legal_risk: float = Field(ge=0, le=100)
    data_quality: float = Field(ge=0, le=100)
    competition: float = Field(ge=0, le=100)
    exit_options: float = Field(ge=0, le=100)


class WholesaleRequest(BaseModel):
    arv: Decimal
    rehab: Decimal
    transaction_costs: Decimal
    holding_costs: Decimal
    buyer_profit: Decimal
    disposition_costs: Decimal


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analysis/distress")
def analyze_distress(request: DistressRequest) -> dict[str, int]:
    return {"score": distress_score(request.signals)}


@app.post("/analysis/deal-score")
def analyze_deal_score(request: DealScoreRequest) -> dict[str, int]:
    values = request.model_dump()
    return {"score": deal_score(**values)}


@app.post("/analysis/wholesale-mao")
def analyze_wholesale(request: WholesaleRequest) -> dict[str, str]:
    mao = wholesale_mao(**request.model_dump())
    return {"maximum_acquisition": str(mao)}


@app.post("/analysis/no-deal")
def analyze_no_deal(
    spread: Decimal | None = None,
    arv_confidence: float = 0,
    buyer_demand: float = 0,
    title_clear: bool | None = None,
    legal_risk: float = 0,
    data_quality: float = 0,
) -> dict[str, object]:
    reasons = no_deal_reasons(
        spread=spread,
        arv_confidence=arv_confidence,
        buyer_demand=buyer_demand,
        title_clear=title_clear,
        legal_risk=legal_risk,
        data_quality=data_quality,
    )
    return {"pass": bool(reasons), "reasons": reasons}
