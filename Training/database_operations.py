'''
This class has all database operations being carried out.
These functions are called from other classes
'''
import psycopg2
from jproperties import Properties
import os

# Read credentials.properties and fetch values

root_path = '/Users/sidpai/Desktop/Sem_2'
os.chdir(root_path)

#root_path = os.environ.get("HOME")
#os.chdir(root_path)

properties_filename = 'EUDR_MTP/Training/credentials.properties'
configs = Properties()
with open(properties_filename, 'rb') as config_file:
    configs.load(config_file)

host = configs.get("host").data
database = configs.get("database").data
user = configs.get("user").data
password = configs.get("password").data
port = configs.get("port").data

def get_risk_source_id(source_name):
    connection = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
    cursor = connection.cursor()
    query = """SELECT source_id from eudr.risk_sources WHERE source_name = %s;"""
    cursor.execute(query,[source_name])
    source_id = cursor.fetchall()[0][0]
    connection.commit()
    cursor.close()
    connection.close()
    return source_id

def get_risk_category_id(category_name):
    connection = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
    cursor = connection.cursor()
    query = """SELECT category_id from eudr.risk_categories WHERE category_name = %s;"""
    #cursor.execute(query,list(category_name.split()))
    cursor.execute(query,[category_name])
    category_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return category_id

def get_commodity_id(commodity_name):
    connection = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
    cursor = connection.cursor()
    query = """SELECT commodity_id from eudr.commodities WHERE commodity_name = %s;"""
    cursor.execute(query,[commodity_name])
    commodity_id = cursor.fetchall()[0][0]
    connection.commit()
    cursor.close()
    connection.close()
    return commodity_id

def update_category_values(source_id,category_id,category_name):
    connection = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
    cursor = connection.cursor()
    query = """UPDATE eudr.risk_sources SET
                category_id = %s,
                category_name = %s
                WHERE source_id = %s"""
    #cursor.execute(query,list(category_name.split()))
    cursor.executemany(query,[(category_id,category_name,source_id)])
    connection.commit()
    cursor.close()
    connection.close()
    print("Updated category_id and category_name")

def risks_table_operations(lis):
    connection = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
    cursor = connection.cursor()
    query = """INSERT INTO eudr.risks
            (
                risk_source_id,
                risk_category_id,
                year,
                country_code,
                risk_score,
                description           
            ) VALUES
            (%s,%s,%s,%s,%s,%s)
            ON CONFLICT (risk_source_id,risk_category_id,year,country_code)
            DO UPDATE SET
            risk_score = %s,
            description = %s,
            last_updated = now();"""
    cursor.executemany(query,lis)
    connection.commit()
    cursor.close()
    connection.close()
    print(cursor.rowcount, "Record upserted successfully into eudr.risks table")

def commodity_risks_table_operations(lis):
    connection = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
    cursor = connection.cursor()
    query = """INSERT INTO eudr.commodity_risks
            (
                commodity_id,
                risk_source_id,
                risk_category_id,
                year,
                country_code,
                region,
                risk_score,
                description        
            ) VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (commodity_id,risk_source_id,risk_category_id,year,country_code,region)
            DO UPDATE SET
            risk_score = %s,
            description = %s,
            last_updated = now();"""
    cursor.executemany(query,lis)
    connection.commit()
    cursor.close()
    connection.close()
    print(cursor.rowcount, "Record upserted successfully into eudr.commodity_risks table")

def exporter_agreements_table_operations(lis):
    connection = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
    cursor = connection.cursor()
    query = """INSERT INTO eudr.exporter_agreements
            (
                commodity_id,
                country_code,
                agreement,
                exporter      
            ) VALUES
            (%s,%s,%s,%s)
            ON CONFLICT (commodity_id,country_code,exporter)
            DO UPDATE SET
            agreement = %s,
            last_updated = now();"""
    cursor.executemany(query,lis)
    connection.commit()
    cursor.close()
    connection.close()
    print(cursor.rowcount, "Record upserted successfully into eudr.exporter_agreements table")

def country_dim_insertion(lis):
    connection = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
    cursor = connection.cursor()
    query = """INSERT INTO eudr.standard_country_dimension
            (
                standard_country_name, 
                country_code
            )
            VALUES 
            (%s,%s) 
            ON CONFLICT (country_code) 
            DO UPDATE SET
            standard_country_name=%s,
            last_updated=now();"""
    cursor.executemany(query,lis)
    connection.commit()
    cursor.close()
    connection.close()
    print(cursor.rowcount, "Record upserted successfully into eudr.standard_country_dimension table")

def forest_coordinates_insertion(lis,year):
    connection = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)
    cursor = connection.cursor()
    query1 = """DELETE FROM eudr.forest_coordinates where year = {};""".format(year)
    query2 = """INSERT INTO eudr.forest_coordinates
            (
                year, 
                centroid_longitude,
                centroid_latitude,
                radius
            )
            VALUES 
            (%s,%s,%s,%s);
            """
    cursor.execute(query1)
    connection.commit()
    cursor.executemany(query2,lis)
    connection.commit()
    cursor.close()
    connection.close()
    print(cursor.rowcount, "Record inserted successfully into eudr.forest_coordinates table")

'''
def customer_dim_insertion()
Happens via Java code because this table gets rows inserted when customer tries the risk evaluation software
'''