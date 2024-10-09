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
category_name = 'corruption'
source_name = 'transparency.org corruption perception index'
# Get the category ID for corruption risk
category_id = int(get_risk_category_id(category_name))
source_id = int(get_risk_source_id(source_name))

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Corruption index available for previous year
year = str(datetime.date.today().year - 1)
filename = "EUDR_MTP/Datasets/corruption_" + year + ".xlsx"
if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

'''
# Find excel files present in the webpage
url = "https://www.transparency.org/en/cpi/" + year
ext = "xlsx"
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')
excels = [node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
excel_url = excels[0]

response = requests.get(excel_url)
if !response.ok:
print("Bad Response: Perhaps URL is incorrect or file for " + year + " is not present.")
System.exit(-1)

# Write response contents to a file and save in directory
with open(filename, mode="wb") as file:
file.write(response.content)
'''
# Read file into pandas dataframe and process
# Find which row is header row
df = pd.read_excel(filename, nrows=20)
i, c = np.where(df == "Region") # Region is one of the columns
df = pd.read_excel(filename, header=i[0]+1) # i an array indicating (Row location of Region - 1)
df2 = df[['Country / Territory','CPI score ' + year]]

# Normalization parameters
max1 = 100
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
    cpi = df2.loc[i][1]
    risk = round(a*(max1-cpi) + b,1)
    desc = "The CPI score for " + country + " in the year " + year + " is " + str(cpi) + ". This score is normalised on a risk scale between 1(best) and 6(worst)."
    vals_list.append((source_id, category_id, int(year), country, risk, desc, risk, desc))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)