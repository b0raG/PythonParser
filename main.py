from shutil import copyfile
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
from lxml import etree
import os
import zipfile
import shutil
from pykml import parser


class Temaxio(object):
    Name = ""
    FEATUREID = ""
    SBPI_ID_NO = ""
    ΚΩΔΙΚΟΣ_ΕΠΑΡΧΙΑΣ = ""
    ΚΩΔΙΚΟΣ_ΔΗΜΟΥ_ΚΟΙΝΟΤΗΤΑΣ = ""
    ΚΩΔΙΚΟΣ_ΕΝΟΡΙΑΣ = ""
    ΚΩΔΙΚΟΣ_ΤΜΗΜΑΤΟΣ = ""
    ΦΥΛΛΟ = ""
    ΣΧΕΔΙΟ = ""
    ΑΡΙΘΜΟΣ_ΤΕΜΑΧΙΟΥ = ""
    SRC_SL_CODE = ""
    ΠΗΓΗ = ""
    ΕΜΒΑΔΟ_ΤΕΜΑΧΙΟΥ = ""
    coordinates= ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, name):
        self.Name = name


def CSVImporter(items, file):

    with open('data/CSV/' + file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name','FEATUREID','SBPI_ID_NO','ΚΩΔΙΚΟΣ_ΕΠΑΡΧΙΑΣ','ΚΩΔΙΚΟΣ_ΔΗΜΟΥ_ΚΟΙΝΟΤΗΤΑΣ','ΚΩΔΙΚΟΣ_ΕΝΟΡΙΑΣ','ΚΩΔΙΚΟΣ_ΤΜΗΜΑΤΟΣ','ΦΥΛΛΟ','ΣΧΕΔΙΟ','ΑΡΙΘΜΟΣ_ΤΕΜΑΧΙΟΥ','SRC_SL_CODE','ΠΗΓΗ','ΕΜΒΑΔΟ_ΤΕΜΑΧΙΟΥ','coordinates']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for temaxio in items:
            writer.writerow({'Name': temaxio.Name, 'FEATUREID': temaxio.FEATUREID, 'SBPI_ID_NO': temaxio.SBPI_ID_NO, 'ΚΩΔΙΚΟΣ_ΕΠΑΡΧΙΑΣ': temaxio.ΚΩΔΙΚΟΣ_ΕΠΑΡΧΙΑΣ, 'ΚΩΔΙΚΟΣ_ΔΗΜΟΥ_ΚΟΙΝΟΤΗΤΑΣ': temaxio.ΚΩΔΙΚΟΣ_ΔΗΜΟΥ_ΚΟΙΝΟΤΗΤΑΣ, 'ΚΩΔΙΚΟΣ_ΕΝΟΡΙΑΣ': temaxio.ΚΩΔΙΚΟΣ_ΕΝΟΡΙΑΣ, 'ΚΩΔΙΚΟΣ_ΤΜΗΜΑΤΟΣ': temaxio.ΚΩΔΙΚΟΣ_ΤΜΗΜΑΤΟΣ, 'ΦΥΛΛΟ': temaxio.ΦΥΛΛΟ, 'ΣΧΕΔΙΟ': temaxio.ΣΧΕΔΙΟ, 'ΑΡΙΘΜΟΣ_ΤΕΜΑΧΙΟΥ': temaxio.ΑΡΙΘΜΟΣ_ΤΕΜΑΧΙΟΥ, 'SRC_SL_CODE': temaxio.SRC_SL_CODE, 'ΠΗΓΗ': temaxio.ΠΗΓΗ, 'ΕΜΒΑΔΟ_ΤΕΜΑΧΙΟΥ': temaxio.ΕΜΒΑΔΟ_ΤΕΜΑΧΙΟΥ, 'coordinates': temaxio.coordinates})

def copyKMZandrenametoZIP(filename):
    sourceFile = "data/KMZ/" + filename
    targetFile = 'data/ZIP/'+filename
    if (os.path.isdir('data/ZIP/') == False):
        os.makedirs('data/ZIP/')
    copyfile(sourceFile,targetFile )
    base = os.path.splitext(targetFile)[0]
    os.rename(targetFile, base + ".zip")
    return base + ".zip"

def unzipFile(filepath, file):
    targetPath='data/UNZIP/'
    targetFile = targetPath + file + '/doc.kml'
    if (os.path.isdir(targetPath) == False):
        os.makedirs(targetPath)
    if (os.path.isdir(targetPath+file) == False):
        os.makedirs(targetPath+file)
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(targetPath+file)
    #base = os.path.splitext(targetFile)[0]
    #os.rename(targetFile, base + ".xml")
    return  targetFile #base + ".xml"

def deleteCreated():
    shutil.rmtree("data/ZIP")
    shutil.rmtree('data/UNZIP')

def Parser(docxml):
    temaxia = []
    #tree = ET.parse(docxml)
    with open(docxml, encoding='utf-8') as f:
        doc = parser.parse(f)
        root = doc.getroot()   
        for placemark in root.Document.Folder.Placemark:
            temaxio = Temaxio(placemark.name)
            temaxio.coordinates = (placemark.MultiGeometry.Polygon.outerBoundaryIs.LinearRing.coordinates)

            desc = placemark.description.text
            table = etree.HTML(desc).find("body/table/tr/td/table")
            rows = iter(table)
            for row in rows:
                values = [col.text for col in row]
                if (len(values) == 2):
                    if (values[0] == 'FEATUREID'):
                        temaxio.FEATUREID = values[1]
                        
                    elif (values[0] == 'SBPI_ID_NO'):
                        temaxio.SBPI_ID_NO = values[1]
                        
                    elif (values[0] == 'ΚΩΔΙΚΟΣ ΕΠΑΡΧΙΑΣ'):
                        temaxio.ΚΩΔΙΚΟΣ_ΕΠΑΡΧΙΑΣ = values[1]
                        
                    elif (values[0] == 'ΚΩΔΙΚΟΣ ΔΗΜΟΥ_ΚΟΙΝΟΤΗΤΑΣ'):
                        temaxio.ΚΩΔΙΚΟΣ_ΔΗΜΟΥ_ΚΟΙΝΟΤΗΤΑΣ = values[1]
                        
                    elif (values[0] == 'ΚΩΔΙΚΟΣ ΕΝΟΡΙΑΣ'):
                        temaxio.ΚΩΔΙΚΟΣ_ΕΝΟΡΙΑΣ = values[1]
                        
                    elif (values[0] == 'ΚΩΔΙΚΟΣ ΤΜΗΜΑΤΟΣ'):
                        temaxio.ΚΩΔΙΚΟΣ_ΤΜΗΜΑΤΟΣ = values[1]
                        
                    elif (values[0] == 'ΦΥΛΛΟ'):
                        temaxio.ΦΥΛΛΟ = values[1]
                        
                    elif (values[0] == 'ΣΧΕΔΙΟ'):
                        temaxio.ΣΧΕΔΙΟ = values[1]
                        
                    elif (values[0] == 'ΑΡΙΘΜΟΣ ΤΕΜΑΧΙΟΥ'):
                        temaxio.ΑΡΙΘΜΟΣ_ΤΕΜΑΧΙΟΥ = values[1]
                        
                    elif (values[0] == 'SRC_SL_CODE'):
                        temaxio.SRC_SL_CODE = values[1]
                        
                    elif (values[0] == 'ΠΗΓΗ'):
                        temaxio.ΠΗΓΗ = values[1]
                        
                    elif (values[0] == 'ΕΜΒΑΔΟ ΤΕΜΑΧΙΟΥ'):
                        temaxio.ΕΜΒΑΔΟ_ΤΕΜΑΧΙΟΥ = values[1]
            temaxia.append(temaxio)
        return temaxia

def main():
    """
    Open the KML. Read the KML. Open a CSV file. Process a coordinate string to be a CSV row.
    """ 
    #file = 'ΤΕΜΑΧΙΑ_0'
  #  file = 'ΚΤΗΡΙΑΓΚΒΔ_17'
    try:
        for filename in os.listdir('data/KMZ'):
            if filename.endswith(".kmz"): 
                zipefile = copyKMZandrenametoZIP(filename)
              #  docxml = unzipFile(zipefile, filename)
      #  temaxia = Parser(docxml)
      #  CSVImporter(temaxia,file + '.csv')
    finally:
       # deleteCreated()
       print("g")
    

if __name__ == "__main__":
    main()