import arcpy
import os, time, datetime

FeatureClass = arcpy.GetParameterAsText(0)
ListOfFields = arcpy.GetParameterAsText(1)
ListOfFieldTypes = arcpy.GetParameterAsText(2)

arcpy.AddMessage(ListOfFields)
arcpy.AddMessage(ListOfFieldTypes)
WetlandTypesList = ListOfFieldTypes.split(";")
NewList = []
for i in WetlandTypesList:
    NewList.append("'" + i.replace("'","") + "'")
arcpy.AddMessage(NewList)
# QuoteList = []
# for i in NewList:
#     QuoteList.append("'" + i + "'")
TypeListConcat = ",".join(NewList)
NWI_Query = '"' + ListOfFields + '"' + " NOT IN (" + TypeListConcat + ")" # create the query
arcpy.AddMessage('Query is: {}'.format(NWI_Query))

