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

category_name = 'employee_rights'
source_name = 'globalrightsindex employee rights'
# Get the category ID for corruption risk
source_id = get_risk_source_id(source_name)
category_id = get_risk_category_id(category_name)

# update category_id and category_name in eudr.risk_sources
update_category_values(source_id, category_id, category_name)

year = str(datetime.date.today().year - 1)
filename = 'EUDR_MTP/Datasets/employee_rights_'+year+'.pdf'
if len(sys.argv) == 3:
    year = sys.argv[1]
    filename = sys.argv[2]

pdfFileObj = open(filename, 'rb')
pdfReader = PyPDF2.PdfReader(pdfFileObj)

# denotes starting and ending page in the pdf consisting of country indices
start = 16
end = 17
emp = ""
for i in range(start-1,end):
    emp = emp + pdfReader.pages[i].extract_text()

#ratings_list = emp.replace('\n',';').split('Rating')
ratings_list = emp.split('Rating')
del ratings_list[0]
lis = ['5+','5','4','3','2','1']
emp_rights_dict = {}
for i in range(len(lis)):
    #sys_msg = "Name the countries with " + lis[i] + " Rating in comma separated way. Do not provide explanations and sentences"
    sys_msg = "Name the countries listed in the text in comma separated way. Do not provide explanations and sentences"
    completion = client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role": "system", "content": sys_msg},{"role": "user", "content":ratings_list[i]}])
    # Gets country names with score = i
    result = completion.choices[0].message.content.split(",")
    emp_rights_dict[lis[i]] = result

# Replace 5+ with 6 as our risk score ranges between 1 and 6
emp_rights_dict['6'] = emp_rights_dict['5+']
emp_rights_dict.pop('5+')

# Convert dict to list of country_name and score as list of tuples
vals_list = []
for i in range(len(emp_rights_dict)):
    country_list = emp_rights_dict[str(i+1)]
    for j in country_list:
        risk = i+1
        country = j
        description = "The risk score for " + country + " is pre-calculated in the source file."
        vals_list.append((source_id, category_id, year, country, risk, description, risk, description))

# Get standard country names and upsert into eudr.risks table
upsert_list = standardize(vals_list)
risks_table_operations(upsert_list)