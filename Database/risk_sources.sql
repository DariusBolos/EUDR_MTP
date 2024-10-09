-- Table: eudr.risk_sources

-- DROP TABLE IF EXISTS eudr.risk_sources;

CREATE TABLE IF NOT EXISTS eudr.risk_sources
(
    source_id integer NOT NULL DEFAULT nextval('eudr.risk_sources_source_id_seq'::regclass),
    source_name character varying,
    category_id integer,
    category_name character varying,
    url character varying(1000),
    description character varying(65535),
    last_updated timestamp without time zone DEFAULT now(),
    confidence_percentage integer,
    CONSTRAINT risk_sources_pkey PRIMARY KEY (source_id)
);

-- insert for corruption
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'transparency.org corruption perception index',
    'https://www.transparency.org/en/cpi/2023',
    'Transparency International''s website serves as a central platform for promoting integrity, accountability, and transparency worldwide. It provides access to research reports, policy briefs, corruption indices, and advocacy campaigns, empowering individuals and organizations to combat corruption in all its forms.',
    100
);

-- insert for employee_rights
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'globalrightsindex employee rights',
    'https://www.globalrightsindex.org/en/2023',
    'This website, located at https://www.globalrightsindex.org/en/2023, serves as a comprehensive platform presenting the Global Rights Index for the year 2023. Through meticulously compiled data and analysis, it offers a detailed overview of the status of workers'' rights globally. Users can access valuable insights, ranging from the prevalence of violations to trends in labor standards adherence across various industries and regions. With its user-friendly interface and up-to-date information, this website serves as an indispensable resource for policymakers, researchers, activists, and anyone interested in advocating for the protection and enhancement of workers'' rights worldwide.',
    100
);

-- insert for land_use_rights
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'heritage.org Index of Economic Freedom for land use rights',
    'https://www.heritage.org/index/pages/all-country-scores',
    'The Heritage Foundation''s website offers a comprehensive index of economic freedom scores for various countries. It provides valuable data for policymakers and researchers alike. With indicators covering property rights, government integrity, and regulatory efficiency, it''s a vital resource for analyzing global economic trends and making informed decisions. Land Use Rights scores are picked from one of the columns named "Property Rights".',
    100
);

-- insert for environmental_protection
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'epi.yale.edu environment performance index',
    'https://epi.yale.edu/downloads',
    'Epi.yale.edu is an online hub dedicated to environmental protection, offering resources, research, and insights on pressing ecological issues. From climate change to biodiversity conservation, the platform hosts a plethora of data-driven analyses and interdisciplinary studies, fostering informed decision-making and action for a sustainable future. Downloaded the EPI2022 Results',
    100
);

-- insert for human_rights
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'Fragile States Index powered by The Fund For Peace',
    'https://fragilestatesindex.org/excel/',
    'The website Fragile States Index (fragilestatesindex.org) provides comprehensive insights into global human rights issues, offering an index that evaluates and tracks the stability and vulnerability of nations. Through extensive data analysis and expert assessments, it offers a valuable resource for understanding and addressing human rights challenges worldwide. Download the lastest excel sheet.',
    100
);

-- insert for land_use_rights
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'unstats.un.org SDG 1.4.2 data',
    'https://unstats.un.org/sdgs/dataportal/database',
    'The website "UNStats Land Use Rights Index" provides comprehensive data on land use rights globally, aiding policymakers and researchers. It offers a user-friendly interface to access critical information for sustainable development initiatives. With reliable statistics and indices, it facilitates informed decision-making, fostering equitable land management practices worldwide. Typed 1.4.2 in Data Series textbox, generated the file and downloaded.',
    100
);

-- insert for deforestation_free
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'Global Forest Watch for deforestation free',
    'https://www.globalforestwatch.org/dashboards/global/',
    'Global Forest Watch provides a comprehensive dashboard offering deforestation-free data. This platform meticulously tracks global forest cover changes, empowering users with up-to-date insights on deforestation trends. It furnishes crucial information for policymakers, researchers, and environmentalists to make informed decisions and undertake effective conservation efforts to combat deforestation worldwide. Click on download button present in the website.',
    100
);

-- insert for forest_degradation
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'Global Forest Watch for forest degradation',
    'https://www.globalforestwatch.org/dashboards/global/',
    'This provides comprehensive data and interactive maps tracking forest degradation worldwide. Offering real-time insights and analysis, the website aids in monitoring deforestation trends, assessing risks to biodiversity, and informing conservation efforts. Users can access diverse datasets, empowering informed decision-making for sustainable forest management and environmental protection initiatives. Click on download button present in the website.',
    100
);

-- insert for indigenous_people
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'mahb.stanford.edu indigenous rights risk report',
    'https://mahb.stanford.edu/wp-content/uploads/2014/12/Indigenous-Rights-Risk-Report.pdf',
    'The website hosts a comprehensive report titled "Indigenous Rights at Risk," examining global challenges faced by indigenous communities. It addresses issues such as land rights, cultural preservation, and socio-economic disparities. The report offers valuable insights into advocating for indigenous rights and fostering sustainable development in collaboration with these marginalized populations.',
    100
);

-- insert for forest_related_regulations
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'FAO UN- Global Forest Resources Assessment',
    'https://fra-data.fao.org/assessments/fra/2020/WO/sections/forestPolicy/',
    'The website offers comprehensive data on forest-related regulations worldwide, focusing on the 2020 Global Forest Resources Assessment. Users can access detailed assessments, policies, and regulations concerning forests. It serves as a valuable resource for policymakers, researchers, and environmentalists, aiding in informed decision-making and sustainable forest management practices. Select all countries and FRA variables and download csv for National only.',
    100
);

-- insert for trade_customs_regulations
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'archive.doingbusiness.org ease of doing business - trading across borders index',
    'https://archive.doingbusiness.org/content/dam/doingBusiness/excel/db2020/Historical-data---COMPLETE-dataset-with-scores.xlsx',
    'It is a rich repository of information on global trade customs regulations. It offers in-depth analysis and country-specific data on customs procedures, tariffs, and documentation requirements. With its user-friendly interface and regularly updated content, it serves as a valuable resource for businesses navigating international trade regulations seamlessly. Download the file in the url.',
    100
);

-- insert for third_party_rights
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'heritage.org Index of Economic Freedom for third party rights',
    'https://www.heritage.org/index/pages/all-country-scores',
    'This website offers an extensive database of country scores evaluating various aspects of economic freedom, including third-party rights. Users can access detailed analyses and rankings regarding property rights, contract enforcement, and legal frameworks, aiding in understanding global standards and fostering informed decision-making for businesses and policymakers. Overall Scores depict the aggregated third party rights.',
    100
);

-- insert for commodity = cattle 
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'trace.earth for deforestation risk concerning cattle products',
    'https://trase.earth/open-data/search/beef',
    'Trase Earth''s beef data repository provides comprehensive insights into the global beef supply chain. Featuring open-access datasets, it empowers researchers, policymakers, and stakeholders to analyze beef production, trade, and associated environmental impacts. Users can explore detailed information on beef production locations, transportation routes, and land-use changes, facilitating informed decision-making towards sustainability. The platform enables querying specific parameters, ensuring tailored data retrieval for diverse research needs. By centralizing reliable data on beef, Trase Earth fosters transparency and accountability within the industry, supporting efforts to mitigate deforestation, biodiversity loss, and greenhouse gas emissions associated with beef production.',
    80
);

-- insert for commodity = cocoa 
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'trace.earth for deforestation risk concerning cocoa products',
    'https://trase.earth/open-data/search/cocoa',
    'Trase Earth''s cocoa data repository provides comprehensive insights into the global cocoa supply chain. Featuring open-access datasets, it empowers researchers, policymakers, and stakeholders to analyze beef production, trade, and associated environmental impacts. Users can explore detailed information on beef production locations, transportation routes, and land-use changes, facilitating informed decision-making towards sustainability. The platform enables querying specific parameters, ensuring tailored data retrieval for diverse research needs. By centralizing reliable data on cocoa, Trase Earth fosters transparency and accountability within the industry, supporting efforts to mitigate deforestation, biodiversity loss, and greenhouse gas emissions associated with cocoa production.',
    80
);

-- insert for commodity = soy 
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'trace.earth for deforestation risk concerning soy products',
    'https://trase.earth/open-data/search/soy',
    'Trase Earth''s soy data repository provides comprehensive insights into the global soy supply chain. Featuring open-access datasets, it empowers researchers, policymakers, and stakeholders to analyze beef production, trade, and associated environmental impacts. Users can explore detailed information on beef production locations, transportation routes, and land-use changes, facilitating informed decision-making towards sustainability. The platform enables querying specific parameters, ensuring tailored data retrieval for diverse research needs. By centralizing reliable data on soy, Trase Earth fosters transparency and accountability within the industry, supporting efforts to mitigate deforestation, biodiversity loss, and greenhouse gas emissions associated with soy production.',
    80
);

-- insert for all commodities
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'DeDuCE: Agriculture and forestry-driven deforestation and associated carbon emissions from 2001-2022',
    'https://zenodo.org/records/10674962',
    'The dataset offers country-level estimates of deforestation and carbon emissions linked to agriculture and forestry from 2001-2022, with sub-national data for Brazil. Utilizing the DeDuCE model, it merges remote sensing data and agricultural statistics, providing detailed global insights across 9100 country-commodity combinations in 176 countries and 184 commodities. Powered by Google Earth Engine and Python, it offers unparalleled scope and granularity.',
    50
);

-- insert for human_rights world in data
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'Human Rights Index- Out World in Data',
    'https://ourworldindata.org/grapher/human-rights-index-vdem?tab=table',
    'The website offers detailed human rights data from the V-Dem project, covering civil liberties like freedom from torture and forced labor, property rights, and freedoms of movement, religion, expression, and association. It provides an aggregate civil liberties index and various visualizations, aiding in comprehensive human rights analysis.',
    95
);

-- insert for publiceye for employee rights
INSERT INTO eudr.risk_sources
(
    source_name,
    category_id,
    category_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'Employee Rights PublicEye',
    2,
    'employee_rights',
    'https://www.publiceye.ch/en/topics/soft-commodity-trading/most-severe-issues-related-to-agricultural-production-and-trade/human-and-labour-rights-violations',
    'The Public Eye website highlights human and labor rights violations in agricultural production, focusing on issues such as inadequate wages, forced and child labor, and unsafe working conditions. The site emphasizes the prevalence of these violations in industries like cocoa production, advocating for living wages and improved safety standards.',
    95
);

-- insert for publiceye for deforestation and forest_degradation
INSERT INTO eudr.risk_sources
(
    source_name,
    category_id,
    category_name,
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'Deforestation and Forest Degradation PublicEye',
    7,
    'forest_degradation',
    'https://www.publiceye.ch/en/topics/soft-commodity-trading/most-severe-issues-related-to-agricultural-production-and-trade/deforestation-and-land-grabbing',
    'The webpage from Public Eye discusses the environmental and social impacts of deforestation and land grabbing in agricultural production. It highlights how industrial agriculture, driven by the demand for flex crops like soy and palm oil, leads to significant deforestation and land conflicts globally.',
    95
);

-- insert for publiceye for corruption
INSERT INTO eudr.risk_sources
(
    source_name, 
    category_id,
    category_name,
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'Tax dodging and Corrpution PublicEye',
    1,
    'corruption',
    'https://www.publiceye.ch/en/topics/soft-commodity-trading/most-severe-issues-related-to-agricultural-production-and-trade/tax-dodging-and-corruption',
    'The Public Eye page discusses tax dodging and corruption in soft commodity trading. It highlights the high risk of tax offenses and corruption due to lax policies, politically exposed persons, and transaction opacity. It provides examples, such as transfer mispricing by major grain traders in Argentina. It emphasizes the role of transparency and regulations in mitigating these issues.',
    95
);

-- insert for publiceye for land grabbing
INSERT INTO eudr.risk_sources
(
    source_name,
    category_id,
    category_name,
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'Land Grabbing PublicEye',
    3,
    'land_use_rights',
    'https://www.publiceye.ch/en/topics/soft-commodity-trading/most-severe-issues-related-to-agricultural-production-and-trade/deforestation-and-land-grabbing',
    'The Public Eye website discusses the severe impact of land grabbing driven by agricultural commodity production. The site emphasizes the role of multinational corporations in these practices and calls for stricter regulations to protect land use rights and address human rights violations.',
    95
);

-- insert for environmental protection EU GDP share
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'Environmental protection expenditure in EU',
    'https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Government_expenditure_on_environmental_protection',
    'The Eurostat page on government expenditure by function provides data on spending, including environmental protection, across EU member states. It includes statistics on expenditure categories like waste management, pollution control, and biodiversity conservation, highlighting government priorities and budget allocations. This data helps assess the effectiveness of environmental policies and funding',
    95
);

-- insert for thrid_party_rights freedom house
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'Freedomhouse data for third party rights',
    'https://freedomhouse.org/report/freedom-world',
    'Freedom House''s "Freedom in the World" report assesses the state of political rights and civil liberties globally. Published annually, it evaluates 195 countries and 15 territories, providing scores and narratives that highlight issues like freedom of expression, electoral processes, and rule of law. This report serves as a crucial resource for policymakers, activists, and researchers advocating for human rights.',
    95
);

-- insert for indigenous people United Nations report 2023
INSERT INTO eudr.risk_sources
(
    source_name, 
    url, 
    description,
    confidence_percentage
)
VALUES 
(
    'United Nations report for indigenous people rights',
    'https://social.desa.un.org/sites/default/files/Regional%20Dialogues_UNPFII%202023.pdf',
    'This report provides an overview of discussions held in various regional dialogues concerning the rights of indigenous peoples. It captures key themes, challenges, and recommendations presented during these dialogues, focusing on areas such as land rights, cultural preservation, and socio-economic development. This report highlights the importance of implementing the United Nations Declaration on the Rights of Indigenous Peoples (UNDRIP), addressing issues like discrimination, environmental protection, and ensuring meaningful participation of indigenous communities in decision-making processes.',
    95
);