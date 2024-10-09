import sys
import pandas as pd
import datetime
import psycopg2
import numpy as np
from database_operations import country_dim_insertion
import csv
import os

root_path = '/Users/sidpai/Desktop/Sem_2'
os.chdir(root_path)

#root_path = os.environ.get("HOME")
#os.chdir(root_path)

std_country_filename = "EUDR_MTP/Datasets/standard_country.csv"
if len(sys.argv) == 3:
    std_country_filename = sys.argv[2]

def get_standard_countries(filename):
    # reads csv file with standard country name and code
    print("Inserting into eudr.standard_country_dimension dimension")
    df = pd.read_csv(std_country_filename)

    # created list of tuples for upserting
    upsert_list = []
    for count in df.values.tolist():
        country_name = count[0].replace(',','')
        country_code = count[1]
        upsert_list.append((country_name, country_code, country_name))

    # insert into the table
    country_dim_insertion(upsert_list) 

get_standard_countries(std_country_filename)