# KML file parser

* Developer - Vishwajeet Shelar

This script is created to parse the kml file downloaded from Google Mymaps. It parses the kml file and returns a csv file with lat, lon rows

Things to keep in mind -
* It will only parse records which have co-ordinates(lat, lon), if you need to get lines, polygons, read the link given at the end

* Language - Python 2.7+

* The file required - kml_parser.py

## To run the tool - 
Execute below command in terminal:  

**python kml_parser.py kml_filename.kml csv_filename.csv**

Most of the code is taken from - http://programmingadvent.blogspot.com/2013/06/kmzkml-file-parsing-with-python.html  
Repurposed it as per my requirement
