import os
import pymysql

from csv import reader
from pathlib import Path 

def upload_date(table_name: str="",csv_file_path: str="",full_upload: bool=False):
    '''
    Selects upload mode 
        full_upload = False  -> Uploads only differences
        full_upload = True   -> Clears tables and uploads everything again
    '''
    pass

def exec_n_fetchall(Connection_Obj, sql_cmd):
    '''
    Accepts connection object and SQL
    returns "fetchall" as result
    '''
    if not Connection_Obj and sql_cmd:
        raise ValueError('All arguments must contain values')
        return None

    with Connection_Obj.cursor() as cursor:
        cursor.execute(sql_cmd)
        return cursor.fetchall()

def exec_n_commit(Connection_Obj, sql_cmd):
    '''
    Accepts connection object and SQL cmd
    executes commands and commits to db
    returns None as result
    '''
    if not Connection_Obj and sql_cmd:
        raise ValueError('All arguments must contain values')
        return None

    with Connection_Obj.cursor() as cursor:
        cursor.execute(sql_cmd)
        Connection_Obj.commit()
        return None

def list_difference(list1, list2):

    list3 = list2.copy()
    for ind,item in enumerate(list3):
        if item in list1:
            list3.pop(ind)

    return list3


###################################################################
#
#           I N I T I A L I Z E    D A T A B A S E
#
###################################################################
#Create connection object with local DBMS
pyConector = pymysql.connect(
                host='localhost',
                user='root',
                passwd='DasWort9')

#Get existing DBs in server
sql_cmd = "SHOW DATABASES;"
results =   [item[0] for item in
            exec_n_fetchall(pyConector, sql_cmd)]

#If schema doesn't exist, create it
if not ("quotesscraper" in results):
    print("\nCreating QuotesScraper DB\n")
    exec_n_commit(pyConector, "CREATE DATABASE quotesscraper;")

#Change DB Connection Object. Add quotesscraper attribute.
#del pyConector
pyConector = pymysql.connect(
                host='localhost',
                user='root',
                passwd='DasWort9',
                database = "quotesscraper")

exec_n_commit(pyConector,"USE quotesscraper;")

#Get existing TABLES in QuotesScraper DataBase
results =   [item[0] for item in exec_n_fetchall(pyConector, "SHOW TABLES;")]

if "quotes" in results: 	
   exec_n_commit(pyConector," DROP TABLE quotes;")

if "authors" in results: 	
   exec_n_commit(pyConector," DROP TABLE authors;")

#Creates quotes table 
print("\nCreating 'quotes' table\n")
sql_cmd = """CREATE TABLE quotes (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
            quote TEXT NOT NULL, 
            author VARCHAR(30) NOT NULL, 
            tags VARCHAR(80) NULL, 
            link VARCHAR(60) NULL);"""
exec_n_commit(pyConector,sql_cmd)

#Creates authors table 
print("\nCreating 'authors' table\n")
sql_cmd = """CREATE TABLE authors (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            author VARCHAR(30) NOT NULL,
            country VARCHAR(40) NOT NULL,
            bdate VARCHAR(10) NOT NULL,
            bio TEXT NOT NULL);"""
exec_n_commit(pyConector,sql_cmd)

###################################################################
#
#     D A T A    M A N A G E M E N T    S T A R T S    H E R E
#
###################################################################

#===========================
# File and filepath handling
#===========================
#Get root folder from where DB_Handler.py is being run and add "\Files" to it
filesfolder = os.path.dirname(
                os.path.abspath(__file__)
                             ) + "\\Files"

#Create "Files" folder if it doesn't exist
if not Path(filesfolder).exists(): Path(filesfolder).mkdir(parents=True, exist_ok=True)

#Check if files are there
file_quotes = filesfolder + "\\Quotes.csv"
file_authors = filesfolder + "\\Authors.csv"
file_exists_quotes = Path(file_quotes).exists()
file_exists_authors = Path(file_authors).exists()

#====================================
# Finally, uploading some stuff, yay!
#====================================
tasks_thingy = dict(
        quotes= [file_exists_quotes,file_quotes],
        authors= [file_exists_authors,file_authors]
        )

for item in tasks_thingy:

    filepath = tasks_thingy[item][1]
    if not tasks_thingy[item][0]: 
        print(f"\nCouldn't find {filepath}...\ncontinuing with the rest of the files\n")
        continue  #If file doesn't exist, continue with the rest
    with open(filepath, 'r', newline='',encoding='utf-16') as file:
        header = next(reader(file))

        for row in reader(file):
            if item == 'quotes':
                sql_cmd = f"INSERT INTO {item} ({header[0]},{header[1]},{header[2]},{header[3]}) VALUES (\"{row[0]}\",'{row[1]}','{row[2]}','{row[3]}');"
            else:
                sql_cmd = f"INSERT INTO {item} ({header[0]},{header[1]},{header[2]},{header[3]}) VALUES ('{row[0]}','{row[1]}','{row[2]}',\"{row[3]}\");"

            exec_n_commit(pyConector,sql_cmd)

print("Databes uploading: Done")