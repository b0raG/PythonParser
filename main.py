from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
from html.parser import HTMLParser
from lxml import etree
import csv


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


def CSVImporter(temaxia):

    with open('temaxia.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name','FEATUREID','SBPI_ID_NO','ΚΩΔΙΚΟΣ_ΕΠΑΡΧΙΑΣ','ΚΩΔΙΚΟΣ_ΔΗΜΟΥ_ΚΟΙΝΟΤΗΤΑΣ','ΚΩΔΙΚΟΣ_ΕΝΟΡΙΑΣ','ΚΩΔΙΚΟΣ_ΤΜΗΜΑΤΟΣ','ΦΥΛΛΟ','ΣΧΕΔΙΟ','ΑΡΙΘΜΟΣ_ΤΕΜΑΧΙΟΥ','SRC_SL_CODE','ΠΗΓΗ','ΕΜΒΑΔΟ_ΤΕΜΑΧΙΟΥ','coordinates']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for temaxio in temaxia:
            writer.writerow({'Name': temaxio.Name, 'FEATUREID': temaxio.FEATUREID, 'SBPI_ID_NO': temaxio.SBPI_ID_NO, 'ΚΩΔΙΚΟΣ_ΕΠΑΡΧΙΑΣ': temaxio.ΚΩΔΙΚΟΣ_ΕΠΑΡΧΙΑΣ, 'ΚΩΔΙΚΟΣ_ΔΗΜΟΥ_ΚΟΙΝΟΤΗΤΑΣ': temaxio.ΚΩΔΙΚΟΣ_ΔΗΜΟΥ_ΚΟΙΝΟΤΗΤΑΣ, 'ΚΩΔΙΚΟΣ_ΕΝΟΡΙΑΣ': temaxio.ΚΩΔΙΚΟΣ_ΕΝΟΡΙΑΣ, 'ΚΩΔΙΚΟΣ_ΤΜΗΜΑΤΟΣ': temaxio.ΚΩΔΙΚΟΣ_ΤΜΗΜΑΤΟΣ, 'ΦΥΛΛΟ': temaxio.ΦΥΛΛΟ, 'ΣΧΕΔΙΟ': temaxio.ΣΧΕΔΙΟ, 'ΑΡΙΘΜΟΣ_ΤΕΜΑΧΙΟΥ': temaxio.ΑΡΙΘΜΟΣ_ΤΕΜΑΧΙΟΥ, 'SRC_SL_CODE': temaxio.SRC_SL_CODE, 'ΠΗΓΗ': temaxio.ΠΗΓΗ, 'ΕΜΒΑΔΟ_ΤΕΜΑΧΙΟΥ': temaxio.ΕΜΒΑΔΟ_ΤΕΜΑΧΙΟΥ, 'coordinates': temaxio.coordinates})

def main():
    """
    Open the KML. Read the KML. Open a CSV file. Process a coordinate string to be a CSV row.
    """ 
    temaxia = []
    tree = ET.parse('doc.xml')
    root = tree.getroot()
    for folder in root.iter('Folder'):
        for placemark in folder.iter('Placemark'):
            print(placemark.find('name').text)
            temaxio = Temaxio(placemark.find('name').text)
            for geometry in placemark.iter('MultiGeometry'):
                for polygon in geometry.iter('Polygon'):
                    for outerB in polygon.iter('outerBoundaryIs'):
                        for ring in outerB.iter('LinearRing'):
                            for coord in ring.iter('coordinates'):
                                temaxio.coordinates = (coord.text)

            desc = placemark.find('description').text
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
    CSVImporter(temaxia)
                


if __name__ == "__main__":
    main()