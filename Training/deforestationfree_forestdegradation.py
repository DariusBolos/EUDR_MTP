# -*- coding: utf-8 -*-
"""ForestWatch_prepocess.ipynb
Original file is located at
    https://colab.research.google.com/drive/1DmFlUP_0ZLB7-yydm55Y9qXwuD4nVDaj
"""
import sys
import datetime
import pandas as pd
from pandasql import sqldf
import psycopg2
from database_operations import get_risk_source_id
from database_operations import get_risk_category_id
from database_operations import risks_table_operations
from database_operations import update_category_values
from country_standard import standardize
from sklearn.preprocessing import MinMaxScaler
import os
import warnings
warnings.filterwarnings("ignore")

root_path = '/Users/sidpai/Desktop/Sem_2'
os.chdir(root_path)

#root_path = os.environ.get("HOME")
#os.chdir(root_path)

category_name1 = 'deforestation_free'
source_name1 = 'Global Forest Watch for deforestation free'
category_name2 = 'forest_degradation'
source_name2 = 'Global Forest Watch for forest degradation'

# Get the category ID for deforstation free and forest degradation risk
category_id1 = int(get_risk_category_id(category_name1))
source_id1 = int(get_risk_source_id(source_name1))
category_id2 = int(get_risk_category_id(category_name2))
source_id2 = int(get_risk_source_id(source_name2))

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id1, category_id1, category_name1)
update_category_values(source_id2, category_id2, category_name2)

# Corruption index available for previous year
year = str(datetime.date.today().year - 1)

# Load excel
excel_file = 'EUDR_MTP/Datasets/global_forestloss.xlsx'
sheet_name = 'Country tree cover loss'
df = pd.read_excel(excel_file, sheet_name=sheet_name)

#Preprocessing
#Filtered the data with threshold = 30, 0 threshold means the size of the country, canopy means the percentage of the are which is covered by trees, it depends on studies but 25-30% of canopy is a forest
threshold = df[df['threshold'] == 30].reset_index(drop=True)
threshold = threshold.drop('threshold', axis=1)

# drop countries where gain is zero
threshold = threshold[threshold['gain_2000-2020_ha'] != 0]
threshold = threshold[threshold['country'] != 'Burkina Faso']

#area_ha = country size in hectar extent ha = forestsize
#summarized forest loss for the 20 years
year_loss = ['tc_loss_ha_2001', 'tc_loss_ha_2002', 'tc_loss_ha_2003', 'tc_loss_ha_2004', 'tc_loss_ha_2005',
                  'tc_loss_ha_2006', 'tc_loss_ha_2007', 'tc_loss_ha_2008', 'tc_loss_ha_2009', 'tc_loss_ha_2010',
                  'tc_loss_ha_2011', 'tc_loss_ha_2012', 'tc_loss_ha_2013', 'tc_loss_ha_2014', 'tc_loss_ha_2015',
                  'tc_loss_ha_2016', 'tc_loss_ha_2017', 'tc_loss_ha_2018', 'tc_loss_ha_2019', 'tc_loss_ha_2020',
                  'tc_loss_ha_2021']

#summarized forest loss for the 20 years                 
year_loss_10 = ['tc_loss_ha_2010','tc_loss_ha_2011', 'tc_loss_ha_2012', 'tc_loss_ha_2013', 'tc_loss_ha_2014', 'tc_loss_ha_2015',
                  'tc_loss_ha_2016', 'tc_loss_ha_2017', 'tc_loss_ha_2018', 'tc_loss_ha_2019', 'tc_loss_ha_2020',
                  'tc_loss_ha_2021', 'tc_loss_ha_2022']

# drop countries where there are no data for at least 10 years
threshold = threshold[(threshold[year_loss] != 0).sum(axis=1) >= 10]
threshold['loss_2001-2021'] = threshold[year_loss].sum(axis=1)
threshold['loss_2010-2022'] = threshold[year_loss_10].sum(axis=1)

# extent_2010_% extent_2010_ha/area_ha
threshold['extent_2010_%'] = ((threshold['extent_2010_ha'])/(threshold['area_ha']))*100

#how many percentage of the 2010 extent was lost until 2022 - deforestation free
threshold['loss_2010-2022_%'] = ((threshold['loss_2010-2022'])/(threshold['extent_2010_ha']))*100

#dividing loss of 2001-2021 with gain of 2000-2020 (higher - lost more than gained) - forest degradation
threshold['loss/gained'] = ((threshold['loss_2001-2021'])/(threshold['gain_2000-2020_ha']))

df2 = threshold[['country','loss_2010-2022_%','loss/gained']]
query = "select `country` as country,`loss_2010-2022_%` as loss_percent from df2"
def_free = sqldf(query)
query = "select `country` as country,`loss/gained` as loss_gain, log(`loss/gained`) as log_loss_gain from df2"
forest_deg = sqldf(query)

# normalising and ingesting for deforestation_free
max1 = 100
min1 = 0
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1

vals_list = []
rows = df2.shape[0]
for i in range(rows):
    country = def_free.loc[i][0]
    loss_percent = def_free.loc[i][1]
    risk = round(a*loss_percent + b,1)
    desc = "The Forest Loss perentage for " + country + " over 2010-2021 is " + str(loss_percent) + ". Higher the percentage worse is the forest cover loss. This score is normalised on a risk scale between 1(best) and 6(worst)."
    vals_list.append((source_id1, category_id1, int(year), country, risk, desc, risk, desc))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)


# normalising and ingesting for forest_degradation
scaler = MinMaxScaler(feature_range=(1,6))
scaler.fit(forest_deg[['log_loss_gain']])
vals_list = []
rows = forest_deg.shape[0]
for i in range(rows):
    country = forest_deg.loc[i][0]
    log_val = [[forest_deg.loc[i][2]]]
    risk = round(scaler.transform(log_val)[0][0],1)
    desc = "Forest Degradation for " + country + " over 2001-2021 is " + str(forest_deg.loc[i][1]) + ". Higher the score worse is the forest degradation in the country. This score is normalised on a risk scale between 1(best) and 6(worst) on the logarithmic value of the loss."
    vals_list.append((source_id2, category_id2, int(year), country, risk, desc, risk, desc))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)