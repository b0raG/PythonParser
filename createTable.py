import psycopg2
import csv
import os
import sys, getopt
import  openDatabase



def createTableColumnsScript(fieldNames):
    sqlscript=''
    for fieldName in fieldNames:
        sqlscript += f'{fieldName.replace(" ", "_").replace("/","_")} VARCHAR(5000000),'
    sqlscript += "Geom geometry"
    return sqlscript

def insertData(reader, tablename, cursor):
    fieldNamesString = ",".join( val.replace(" ", "_").replace("/","_")  for val in reader.fieldnames)
    for row in reader:
        values = ",".join("'" + val + "'" for val in list(row.values()))
        sqlString = f"INSERT INTO {tablename} ({fieldNamesString}) VALUES ({values})"
        cursor.execute(f'''{sqlString}''')
       

def createTable(tableName, conn):
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Doping table if already exists.21
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {tableName}")
        conn.commit()
    except Exception as e:
        print(e)
    with open('data/CSV/' + tableName + '.csv', 'r', newline='', encoding='utf-8') as csvfile:
        csv.field_size_limit(sys.maxsize)
        reader = csv.DictReader(csvfile)

        #Creating table as per requirement
        sql =f'''CREATE TABLE {tableName}(
            {createTableColumnsScript(reader.fieldnames)}
        )'''
        cursor.execute(sql)
        conn.commit()
        print(f"Table {tableName}created successfully........")

        insertData(reader,tableName,cursor)
        #Closing the connection
        cursor.close()
        conn.commit()


def main(argv):
    """
    Open the CSV. 
    """ 
    try:
        conn = openDatabase.openConnection(argv)
        for filename in os.listdir('data/CSV'):
            if filename.endswith(".csv"): 
                createTable(filename.replace('.csv',''),conn)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        print("g")
    

if __name__ == "__main__":
    main(sys.argv[1:])