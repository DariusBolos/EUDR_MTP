-- The PublicEye website content is restricetd to be retrieved by Python
-- Hence, the risk scores are manually inserted in the database
-- The risk scores are retrieved using ChatGPT.

-- Employee Rights
/*
PROMPT
There are 7 commodities- Cattle, Soy, Palm Oil, Wood, Coffee, Cocoa, Natural Rubber.
Provide risk score between 1 and 6 related to labour rights. High score is more risk. Risk score should be related to the commodity mentioned in the list. Output should contain the country name, 2 character ISO country code, commodity for which the score is calculated and the risk score value, 30 word description of the risk score why this value was mentioned.
https://www.publiceye.ch/en/topics/soft-commodity-trading/most-severe-issues-related-to-agricultural-production-and-trade/human-and-labour-rights-violations
*/

insert into eudr.commodity_risks
(
    commodity_id, risk_source_id, risk_category_id, year, country_code, risk_score, description
)
values 
(
   6, 18, 2, 2023, 'CI', 6.0, 'In Côte d''Ivoire, cocoa production is plagued by severe labor rights issues, including widespread child labor and poverty wages, with most workers earning less than $1.90 per day.'
);

insert into eudr.commodity_risks
(
    commodity_id, risk_source_id, risk_category_id, year, country_code, risk_score, description
)
values 
(
   6, 18, 2, 2023, 'GH', 5.0, 'In Ghana, cocoa farming faces labor rights challenges such as child labor and inadequate wages, though efforts to improve conditions are ongoing, reducing the risk slightly compared to Côte d''Ivoire.'
);


-- Deforestation and Forest Degradation
/*
PROMPT
There are 7 commodities- Cattle, Soy, Palm Oil, Wood, Coffee, Cocoa, Natural Rubber.
Provide risk score between 1 and 6 related to deforestation and forest degradation. High score is more risk. Risk score should be related to the commodity mentioned in the list. Output should contain the country name, 2 character ISO country code, commodity for which the score is calculated and the risk score value, 30 word description of the risk score why this value was mentioned.
https://www.publiceye.ch/en/topics/soft-commodity-trading/most-severe-issues-related-to-agricultural-production-and-trade/deforestation-and-land-grabbing
*/

insert into eudr.commodity_risks
(
    commodity_id, risk_source_id, risk_category_id, year, country_code, risk_score, description
)
values 
(
    2, 19, 7, 2023, 'BR', 6.0, 'Soy cultivation in Brazil, particularly in the Amazon and Cerrado, drives massive deforestation due to expanding farmland needs.'
);

insert into eudr.commodity_risks
(
    commodity_id, risk_source_id, risk_category_id, year, country_code, risk_score, description
)
values 
(
    3, 19, 7, 2023, 'ID', 6.0, 'Palm oil plantations lead to extensive deforestation in Indonesia, threatening biodiversity and contributing significantly to carbon emissions.'
);

insert into eudr.commodity_risks
(
    commodity_id, risk_source_id, risk_category_id, year, country_code, risk_score, description
)
values 
(
    3, 19, 7, 2023, 'MY', 5.0, 'Palm oil expansion in Malaysia leads to forest degradation, impacting ecosystems and indigenous communities.'
);

insert into eudr.commodity_risks
(
    commodity_id, risk_source_id, risk_category_id, year, country_code, risk_score, description
)
values 
(
    5, 19, 7, 2023, 'CI', 5.0, 'Côte d''Ivoire''s cocoa production results in significant forest loss, with illegal farming in protected areas worsening the impact.'
);

insert into eudr.commodity_risks
(
    commodity_id, risk_source_id, risk_category_id, year, country_code, risk_score, description
)
values 
(
    6, 19, 7, 2023, 'GH', 5.0, 'Cocoa farming in Ghana causes deforestation, particularly in protected areas, due to the clearing of forests for new plantations.'
);

-- Corruption
/*
PROMPT
Provide risk score between 1 and 6 related to corruption. High score is more risk. Risk score should be related to the commodity mentioned in the list. Output should contain the country name, 2 character ISO country code, risk score value, 30 word description of the risk score why this value was mentioned.
https://www.publiceye.ch/en/topics/soft-commodity-trading/most-severe-issues-related-to-agricultural-production-and-trade/tax-dodging-and-corruption
*/

insert into eudr.risks
(
    risk_source_id, risk_category_id, year, country_code, risk_score, description
)
values 
(
    20, 1, 2023, 'AR', 6.0, 'In Argentina, corruption risks are high, as seen in the grain trading sector, where allegations of tax fraud and mispricing persist among major companies.'
);

insert into eudr.risks
(
    risk_source_id, risk_category_id, year, country_code, risk_score, description
)
values 
(
    20, 1, 2023, 'BR', 6.0, 'Political connections between agricultural companies and the elite, such as the Maggi family, heighten corruption risks in Brazil''s soy industry due to conflicts of interest.'
);

insert into eudr.risks
(
    risk_source_id, risk_category_id, year, country_code, risk_score, description
)
values 
(
    20, 1, 2023, 'CO', 6.0, 'Corruption is severe in Colombia, exemplified by Chiquita''s payments to paramilitary groups, reflecting deep entanglement between business and unlawful activities.'
);

-- Land Grabbing
/*
PROMPT
There are 7 commodities- Cattle, Soy, Palm Oil, Wood, Coffee, Cocoa, Natural Rubber.
Provide risk score between 1 and 6 related to land grabbing. High score is more risk. Risk score should be related to the commodity mentioned in the list. Output should contain the country name, 2 character ISO country code, commodity for which the score is calculated and the risk score value, 30 word description of the risk score why this value was mentioned.
https://www.publiceye.ch/en/topics/soft-commodity-trading/most-severe-issues-related-to-agricultural-production-and-trade/deforestation-and-land-grabbing
*/

insert into eudr.commodity_risks
(
    commodity_id, risk_source_id, risk_category_id, year, country_code, risk_score, description
)
values 
(
    5, 21, 7, 2023, 'UG', 6.0, 'Land grabbing in Uganda often involves coffee production, with cases like the Kaweri plantation, where communities were forcibly evicted to make way for large-scale coffee farming.'
);