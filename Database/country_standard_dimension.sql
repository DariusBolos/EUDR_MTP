-- Table: eudr.standard_country_dimension

-- DROP TABLE IF EXISTS eudr.standard_country_dimension;

CREATE TABLE IF NOT EXISTS eudr.standard_country_dimension
(
    standard_country_name varchar,
    country_code character varying NOT NULL,
    last_updated timestamp without time zone DEFAULT now(),
    CONSTRAINT standard_country_dimension_pkey PRIMARY KEY (country_code)
);

-- insertions happen through dimension_upserts.py