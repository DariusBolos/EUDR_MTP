-- Table: eudr.risk_categories

-- DROP TABLE IF EXISTS eudr.risk_categories;

CREATE TABLE IF NOT EXISTS eudr.risk_categories
(
    category_id integer NOT NULL DEFAULT nextval('eudr.risk_categories_category_id_seq'::regclass),
    category_name character varying COLLATE pg_catalog."default",
    last_updated timestamp without time zone DEFAULT now(),
    weight integer,
    CONSTRAINT risk_categories_pkey PRIMARY KEY (category_id)
);

-- insert categories
INSERT INTO eudr.risk_categories
(category_name)
VALUES 
('corruption'),--1
('employee_rights'),--2
('land_use_rights'),--3
('environmental_protection'),--4
('human_rights'),--5
('deforestation_free'),--6
('forest_degradation'),--7
('indigenous_people'),--8
('forest_related_regulations'),--9
('trade_customs_regulations'),--10
('third_party_rights')--11
;