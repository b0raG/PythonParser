from shutil import copyfile
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
from lxml import etree
import os
import zipfile
import shutil
from pykml import parser

def CSVImporter(items, file):

    with open('data/CSV/' + file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(items[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for temaxio in items:
            writer.writerow(temaxio)


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
    items = []
    #tree = ET.parse(docxml)
    with open(docxml, encoding='utf-8') as f:
        doc = parser.parse(f)
        root = doc.getroot()   
        for placemark in root.Document.Folder.Placemark:
            item = {}
            item["Name"] = placemark.name
            try:
                item["coordinates"] ='<MultiGeometry><Polygon><outerBoundaryIs><LinearRing><coordinates>' + placemark.MultiGeometry.Polygon.outerBoundaryIs.LinearRing.coordinates + '</coordinates></LinearRing></outerBoundaryIs></Polygon></MultiGeometry>'
            except:
                try:
                    item["coordinates"] = (
                    '<Point><coordinates>' + 
                    placemark.Point.coordinates + 
                    '</coordinates></Point>')
                except:
                    item["coordinates"] = (
                    '<MultiGeometry><LinearString><coordinates>' + 
                    placemark.MultiGeometry.LineString.coordinates +
                    '</coordinates></LinearString></MultiGeometry>')

            desc = placemark.description.text
            table = etree.HTML(desc).find("body/table/tr/td/table")
            rows = iter(table)
            for row in rows:
                values = [col.text for col in row]
                if (len(values) == 2):
                    item[values[0]] = values[1]
     
            items.append(item)
        return items

def main():
    """
    Open the KML. Read the KML. Open a CSV file. Process a coordinate string to be a CSV row.
    """ 
    try:
         for filename in os.listdir('data/KMZ'):
             if filename.endswith(".kmz"): 
                zipefile = copyKMZandrenametoZIP(filename)
                docxml = unzipFile(zipefile, filename)
                temaxia = Parser(docxml)
                base = os.path.splitext(filename)[0]
                CSVImporter(temaxia,base + '.csv')
    finally:
       deleteCreated()
       print("g")
    

if __name__ == "__main__":
    main()