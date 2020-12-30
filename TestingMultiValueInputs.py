import arcpy
import os, time, datetime

ListOfFields = arcpy.GetParameterAsText(0)

arcpy.AddMessage(ListOfFields)