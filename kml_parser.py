import xml.sax, xml.sax.handler
import csv
import sys
import os.path


class PlacemarkHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.inName = False # handle XML parser events
        self.inPlacemark = False
        self.mapping = {} 
        self.buffer = ""
        self.name_tag = ""
        self.counter = {}

    def startElement(self, name, attributes):
        
        if name == "Placemark": # on start Placemark tag
            self.inPlacemark = True
            self.buffer = "" 
        if self.inPlacemark:
            if name == "name": # on start title tag
                self.inName = True # save name text to follow

            
    def characters(self, data):
        
        if self.inPlacemark: # on text within tag
            self.buffer += data # save text if in title
            
    def endElement(self, name):

        self.buffer = self.buffer.strip('\n\t')

        if name == "Placemark":

            self.inPlacemark = False
            self.name_tag = "" #clear current name
            
        elif name == "name" and self.inPlacemark:
            
            self.inName = False # on end title tag 
            if self.buffer.strip() in self.counter.keys():
                self.counter[self.buffer.strip()] = self.counter[self.buffer.strip()] + 1
                self.name_tag = self.buffer.strip() + "_" + str(self.counter[self.buffer.strip()])
                self.mapping[self.name_tag] = {}
            else:
                self.name_tag = self.buffer.strip()
                self.mapping[self.name_tag] = {}
                self.counter[self.buffer.strip()] = 0

#             self.name_tag = self.buffer.strip()
#             self.mapping[self.name_tag] = {}

        elif self.inPlacemark:
 
            if name in self.mapping[self.name_tag]:
                self.mapping[self.name_tag][name] += self.buffer.strip()
            else:
                self.mapping[self.name_tag][name] = self.buffer.strip()
        self.buffer = ""

        
def read_kml(kml_file):
    try:
        kml = open(kml_file, 'r')
        parser = xml.sax.make_parser()
        handler = PlacemarkHandler()
        parser.setContentHandler(handler)
        parser.parse(kml)
        kml.close()
    except:
        return
    return handler.mapping


def parse_coordinates(val):
    if (val == None):
        print("Something is wrong! No data parsed")
        return 0
    elif len(val) == 0:
        print("Something is wrong! No data parsed")
        return 0
    
    entries = []
    for key in val:
        lon = val[key]['coordinates'].split(',')[:2][0]
        lat = val[key]['coordinates'].split(',')[:2][1]
#         row_format = (key, lat, lon) #Issues with ascii encoding in python 2.7 
        row_format = ("1", lat, lon)
        entries.append(row_format)
    return entries
    
    
def write_csv_file(entries, csv_file):
    try:
#         with open(csv_file, 'w', newline='') as f: #does not work with Python 2.7 
        with open(csv_file, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(entries)
        f.close()
        print("File is written successfully!")
    except Exception as e:
        print("Something is wrong! Unable to write csv\n" + str(e))
    return 0


def main(kml_file, csv_file):
    if not os.path.exists(kml_file):
        print("kml file not found")
        return 0
    kml_dict = read_kml(kml_file)
    coordinates_data = parse_coordinates(kml_dict)
    if coordinates_data == 0:
        return 0
    write_csv_file(coordinates_data, csv_file)
    return 0
    
    
if __name__ == '__main__':
    if (sys.argv is None) | (len(sys.argv) != 3):
        print("Expected command - python kml_parser.py [kml_file_name] [csv_file_name]")
        print("Terminating Program")
        exit()
    else:
        if not ((sys.argv[1].endswith('.kml')) & (sys.argv[2].endswith('.csv'))):
            print("Expected command - python kml_parser.py [kml_file_name ending in .kml] [csv_file_name ending in .csv]")
            print("Terminating Program")
            exit()
    ret = main(sys.argv[1], sys.argv[2])
    if ret == 0:
        print("Terminating Program")
        exit()