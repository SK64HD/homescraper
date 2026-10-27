-- PostgreSQL-oriented MVP schema. Live ingestion is intentionally absent until
-- an authorized source and county are selected and documented.

CREATE TABLE properties (
  id BIGSERIAL PRIMARY KEY,
  property_id TEXT UNIQUE NOT NULL,
  parcel_id TEXT,
  address TEXT NOT NULL,
  municipality TEXT,
  county TEXT NOT NULL,
  zip_code TEXT,
  latitude NUMERIC(9,6),
  longitude NUMERIC(9,6),
  property_type TEXT,
  year_built INTEGER,
  bedrooms INTEGER,
  bathrooms NUMERIC(4,1),
  square_feet INTEGER,
  lot_size NUMERIC,
  owner_name TEXT,
  mailing_address TEXT,
  assessed_value NUMERIC(14,2),
  tax_amount NUMERIC(14,2),
  last_sale_price NUMERIC(14,2),
  last_sale_date DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE sources (
  id BIGSERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  jurisdiction TEXT NOT NULL,
  url TEXT NOT NULL,
  access_method TEXT NOT NULL,
  update_frequency TEXT,
  terms_url TEXT,
  robots_policy TEXT,
  api_available BOOLEAN,
  cost TEXT,
  reliability NUMERIC(5,4),
  legal_confidence NUMERIC(5,4),
  checked_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE source_records (
  id BIGSERIAL PRIMARY KEY,
  source_id BIGINT NOT NULL REFERENCES sources(id),
  property_id BIGINT REFERENCES properties(id),
  external_record_id TEXT,
  retrieved_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  original_value JSONB NOT NULL,
  normalized_value JSONB,
  confidence NUMERIC(5,4),
  UNIQUE(source_id, external_record_id)
);

CREATE TABLE distress_events (
  id BIGSERIAL PRIMARY KEY,
  property_id BIGINT NOT NULL REFERENCES properties(id),
  event_type TEXT NOT NULL,
  observed_on DATE,
  source_record_id BIGINT REFERENCES source_records(id),
  confidence NUMERIC(5,4),
  details JSONB NOT NULL DEFAULT '{}'
);

CREATE TABLE valuations (
  id BIGSERIAL PRIMARY KEY,
  property_id BIGINT NOT NULL REFERENCES properties(id),
  method TEXT NOT NULL,
  low NUMERIC(14,2),
  central NUMERIC(14,2),
  high NUMERIC(14,2),
  confidence NUMERIC(5,4),
  source_record_ids BIGINT[] NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE deal_analyses (
  id BIGSERIAL PRIMARY KEY,
  property_id BIGINT NOT NULL REFERENCES properties(id),
  strategy TEXT NOT NULL,
  assumptions JSONB NOT NULL,
  projected_profit NUMERIC(14,2),
  maximum_acquisition NUMERIC(14,2),
  risks JSONB NOT NULL DEFAULT '[]',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE deal_scores (
  id BIGSERIAL PRIMARY KEY,
  property_id BIGINT NOT NULL REFERENCES properties(id),
  score INTEGER NOT NULL CHECK (score BETWEEN 0 AND 100),
  factors JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE approvals (
  id BIGSERIAL PRIMARY KEY,
  action TEXT NOT NULL,
  property_id BIGINT REFERENCES properties(id),
  state TEXT NOT NULL CHECK (state IN ('draft','pending','approved','rejected')),
  reviewer TEXT,
  reason TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  decided_at TIMESTAMPTZ
);

CREATE TABLE audit_logs (
  id BIGSERIAL PRIMARY KEY,
  actor TEXT,
  action TEXT NOT NULL,
  property_id BIGINT REFERENCES properties(id),
  source TEXT,
  previous_value JSONB,
  new_value JSONB,
  automated BOOLEAN NOT NULL DEFAULT false,
  reason TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX properties_county_idx ON properties(county);
CREATE INDEX properties_parcel_idx ON properties(parcel_id);
CREATE INDEX source_records_property_idx ON source_records(property_id);
CREATE INDEX distress_events_property_idx ON distress_events(property_id);
