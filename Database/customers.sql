-- Table: eudr.customers

-- DROP TABLE IF EXISTS eudr.customers;

CREATE TABLE IF NOT EXISTS eudr.customers
(
    customer_id integer NOT NULL DEFAULT nextval('eudr.customers_customer_id_seq'::regclass),
    customer_name character varying,
    customer_address character varying,
    region character varying,
    import_country character varying,
    zip character varying,
    commodity character varying,
    year_of_trade integer,
    risk_score float,
    last_updated timestamp without time zone DEFAULT now(),
    CONSTRAINT customers_pkey PRIMARY KEY (customer_id)
);