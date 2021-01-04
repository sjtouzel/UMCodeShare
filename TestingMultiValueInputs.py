import arcpy
import os, time, datetime

FeatureClass = arcpy.GetParameterAsText(0)
ListOfFields = arcpy.GetParameterAsText(1)
ListOfFieldTypes = arcpy.GetParameterAsText(2)

arcpy.AddMessage(ListOfFields)
arcpy.AddMessage(ListOfFieldTypes)
for i in ListOfFieldTypes:
    arcpy.AddMessage(i.replace("'",""))

