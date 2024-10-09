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
commodity_name = 'Cocoa'
source_name = 'trace.earth for deforestation risk concerning cocoa products'
category_name = 'forest_degradation'
# Get ids
commodity_id = int(get_commodity_id(commodity_name))
source_id = int(get_risk_source_id(source_name))
category_id = int(get_risk_category_id(category_name))

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Corruption index available for previous year
year = str(datetime.date.today().year - 1)
cote_divoire_file = "EUDR_MTP/Datasets/Cocoa/cote_divoire_cocoa_2023.csv"

if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

# Read file into pandas dataframe and process
# Find which row is header row
file_cote_divoire = pd.read_csv(cote_divoire_file)
query_cote_divoire_risk = '''with cte as (select sum(cocoa_deforestation_15_years_total_exposure) as tot from file_cote_divoire 
                    where year = (select max(year) from file_cote_divoire))
                    select country_of_production,department_of_production,total_def*100/tot as percentage_def from
                    (select country_of_production,
                    department_of_production,
                    sum(coalesce(cocoa_deforestation_15_years_total_exposure,0)) as total_def
                    from file_cote_divoire
                    where year = (select max(year) from file_cote_divoire) 
                    group by country_of_production,department_of_production),cte'''

query_cote_divoire_exporter = '''select country_of_production,zero_deforestation_cote_divoire_cocoa,exporter
                        from file_cote_divoire
                        where year = (select max(year) from file_cote_divoire)
                        group by exporter
                        '''
df_cote_divoire_risk = sqldf(query_cote_divoire_risk)
df_cote_divoire_exporter = sqldf(query_cote_divoire_exporter)

# Normalization parameters
max1 = 100
min1 = 0
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1

# COTE D'IVOIRE risk data load
vals_list = []
rows = df_cote_divoire_risk.shape[0]
country = get_standard_country_codes(['COTE D''IVOIRE'])[0].strip()
for i in range(rows):
    state = df_cote_divoire_risk.loc[i][1]
    def_score = df_cote_divoire_risk.loc[i][2]
    risk = round(a*(def_score) + b,1)
    desc = "The percentage of deforestation in " +state+ " , Cote D'Ivoire is " +str(round(def_score,2))+ ". This score is normalised on a risk scale between 1(best) and 6(worst)."
    vals_list.append((commodity_id, source_id ,category_id, int(year), country, state, risk, desc, risk, desc))
commodity_risks_table_operations(vals_list)

# COTE D'IVOIRE exporter data load
country = get_standard_country_codes(['COTE D''IVOIRE'])
vals_list = []
rows = df_cote_divoire_exporter.shape[0]
for i in range(rows):
    agreement = df_cote_divoire_exporter.loc[i][1]
    exporter = df_cote_divoire_exporter.loc[i][2]
    vals_list.append((commodity_id,country,agreement,exporter,agreement))
exporter_agreements_table_operations(vals_list)