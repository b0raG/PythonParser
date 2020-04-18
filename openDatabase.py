import psycopg2
import os
import sys, getopt


def openConnection(argv):
    """
    Open the connection. 
    """ 
    try:
        opts, args = getopt.getopt(argv,"",["password="])
        for opt,arg in opts:
            if opt == '--password':
                password = arg

        try:
            conn = psycopg2.connect(
                database="gisdata", user='postgres', password=password, host='localhost', port= '5432'
            )
        except:
            print("Connection failed")
        return conn
    except Exception as e:
        print(e)
    

if __name__ == "__main__":
    openConnection(sys.argv[1:])