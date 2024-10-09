import openpyxl
import sys
import pandas as pd
import numpy as np
import datetime
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
category_name = 'environmental_protection'
source_name = 'Environmental protection expenditure in EU'

# Get the category ID for corruption risk
category_id = int(get_risk_category_id(category_name))
source_id = int(get_risk_source_id(source_name))

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Corruption index available for previous year
year = str(datetime.date.today().year - 1)
filename = 'EUDR_MTP/Datasets/EU_GDP_Environmental.xlsx'
sheet_name = 'Sheet_1'
df = pd.read_excel(filename, sheet_name=sheet_name, engine='openpyxl')
df = df.drop(columns=['Waste management', 'Waste water management', 'Pollution abatement', 'Protection of biodiversity and landscape', 'R&D Environmental protection', 'Environmental protection n.e.c.'
])
df2 = df.rename(columns={'Location': 'Country', 'Environmental protection': 'gdp_contri'})

# Normalization parameters
max1 = 0.8 #0.8 because it is average share of GDP spent on env protection
min1 = 0
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1

vals_list = []
rows = df2.shape[0]
for i in range(rows):
    country = ''.join(letter for letter in df2.loc[i][0] if letter.isalnum())
    gdp_contri = float(df2.loc[i][1])/2
    risk = round(a*(max1-gdp_contri) + b,1)
    desc = "For the year " + year + ", " + country + " spent " + str(round(gdp_contri,2)) + "% of GDP for environmental protection whereas the average expenditure is 0.8%. This value is normalised on a risk scale between 1(best) and 6(worst)."
    vals_list.append((source_id, category_id, int(year), country, risk, desc, risk, desc))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)