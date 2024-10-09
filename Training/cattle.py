import sys
import pandas as pd
from pandasql import sqldf
import requests
import datetime
import psycopg2
import numpy as np
from database_operations import get_risk_source_id
from database_operations import get_commodity_id
from database_operations import get_risk_category_id
from database_operations import commodity_risks_table_operations
from database_operations import update_category_values
from database_operations import exporter_agreements_table_operations
from country_standard import standardize
from country_standard import get_standard_country_codes
import os
import warnings
warnings.filterwarnings("ignore")

root_path = '/Users/sidpai/Desktop/Sem_2'
os.chdir(root_path)

#root_path = os.environ.get("HOME")
#os.chdir(root_path)

# Will be later converted to user interactive
commodity_name = 'Cattle'
source_name = 'trace.earth for deforestation risk concerning cattle products'
category_name = 'forest_degradation'
# Get ids
commodity_id = int(get_commodity_id(commodity_name))
source_id = int(get_risk_source_id(source_name))
category_id = int(get_risk_category_id(category_name))

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Corruption index available for previous year
year = str(datetime.date.today().year - 1)
brazil_file = "EUDR_MTP/Datasets/Cattle/brazil_beef_2023.csv"
paraguay_file = "EUDR_MTP/Datasets/Cattle/paraguay_beef_2023.csv"

if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

# Read file into pandas dataframe and process
# Find which row is header row
file_brazil = pd.read_csv(brazil_file)
file_paraguay = pd.read_csv(paraguay_file)
query_brazil_risk = '''with cte as (select sum(cattle_deforestation_5_year_total_exposure) as tot from file_brazil 
                    where year = (select max(year) from file_brazil))
                    select country_of_production,state_of_production,total_def*100/tot as percentage_def from
                    (select country_of_production,
                    state_of_production,
                    sum(coalesce(cattle_deforestation_5_year_total_exposure,0)) as total_def
                    from file_brazil
                    where year = (select max(year) from file_brazil) 
                    group by country_of_production,state_of_production),cte'''
query_paraguay_risk = '''with cte as (select sum(cattle_deforestation_5_year_total_exposure) as tot from file_paraguay 
                    where year = (select max(year) from file_paraguay))
                    select country_of_production,department,total_def*100/tot as percentage_def from
                    (select country_of_production,
                    department,
                    sum(coalesce(cattle_deforestation_5_year_total_exposure,0)) as total_def
                    from file_paraguay
                    where year = (select max(year) from file_paraguay) 
                    group by country_of_production,department),cte'''

query_brazil_exporter = '''select country_of_production,zero_deforestation_brazil_beef,exporter
                        from file_brazil
                        where year = (select max(year) from file_brazil)
                        group by exporter
                        '''
query_paraguay_exporter = '''select country_of_production,zero_deforestation_paraguay_beef,exporter
                        from file_paraguay
                        where year = (select max(year) from file_paraguay)
                        group by exporter
                        '''
df_brazil_risk = sqldf(query_brazil_risk)
df_paraguay_risk = sqldf(query_paraguay_risk)
df_brazil_exporter = sqldf(query_brazil_exporter)
df_paraguay_exporter = sqldf(query_paraguay_exporter)

# Normalization parameters
max1 = 100
min1 = 0
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1

# Brazil risk data load
vals_list = []
rows = df_brazil_risk.shape[0]
country = get_standard_country_codes(['BRAZIL'])[0].strip()
for i in range(rows):
    state = df_brazil_risk.loc[i][1]
    def_score = df_brazil_risk.loc[i][2]
    risk = round(a*(def_score) + b,1)
    desc = "The percentage of deforestation in " +state+ " , Brazil is " +str(round(def_score,2))+ ". This score is normalised on a risk scale between 1(best) and 6(worst)."
    vals_list.append((commodity_id, source_id ,category_id, int(year), country, state, risk, desc, risk, desc))
commodity_risks_table_operations(vals_list)

# Paraguay risk data load
vals_list = []
rows = df_paraguay_risk.shape[0]
country = get_standard_country_codes(['PARAGUAY'])[0].strip()
for i in range(rows):
    state = df_paraguay_risk.loc[i][1]
    def_score = df_paraguay_risk.loc[i][2]
    risk = round(a*def_score + b,1)
    desc = "The percentage of deforestation in " +state+ ", Paraguay  is " +str(round(def_score,2))+ ". This score is normalised on a risk scale between 1(best) and 6(worst)."
    vals_list.append((commodity_id, source_id, category_id, int(year), country, state, risk, desc, risk, desc))
commodity_risks_table_operations(vals_list)

# Brazil exporter data load
brazil_country_code = get_standard_country_codes(['BRAZIL'])
vals_list = []
rows = df_brazil_exporter.shape[0]
for i in range(rows):
    agreement = df_brazil_exporter.loc[i][1]
    exporter = df_brazil_exporter.loc[i][2]
    vals_list.append((commodity_id,brazil_country_code,agreement,exporter,agreement))
exporter_agreements_table_operations(vals_list)

# Paraguay exporter data load
paraguay_country_code = get_standard_country_codes(['PARAGUAY'])
vals_list = []
rows = df_paraguay_exporter.shape[0]
for i in range(rows):
    agreement = df_paraguay_exporter.loc[i][1]
    exporter = df_paraguay_exporter.loc[i][2]
    vals_list.append((commodity_id,paraguay_country_code,agreement,exporter,agreement))
exporter_agreements_table_operations(vals_list)