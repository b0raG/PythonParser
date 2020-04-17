import psycopg2
import csv
import os
import sys, getopt

def openConnection(password):
    #Establishing the connection
    try:
        conn = psycopg2.connect(
            database="gisdata", user='postgres', password=password, host='localhost', port= '5432'
        )
    except:
        print("Connection failed")
        
    return conn

def CSVReader(tableName):

    with open('data/CSV/' + tableName + '.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return reader.fieldnames

def createTableColumnsScript(tableName):
    fieldNames = CSVReader(tableName)
    sqlscript=''
    for fieldName in fieldNames:
        sqlscript += f'{fieldName.replace(" ", "_").replace("/","_")} VARCHAR(255),'
    sqlscript += "Geom geometry"
    return sqlscript

def createTable(tableName, conn):
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Doping table if already exists.21
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {tableName}")
    except Exception as e:
        print(e)


    #Creating table as per requirement
    sql =f'''CREATE TABLE {tableName}(
        {createTableColumnsScript(tableName)}
    )'''
    cursor.execute(sql)
    print(f"Table {tableName}created successfully........")

    #Closing the connection
    cursor.close()
    conn.commit()


def main(argv):
    """
    Open the CSV. 
    """ 
    try:
        opts, args = getopt.getopt(argv,"",["password="])
        for opt,arg in opts:
            if opt == '--password':
                password = arg

        conn = openConnection(password)
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