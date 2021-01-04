import arcpy
import os, time, datetime

FeatureClass = arcpy.GetParameterAsText(0)
ListOfFields = arcpy.GetParameterAsText(1)
ListOfFieldTypes = arcpy.GetParameterAsText(2)

arcpy.AddMessage(ListOfFields)
arcpy.AddMessage(ListOfFieldTypes)
WetlandTypesList = ListOfFieldTypes.split(";")
for i in WetlandTypesList:
    arcpy.AddMessage(i.replace("'",""))
arcpy.AddMessage(WetlandTypesList)

