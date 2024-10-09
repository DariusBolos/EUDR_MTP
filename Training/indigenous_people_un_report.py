import sys
import pandas as pd
import datetime
import psycopg2
import PyPDF2
from openai import OpenAI
from database_operations import get_risk_source_id
from database_operations import get_risk_category_id
from database_operations import risks_table_operations
from database_operations import update_category_values
from country_standard import standardize
import os
from jproperties import Properties

root_path = '/Users/sidpai/Desktop/Sem_2'
os.chdir(root_path)

#root_path = os.environ.get("HOME")
#os.chdir(root_path)

properties_filename = 'EUDR_MTP/Training/credentials.properties'
configs = Properties()
with open(properties_filename, 'rb') as config_file:
    configs.load(config_file)

client = OpenAI(api_key=configs.get("open_api_key").data,)

category_name = 'indigenous_people'
source_name = 'United Nations report for indigenous people rights'
# Get the category ID for rights of indigenous people risk
category_id = get_risk_category_id(category_name)
source_id = get_risk_source_id(source_name)

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Indigenous rights risk report available for year 2014, not a periodic report
year = str(datetime.date.today().year - 1)
filename = "EUDR_MTP/Datasets/indigenous_people_report_UN.pdf"
if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

pdfFileObj = open(filename, 'rb')
pdfReader = PyPDF2.PdfReader(pdfFileObj)
pages = len(pdfReader.pages)

# read all content into a variable
ind = ""
for p in range(pages):
    ind = ind + pdfReader.pages[p].extract_text()

sys_msg = "Provide a list of countries mentioned in this text. Dont provide any explanations and only output comma separated list of ISO approved country names."
completion = client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role": "system", "content": sys_msg},{"role": "user", "content":ind}])
countries_list = completion.choices[0].message.content.split(",")
vals_list = []
for country in countries_list:
    sys_msg = f"Assess the risk score for the rights of indigenous people for country = {country}, mentioned in this extract. Assess the score on a scale from 1 to 6, with 6 being the highest risk. Provide the answer in the following format: country name, risk score, one sentence description without comma and quotes of the risk assessment. Example: Germany, 1, There are no indigenous people in Germany. Provide no additional explanations or remarks, only a list of countries with the risk scores and descriptions."
    completion = client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role": "system", "content": sys_msg},{"role": "user", "content":ind}])
    out_list = completion.choices[0].message.content.split(",")
    country = out_list[0].strip()
    risk = round(float(out_list[1].strip()),1)
    desc = ' '.join(out_list[2:]).strip()
    vals_list.append((source_id, category_id, int(year), country, risk, desc, risk, desc))

# change country name to country code and then insert into risks table
upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)