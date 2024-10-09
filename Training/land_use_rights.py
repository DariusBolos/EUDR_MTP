import sys
import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup
import psycopg2
import numpy as np
from database_operations import get_risk_source_id
from database_operations import get_risk_category_id
from database_operations import risks_table_operations
from database_operations import update_category_values
from country_standard import standardize
import os

root_path = '/Users/sidpai/Desktop/Sem_2'
os.chdir(root_path)

#root_path = os.environ.get("HOME")
#os.chdir(root_path)

# Will be later converted to user interactive
category_name = 'land_use_rights'
source_name = 'unstats.un.org SDG 1.4.2 data'
# Get the category ID for land use rights risk
category_id = get_risk_category_id(category_name)
source_id = get_risk_source_id(source_name)

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Land use rights indicator is available for some countries with data retrieved for different years
year = str(datetime.date.today().year-1)
filename = "EUDR_MTP/Datasets/land_use_rights_" + year + ".xlsx"
if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

# Read file into pandas dataframe and process
df = pd.read_excel(filename, sheet_name=1)
# Filtered on the Series: Proportion of people with legally recognized documentation of their rights to land out of total adult population, by sex (%)
df2 = df.loc[(df['SeriesCode'] == 'SP_LGL_LNDDOC') & (df['Sex'] == 'BOTHSEX'), ['GeoAreaName', 'TimePeriod', 'Value']]
df2 = df2.loc[df2.groupby('GeoAreaName')['TimePeriod'].idxmax()]
df2 = df2.reset_index(drop=True)

# Normalization parameters
max1 = 100
min1 = 0
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1

# Normalize land use rights as risk between 1 and 6
vals_list = []
rows = df2.shape[0]
for i in range(rows):
    country = df2.loc[i][0]
    data_year = df2.loc[i][1]
    land_use = df2.loc[i][2]
    risk = round(a*(max1-land_use) + b,1)
    desc = "The Land Use Rights risk score for " + country + " in the year " + str(data_year) + " is " + str(risk) + ". In " + country + ", " + str(land_use) + "% of people out of the total adult population have legally recognized documentation of their rights to land out."
    vals_list.append((source_id, category_id, int(year), country, risk, desc, risk, desc))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)