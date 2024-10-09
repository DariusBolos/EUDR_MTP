-- Table: eudr.commodities

-- DROP TABLE IF EXISTS eudr.commodities;

CREATE TABLE IF NOT EXISTS eudr.commodities
(
    commodity_id integer NOT NULL DEFAULT nextval('eudr.commodities_commodity_id_seq'::regclass),
    commodity_name character varying,
    last_updated timestamp without time zone DEFAULT now(),
    CONSTRAINT commodities_pkey PRIMARY KEY (commodity_id)
);

INSERT INTO eudr.commodities
(
    commodity_name
)
VALUES
('Cattle'),
('Soy'),
('Palm Oil'),
('Wood'),
('Coffee'),
('Cocoa'),
('Natural Rubber');