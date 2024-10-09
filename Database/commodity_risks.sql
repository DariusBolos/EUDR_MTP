-- Table: eudr.commodity_risks

-- DROP TABLE IF EXISTS eudr.commodity_risks;

CREATE TABLE IF NOT EXISTS eudr.commodity_risks
(
    commodity_id integer NOT NULL,
    risk_source_id integer NOT NULL,
    risk_category_id integer NOT NULL,
    year integer NOT NULL,
    country_code character varying,
    region character varying,
    risk_score float,
    description character varying,
    last_updated timestamp without time zone DEFAULT now(),
    UNIQUE(commodity_id, risk_source_id, risk_category_id, year, country_code, region)
);
