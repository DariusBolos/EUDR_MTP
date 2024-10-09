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
import warnings
warnings.filterwarnings("ignore")

root_path = '/Users/sidpai/Desktop/Sem_2'
os.chdir(root_path)

#root_path = os.environ.get("HOME")
#os.chdir(root_path)

# Will be later converted to user interactive
category_name = 'human_rights'
source_name = 'Human Rights Index- Out World in Data'
# Get the category ID for corruption risk
category_id = int(get_risk_category_id(category_name))
source_id = int(get_risk_source_id(source_name))

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Corruption index available for previous year
year = str(datetime.date.today().year - 1)
filename = "EUDR_MTP/Datasets/humanrights_world_in_data_" + year + ".csv"
if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

# Read file into pandas dataframe and process
df = pd.read_csv(filename)
df2 = df[['country','score']]

# Normalization parameters
max1 = 1
min1 = 0
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1

# Normalize score as risk between 1 and 6. 
# Subtract score from max value because risk value and score are inversely proportional.
vals_list = []
rows = df2.shape[0]
for i in range(rows):
    country = df2.loc[i][0]
    human_r = float(df2.loc[i][1])
    risk = round(a*(1-human_r) + b,1)
    desc = "The Human Rights score (between 0 and 1) for " + country + " in the year " + year + " is " + str(human_r) + ". Higher score indicates better human rights. This score is normalised on a risk scale between 1(best) and 6(worst)."
    vals_list.append((source_id, category_id, int(year), country, risk, desc, risk, desc))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)