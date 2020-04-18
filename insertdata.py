import psycopg2
import csv
import os
import sys, getopt
import  openDatabase

def insertData(reader, tablename, cursor):
    fieldNamesString = ",".join(reader.fieldnames)
    for row in reader:
        values = ",".join("'" + val + "'" for val in list(row.values()))
        sqlString = f"INSERT INTO {tablename} ({fieldNamesString}) VALUES ({values})"
        cursor.execute(f'''{sqlString}''')
    
 
