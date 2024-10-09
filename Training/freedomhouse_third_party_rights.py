import sys
import pandas as pd
from pandasql import sqldf
import datetime
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
category_name = 'third_party_rights'
source_name = 'Freedomhouse data for third party rights'
# Get the category ID for corruption risk
category_id = int(get_risk_category_id(category_name))
source_id = int(get_risk_source_id(source_name))

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Corruption index available for previous year
year = str(datetime.date.today().year - 1)
filename = "EUDR_MTP/Datasets/third_party_rights_freedomhouse.xlsx"
sheet = 'data'
if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

# Read file into pandas dataframe and process
df = pd.read_excel(filename, sheet_name=sheet, header=1)
df2 = sqldf("select * from df where Edition=2024 and `C/T`='c'")
df2 = df2[['Country/Territory','Total']].dropna().reset_index(drop=True)

# Normalization parameters
max1 = 100
min1 = 0
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1

# Normalize cpi as risk between 1 and 6.
# Subtract score from max value because risk value and score are inversely proportional.
vals_list = []
rows = df2.shape[0]
for i in range(rows):
    country = df2.loc[i][0]
    risk_score = df2.loc[i][1]
    risk = round(a*(max1-risk_score) + b,1)
    description = "The Freedom score for " + country + " in the year " + year + " is " + str(risk_score) + ". Higher the score, better are the conditions, as a result, lower risk. This score is normalised on a risk scale between 1(best) and 6(worst)."
    vals_list.append((source_id, category_id, int(year), country, risk, description, risk, description))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)