import os
from arcpy import env
import arcpy
import datetime
import csv

# set workspace to the folder where the
path = r"E:\Dropbox (RES)\@RES GIS\projects\CA\Domain\GDB"

# get projections to use
prj10 = arcpy.Describe(r"C:\Users\jtouzel\Documents\ArcGIS\Templates.gdb\Point").spatialReference

# Get the names of all the properties
DomainBanksCSV = r"C:\Users\jtouzel\Desktop\PythonTempOutput\DomainBanks.csv"
with open(DomainBanksCSV, 'r') as f:
    reader = csv.reader(f)
    DomainBanksList2 = list(reader)

DomainBanksList = DomainBanksList2[0]
DomainBanksList[1]

# Create a new geodatabase for each Domain Bank
GDBPathsList = []
for i in DomainBanksList:
    GDBPathsList.append(os.path.join(path, i + "Collector_Field.gdb"))
    arcpy.CreateFileGDB_management(path, i + "Collector_Field.gdb")
    print(i + "Collector_Field.gdb")

# For each Geodatabase create a line, point, and polygon layer
LineTemplate = r"E:\Dropbox (RES)\@RES GIS\projects\CA\Domain\GDB\PajaroCollector_Field.gdb\Line"
PolygonTemplate = r"E:\Dropbox (RES)\@RES GIS\projects\CA\Domain\GDB\PajaroCollector_Field.gdb\Polygon"
PointTemplate = r"C:\Users\jtouzel\Documents\ArcGIS\Templates.gdb\Point"
has_m = "DISABLED"
has_z = "DISABLED"

for i in GDBPathsList:
    arcpy.CreateFeatureclass_management(GDBPathsList[0],"Point", "POINT", PointTemplate, has_m, has_z, prj10)
    print(i)



