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
source_name = 'mahb.stanford.edu indigenous rights risk report'
# Get the category ID for rights of indigenous people risk
category_id = get_risk_category_id(category_name)
source_id = get_risk_source_id(source_name)

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

# Indigenous rights risk report available for year 2014, not a periodic report
year = str(datetime.date.today().year - 1)
filename = "EUDR_MTP/Datasets/indigenous_people_" + year + ".pdf"
if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

pdfFileObj = open(filename, 'rb')
pdfReader = PyPDF2.PdfReader(pdfFileObj)

# page containing the country risk is p.25
page = 24
ind = pdfReader.pages[page].extract_text()
sys_msg = "Provide a list of comma separated and without quotes country wise risk scores from the following text in this format: Country-Score. Every row should be delimited by a \n. Do not provide any explanations and comments"
completion = client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role": "system", "content": sys_msg},{"role": "user", "content":ind}])
result = completion.choices[0].message.content.split(",")

# result has comma separated list of country-score
max1 = 5
min1 = 1
max2 = 6
min2 = 1
a = (max2-min2)/(max1-min1)
b = max2 - a*max1
vals_list = []
for row in result:
    s = row.strip().split('-')
    country = s[0]
    rs = float(s[1])
    risk = round(a*rs + b,1)
    desc = "The pre calculated Risk Score " + country + " is " + str(rs) + " (Min-1 and Max-5). This score is normalised on a risk scale between 1(best) and 6(worst)."
    vals_list.append((source_id, category_id, int(year), country, risk, desc, risk, desc))

upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)