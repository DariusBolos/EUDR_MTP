import sys
import pandas as pd
import datetime
import psycopg2
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

category_name = 'forest_related_regulations'
source_name = 'FAO UN- Global Forest Resources Assessment'
# Get the category ID for rights of indigenous people risk
category_id = get_risk_category_id(category_name)
source_id = get_risk_source_id(source_name)

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Indigenous rights risk report available for year 2014, not a periodic report
year = str(datetime.date.today().year - 1)
df = pd.read_csv('EUDR_MTP/Datasets/forest_related_regulations.csv')
df = df.drop(0)

# Drop rows where NaN values are more than 2
na_counts = df.isna().sum(axis=1)
df = df[na_counts <= 2]

df.reset_index(drop=True, inplace=True)

# Adding points: Policies, Legalisation and Regulations got 2 in case of yes, others 1 point
points_mapping = {
    'Policies supporting SFM ( 1000 ha )': 2,
    'Legislations and regulations supporting SFM ( 1000 ha )': 2,
    'Platform that promotes or allows for stakeholder participation in forest policy development ( 1000 ha )': 1,
    'Traceability system(s) for wood products ( 1000 ha )': 1
}

df['point'] = df.apply(lambda row: sum(points_mapping[col] for col in points_mapping if row[col] == 'yes'), axis=1)

# Set 0 points to 1 
df['point'] = df['point'].replace(0, 1)

# Reverse the scale
score_mapping = {6: 1, 5: 2, 4: 3, 3: 4, 2: 5, 1: 6}
df['score'] = df['point'].map(score_mapping)

# List of columns to drop
columns_to_drop = [
    'Policies supporting SFM ( 1000 ha )',
    'Legislations and regulations supporting SFM ( 1000 ha )',
    'Platform that promotes or allows for stakeholder participation in forest policy development ( 1000 ha )',
    'Traceability system(s) for wood products ( 1000 ha )',
    'point'
]

# Drop the specified columns
df.drop(columns=columns_to_drop, inplace=True)
df = df.rename(columns={'Unnamed: 0':'Country'})

vals_list = []
rows = df.shape[0]
for i in range(rows):
    country = df.loc[i][0]
    risk = float(df.loc[i][1])
    desc = "The pre calculated Risk Score " + country + " is " + str(risk) + ". Scores were assigned based on the categories with higher weightage given to Policies, Legislation and regulations supporting SFM."
    vals_list.append((source_id, category_id, int(year), country, risk, desc, risk, desc))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)