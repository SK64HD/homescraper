# homescraper

Real-estate acquisition research and underwriting platform for Northern Illinois.

This repository is intentionally source-first: the system must not invent property facts, comps, seller circumstances, valuations, or legal conclusions. Data fields carry provenance and confidence, and consequential actions require human approval.

## Current implementation

- Deterministic property, distress, motivation, valuation, rehab, deal-score, and approval domain models.
- Provenance-aware data structures.
- Configurable wholesale / flip / buy-and-hold analysis.
- No-deal checks and explainable scoring.
- Authorized-source adapter interface; no access-control bypassing or implicit scraping.
- SQL schema targeting PostgreSQL.
- Compliance research record for Illinois based on current primary sources checked during implementation.
- SEO metadata helpers that only emit facts supplied by the caller.
- Tests for core deterministic calculations.

## MVP status

The repository was initially empty except for this README. The first implementation therefore establishes the architecture and deterministic core rather than pretending a county adapter, comps feed, or live property dataset already exists.

The first county and first live public data adapter remain research decisions. They are not fabricated here.

## Run

```bash
python -m pytest
python -m homescraper.api
```

The API is intentionally small until a real source adapter and database connection are selected.

## Principles

1. Source data before assertions.
2. Every important property value has provenance.
3. Estimates are labeled as estimates.
4. Never manufacture comparable sales.
5. Never infer personal financial hardship without evidence.
6. Do not bypass CAPTCHA, authentication, paywalls, bot protection, or rate limits.
7. Human approval is required for legally or financially consequential actions.
8. SEO pages must be useful and traceable, not mass-generated filler.
9. Do not commit secrets.

## Legal note

This software is an analysis and workflow system, not legal advice, brokerage authorization, an appraisal, or a guarantee of investment returns. Current compliance notes live in `docs/compliance/illinois.md` and must be re-checked before consequential activity.
