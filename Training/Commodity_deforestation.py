import openpyxl
import sys
import pandas as pd
from pandasql import sqldf
import requests
import datetime
import psycopg2
import math
import numpy as np
from database_operations import get_risk_source_id
from database_operations import get_commodity_id
from database_operations import get_risk_category_id
from database_operations import commodity_risks_table_operations
from database_operations import update_category_values
from database_operations import exporter_agreements_table_operations
from country_standard import standardize
from country_standard import get_standard_country_codes
from sklearn.preprocessing import MinMaxScaler
import os
import warnings
warnings.filterwarnings("ignore")

root_path = '/Users/sidpai/Desktop/Sem_2'
os.chdir(root_path)

#root_path = os.environ.get("HOME")
#os.chdir(root_path)

# Set year
year = str(datetime.date.today().year - 1)

filtered_df = pd.read_excel('EUDR_MTP/Datasets/commoditybased_deforestation.xlsx')

columns_to_drop = ['Continent/Country group', 'Commodity group', 'Deforestation risk, amortized (ha)',
                   'Deforestation emissions excl. peat drainage, unamortized (MtCO2)','Deforestation emissions excl. peat drainage, amortized (MtCO2)',
                   'Peatland drainage emissions (MtCO2)','Deforestation emissions incl. peat drainage, amortized (MtCO2)']
filtered_df.drop(columns=columns_to_drop, inplace=True)

# Change cattle names
cattle_mapping = {'Cattle meat': 'Cattle', 'Leather': 'Cattle'}

# Use the updated mapping with default value
filtered_df['Commodity'] = filtered_df['Commodity'].map(lambda x: cattle_mapping.get(x, x))

# Aggregate forest and cattle related rows
forest_columns = [
    'Forest plantation (Alder)',
    'Forest plantation (Australian Blackwood)', 'Forest plantation (Bamboo)',
    'Forest plantation (Birch)', 'Forest plantation (Bluegum)',
    'Forest plantation (Broadleaf)', 'Forest plantation (Fir)',
    'Forest plantation (Gum)', 'Forest plantation (Maple)',
    'Forest plantation (Mix of needleleaf and broadleaf)', 'Forest plantation (Needleleaf)',
    'Forest plantation (Padauk)', 'Forest plantation (Pine)', 'Forest plantation (Sal)',
    'Forest plantation (Teak)', 'Forest plantation (Unclassified)'
]

forest_df = filtered_df[filtered_df['Commodity'].isin(forest_columns)]
forest_df = forest_df.reset_index()

aggregation = {
    
    'Deforestation attribution, unamortized (ha)': 'sum', 
    'Quality Index': 'mean'
}

grouped_forest = forest_df.groupby(['Producer country', 'Year','Commodity']).agg(aggregation)
grouped_forest = grouped_forest.reset_index()

grouped_forest['Commodity'] = grouped_forest['Commodity'].replace(to_replace=r'^Forest.*', value='Forest plantation', regex=True)

# Aggregate cattle related rows
cattle_df = filtered_df[filtered_df['Commodity'] == 'Cattle']
grouped_cattle = cattle_df.groupby(['Producer country', 'Year','Commodity']).agg(aggregation)
grouped_cattle = grouped_cattle.reset_index()

# Commodities without forest and cattle
commodities_without_forest = [
    'Cocoa beans', 'Coffee, green',
    'Oil palm fruit', 'Soya beans', 'Natural rubber in primary forms'
]

# Filter the DataFrame to keep only rows with other commodities
no_forest_df = filtered_df[filtered_df['Commodity'].isin(commodities_without_forest)]

# Merge forest data with other
merged_df = pd.concat([grouped_forest, no_forest_df], ignore_index=True)
merged_df = pd.concat([merged_df, grouped_cattle], ignore_index=True)

sorted_df = merged_df.sort_values(by=['Producer country', 'Commodity', 'Year'], ascending=True)
sorted_df = sorted_df.fillna(0)
sorted_df.rename(columns={'Producer country': 'Country', 'Deforestation attribution, unamortized (ha)': 'Risk', 'Quality Index': 'Confidence' }, inplace=True)

transformed_df = sqldf("select Country, Commodity, avg(Risk) as Risk, round(avg(confidence)*100, 2) as confidence from sorted_df group by Country, Commodity")
transformed_df['Commodity'] = transformed_df['Commodity'].replace(to_replace='Soya beans', value='Soy').replace(to_replace='Cocoa beans', value='Cocoa').replace(to_replace='Coffee, green', value='Coffee').replace(to_replace='Oil palm fruit', value='Palm Oil').replace(to_replace='Natural rubber in primary forms', value='Natural Rubber').replace(to_replace='Forest plantation', value='Wood')

# Risk data loading function
def risk_data_load(df,commodity_id, source_id ,category_id,commodity_name):
    scaler = MinMaxScaler(feature_range=(1,6))
    scaler.fit(np.log(df[['risk_score']]))
    vals_list = []
    rows = df.shape[0]
    for i in range(rows):
        country = df.loc[i][0]
        state = df.loc[i][1]
        def_score = math.log(df.loc[i][2])
        risk = round(scaler.transform([[def_score]])[0][0],1)
        desc = f"The average deforestation in {country} for {commodity_name} is "+str(round(df.loc[i][2],2))+ ". The logarithm of this score is normalised on a risk scale between 1(best) and 6(worst)."
        vals_list.append((commodity_id, source_id ,category_id, int(year), country, state, risk, desc, risk, desc))
    upsert_list = standardize(vals_list)
    commodity_risks_table_operations(upsert_list)

# Use transformed_df for ingestion into database
commodities = ["Cattle","Soy","Palm Oil","Wood","Coffee","Cocoa","Natural Rubber"]
for c in commodities:
    print(f"For commodity {c}")
    commodity_name = c
    source_name = 'DeDuCE: Agriculture and forestry-driven deforestation and associated carbon emissions from 2001-2022'
    category_name = 'forest_degradation'
    # Get ids
    commodity_id = int(get_commodity_id(commodity_name))
    source_id = int(get_risk_source_id(source_name))
    category_id = int(get_risk_category_id(category_name))

    # update category_id and category_name in eudr.risk_sources
    update_category_values(source_id, category_id, category_name)
    df = sqldf(f"select Country, null as state, case when Risk>1 then Risk else 1 end as risk_score from transformed_df where commodity = '{commodity_name}'")
    risk_data_load(df,commodity_id, source_id ,category_id,commodity_name)
