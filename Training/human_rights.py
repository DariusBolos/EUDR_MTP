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
category_name = 'human_rights'
source_name = 'Fragile States Index powered by The Fund For Peace'
# Get the category ID for corruption risk
category_id = int(get_risk_category_id(category_name))
source_id = int(get_risk_source_id(source_name))

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Corruption index available for previous year
year = str(datetime.date.today().year - 1)
filename = "EUDR_MTP/Datasets/human_rights_" + year + ".xlsx"
if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

# Read file into pandas dataframe and process
df = pd.read_excel(filename)
df2 = df[['Country','P3: Human Rights','Total']]

# Normalization parameters
max1 = 10
min1 = 0
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1

# Normalize cpi as risk between 1 and 6. 
# Subtract score from max value because risk_score and cpi_score are inversely proportional.
vals_list = []
rows = df2.shape[0]
for i in range(rows):
    country = df2.loc[i][0]
    human_r = float(df2.loc[i][1])
    tot = float(df2.loc[i][2])
    resulting_score = ((tot/12) + human_r)/2
    risk = round(a*resulting_score + b,1)
    desc = "The Human Rights score (between 1 and 10) for " + country + " in the year " + year + " is " + str(human_r) + " and the total aggregate score (between 1 and 10) is " + str(round(tot/12,1)) + ". Higher the score worse is the country performance. This score is normalised on a risk scale between 1(best) and 6(worst)."
    vals_list.append((source_id, category_id, int(year), country, risk, desc, risk, desc))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)