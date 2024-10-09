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
commodity_name = 'Soy'
source_name = 'trace.earth for deforestation risk concerning soy products'
category_name = 'forest_degradation'
# Get ids
commodity_id = int(get_commodity_id(commodity_name))
source_id = int(get_risk_source_id(source_name))
category_id = int(get_risk_category_id(category_name))

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Corruption index available for previous year
year = str(datetime.date.today().year - 1)
argentina_file = "EUDR_MTP/Datasets/Soy/argentina_soy_2023.csv"
bolivia_file = "EUDR_MTP/Datasets/Soy/bolivia_soy_2023.csv"
brazil_file = "EUDR_MTP/Datasets/Soy/brazil_soy_2023.csv"
paraguay_file = "EUDR_MTP/Datasets/Soy/paraguay_soy_2023.csv"

if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

# Read file into pandas dataframe and process
# Find which row is header row
file_argentina = pd.read_csv(argentina_file)
file_bolivia = pd.read_csv(bolivia_file)
file_brazil = pd.read_csv(brazil_file)
file_paraguay = pd.read_csv(paraguay_file)

query_argentina_risk = '''with cte as (select sum(soy_deforestation_5_year_total_exposure) as tot from file_argentina 
                    where year = (select max(year) from file_argentina))
                    select country_of_production,province_of_production,total_def*100/tot as percentage_def from
                    (select country_of_production,
                    province_of_production,
                    sum(coalesce(soy_deforestation_5_year_total_exposure,0)) as total_def
                    from file_argentina
                    where year = (select max(year) from file_argentina) 
                    group by country_of_production,province_of_production),cte'''
query_bolivia_risk = '''with cte as (select sum(soy_deforestation_5_year_total_exposure) as tot from file_bolivia 
                    where year = (select max(year) from file_bolivia))
                    select country_of_production,province_of_production,total_def*100/tot as percentage_def from
                    (select country_of_production,
                    province_of_production,
                    sum(coalesce(soy_deforestation_5_year_total_exposure,0)) as total_def
                    from file_bolivia
                    where year = (select max(year) from file_bolivia) 
                    group by country_of_production,province_of_production),cte'''
query_brazil_risk = '''with cte as (select sum(soy_deforestation_5_year_total_exposure) as tot from file_brazil 
                    where year = (select max(year) from file_brazil))
                    select country_of_production,state,total_def*100/tot as percentage_def from
                    (select country_of_production,
                    state,
                    sum(coalesce(soy_deforestation_5_year_total_exposure,0)) as total_def
                    from file_brazil
                    where year = (select max(year) from file_brazil) 
                    group by country_of_production,state),cte'''
query_paraguay_risk = '''with cte as (select sum(soy_deforestation_5_year_total_exposure) as tot from file_paraguay 
                    where year = (select max(year) from file_paraguay))
                    select country_of_production,department,total_def*100/tot as percentage_def from
                    (select country_of_production,
                    department,
                    sum(coalesce(soy_deforestation_5_year_total_exposure,0)) as total_def
                    from file_paraguay
                    where year = (select max(year) from file_paraguay) 
                    group by country_of_production,department),cte'''


query_argentina_exporter = '''select country_of_production,zero_deforestation_argentina_soy,exporter
                        from file_argentina
                        where year = (select max(year) from file_argentina)
                        group by exporter
                        '''
query_bolivia_exporter = '''select country_of_production,zero_deforestation_bolivia_soy,exporter_group
                        from file_bolivia
                        where year = (select max(year) from file_argentina)
                        group by exporter_group
                        '''
query_brazil_exporter = '''select country_of_production,zero_deforestation_brazil_soy,exporter
                        from file_brazil
                        where year = (select max(year) from file_argentina)
                        group by exporter
                        '''
query_paraguay_exporter = '''select country_of_production,zero_deforestation_paraguay_soy,exporter
                        from file_paraguay
                        where year = (select max(year) from file_argentina)
                        group by exporter
                        '''

df_argentina_risk = sqldf(query_argentina_risk)
df_bolivia_risk = sqldf(query_bolivia_risk)
df_brazil_risk = sqldf(query_brazil_risk)
df_paraguay_risk = sqldf(query_paraguay_risk)

df_argentina_exporter = sqldf(query_argentina_exporter)
df_bolivia_exporter = sqldf(query_bolivia_exporter)
df_brazil_exporter = sqldf(query_brazil_exporter)
df_paraguay_exporter = sqldf(query_paraguay_exporter)

# Normalization parameters
max1 = 100
min1 = 0
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1

def risk_data_load(df,ctry):
    vals_list = []
    rows = df.shape[0]
    country = get_standard_country_codes([ctry])[0].strip()
    for i in range(rows):
        state = df.loc[i][1]
        def_score = df.loc[i][2]
        risk = round(a*(def_score) + b,1)
        desc = "The percentage of deforestation in " +state+ ", "+ctry+" is " +str(round(def_score,2))+ ". This score is normalised on a risk scale between 1(best) and 6(worst)."
        vals_list.append((commodity_id, source_id ,category_id, int(year), country, state, risk, desc, risk, desc))
    commodity_risks_table_operations(vals_list)


def exporter_data_load(df,ctry):
    country = get_standard_country_codes([ctry])
    vals_list = []
    rows = df.shape[0]
    for i in range(rows):
        agreement = df.loc[i][1]
        exporter = df.loc[i][2]
        vals_list.append((commodity_id,country,agreement,exporter,agreement))
    exporter_agreements_table_operations(vals_list)


# load risk data to database
risk_data_load(df_argentina_risk,'Argentina')
risk_data_load(df_bolivia_risk,'Bolivia')
risk_data_load(df_brazil_risk,'Brazil')
risk_data_load(df_paraguay_risk,'Paraguay')

# load exporter agreement data to database
exporter_data_load(df_argentina_exporter,'Argentina')
exporter_data_load(df_bolivia_exporter,'Bolivia')
exporter_data_load(df_brazil_exporter,'Brazil')
exporter_data_load(df_paraguay_exporter,'Paraguay')