'''
This class standardizes country names across all input files and provides country code as output
Country code is used in risks table as FK.
'''
import pandas as pd
from pandasql import sqldf
#from database_operations import get_standard_country_names_codes
#from database_operations import get_all_standard_country_names_codes
import csv
import openpyxl
from thefuzz import fuzz, process
from openai import OpenAI
from jproperties import Properties
import os

root_path = '/Users/sidpai/Desktop/Sem_2'
os.chdir(root_path)

#root_path = os.environ.get("HOME")
#os.chdir(root_path)

properties_filename = 'EUDR_MTP/Training/credentials.properties'
configs = Properties()
with open(properties_filename, 'rb') as config_file:
    configs.load(config_file)
client = OpenAI(api_key=configs.get("open_api_key").data,)

def get_standard_country_codes(lis):
    sys_msg = "Provide 2 character official code for the countries=" + ','.join(lis) + ". Provide no explanation and only output as a list of comma separated codes."
    completion = client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role": "system", "content": sys_msg}])
    result = completion.choices[0].message.content.split(",")
    return result

# input is list of tuples of risk scores per year, country for a specific category
def standardize(vals_list):
    country_list = []
    # extract country column index
    sys_msg = "Provided list of values. Give index which denotes country names. Provide no explanation and only single output integer:" + str(vals_list[-1])
    completion = client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role": "system", "content": sys_msg}])
    result = completion.choices[0].message.content.split(",")
    country_index = int(result[0])

    # extract countries
    for i in range(len(vals_list)):
        country_list.append(vals_list[i][country_index].replace(',',''))

    # Modify vals_list to include country_code instead of country
    res = get_standard_country_codes(country_list)
    return_list = []
    #print(len(res))
    #print(country_list)
    # Replace country with code fetched from LLM
    for i in range(len(vals_list)):
        tup_lis = list(vals_list[i])
        tup_lis[country_index] = res[i].strip()
        return_list.append(tuple(tup_lis))
    return return_list