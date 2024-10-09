import sys
import pandas as pd
from pandasql import sqldf
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
category_name = 'trade_customs_regulations'
source_name = 'archive.doingbusiness.org ease of doing business - trading across borders index'
# Get the category ID for trade and customs regulation risk
category_id = get_risk_category_id(category_name)
source_id = get_risk_source_id(source_name)

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Ease of doing business indicator is annual but has not been released in recent years
year = str(datetime.date.today().year - 1)
filename = "EUDR_MTP/Datasets/trade_customs_regulations_" + year + ".xlsx"
if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

# Read file into pandas dataframe and process
df = pd.read_excel(filename, header = 3)
df['DB Year'].fillna(-1, inplace=True)
df['DB Year'] = df['DB Year'].astype(int)
df['DB Year'] = df['DB Year'].astype(str)

latest_yr = str(sqldf("SELECT max(`DB Year`) as yr from df").loc[0][0])
# Filtered on the most recent available year
df2 = df.loc[(df['DB Year'] == latest_yr), ['Economy', 'Rank-Trading across borders', 'Ease of doing business rank']]
df2 = df2.dropna(subset=['Rank-Trading across borders'])
df2 = df2.reset_index(drop=True)

df2['Ease of doing business rank'] = df2['Ease of doing business rank'].astype(int)
df2['Ease of doing business rank'] = df2['Ease of doing business rank'].astype(str)

# Normalization parameters
max1 = 190
min1 = 1
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1

# Normalize land use rights as risk between 1 and 6
vals_list = []
rows = df2.shape[0]
for i in range(rows):
    country = df2.loc[i][0]
    trading = df2.loc[i][1]
    risk = round(a*trading + b,1)
    desc = "The Trade and Customs Regulation risk score for " + country + " is " + str(risk) + ". According to the Ease of Doing Business Index, " + country + " ranked " + str(df2.loc[i][2]) + " in the world regarding the ease of doing business."
    vals_list.append((source_id, category_id, int(year), country, risk, desc, risk, desc))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)