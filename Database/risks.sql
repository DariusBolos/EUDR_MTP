-- Table: eudr.risks

-- DROP TABLE IF EXISTS eudr.risks;

CREATE TABLE IF NOT EXISTS eudr.risks
(
    risk_source_id integer NOT NULL,
    risk_category_id integer NOT NULL,
    year integer NOT NULL,
    country_code character varying NOT NULL,
    risk_score float,
    description character varying(2000),
    last_updated timestamp without time zone DEFAULT now(),
    CONSTRAINT risks_pkey PRIMARY KEY (risk_source_id, risk_category_id, year, country_code)
);