#### We're going to check all these geodatabases, get the point layer, add a lat and a long field, then calc the lat and longs
import os
from arcpy import env
import arcpy
import datetime
import time

###### Get date for tagging our output files ######
dateTag = datetime.datetime.today().strftime('%Y%m%d') # looks somethin like this 20181213

###### Get the folder path for all our stuff ######
MotherShipFolder = r"C:/Users/jtouzel/Downloads/DomainFieldDataDownload"
calcCS = r"C:/Users/jtouzel/AppData/Roaming/Esri/Desktop10.6/ArcMap/Coordinate Systems/WGS 1984.prj"
folderlist = [] # Create empty list for all the sub-folder paths
for i in os.listdir(MotherShipFolder): # get a list of all the sub-folders
    folderlist.append(MotherShipFolder + "/" + i)
for i in folderlist: # get into each sub-folder
    for n in os.listdir(i):# get the geodatabase out of the sub-folder
        if n.endswith('.gdb'):
            env.workspace = os.path.join(i,n) # set the gdb as the workspace
            for fc in arcpy.ListFeatureClasses(): # find the point layer
                desc = arcpy.Describe(fc) # first let's check if there's lat and long fields
                flds = desc.fields
                for fld in flds: # if they are there we need to delete them
                    if fld == "LAT":
                        arcpy.Delete_management(fc, ["LAT", "LONG"])
                # add the fields back in and calculate them
                arcpy.AddField_management(fc, "LAT", "DOUBLE")
                arcpy.AddField_management(fc, "LONG", "DOUBLE")
                arcpy.env.outputCoordinateSystem = calcCS # set the output coordinate system so we can actually get lat long coords
                arcpy.CalculateGeometryAttributes_management(fc, [["LAT", "POINT_Y"],["LONG", "POINT_X"]])
