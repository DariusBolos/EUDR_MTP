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
category_name = 'environmental_protection'
source_name = 'epi.yale.edu environment performance index'
# Get the category ID for environmental protection risk
category_id = get_risk_category_id(category_name)
source_id = get_risk_source_id(source_name)

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Environmental performance index available for year 2022
year = str(datetime.date.today().year - 1)
filename = "EUDR_MTP/Datasets/environmental_protection_" + year + ".csv"
if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

# Read file into pandas dataframe and process
df = pd.read_csv(filename)
df2 = df[['country','EPI.new','EPI.change','EPI.rnk.new']]

# Normalization parameters
max1 = 100
min1 = 0
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1

# Normalize epi as risk between 1 and 6
# Subtract score from max value because risk_score and epi_score are inversely proportional
vals_list = []
rows = df2.shape[0]
for i in range(rows):
    country = df2.loc[i][0]
    epi = df2.loc[i][1]
    risk = round(a*(max1-epi) + b,1)
    delta = df2.loc[i][2]
    desc = "The EPI score for " + country + " in the year " + year + " is " + str(epi) + ". " + country + " ranks " + str(df2.loc[i][3]) + " worldwide according to the EPI. The index score has " + ("improved by " + str(delta) + " units" if delta > 0 else ("deteriorated by " + str(abs(delta)) + " units" if delta < 0 else "remained unchanged")) + " compared to the previous assessment."
    vals_list.append((source_id, category_id, int(year), country, risk, desc, risk, desc))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)