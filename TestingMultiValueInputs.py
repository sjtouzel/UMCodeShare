import arcpy
import os, time, datetime

FeatureClass = arcpy.GetParameterAsText(0)
ListOfFields = arcpy.GetParameterAsText(1)

arcpy.AddMessage(ListOfFields)