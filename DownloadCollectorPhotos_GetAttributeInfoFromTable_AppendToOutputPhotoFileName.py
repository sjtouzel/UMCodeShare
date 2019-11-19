import arcpy
from arcpy import da
from arcpy import env
import os

MotherShipFolder = r"C:/Users/jtouzel/Downloads/DomainFieldDataDownload"
folderlist = [] # Create empty list for all the sub-folder paths
for i in os.listdir(MotherShipFolder): # get a list of all the sub-folders
    folderlist.append(MotherShipFolder + "/" + i)
for i in folderlist: # get into each sub-folder
    for n in os.listdir(i):# get the geodatabase out of the sub-folder
        if n.endswith('.gdb'):
            env.workspace = os.path.join(i,n) # set the gdb as the workspace
            for table in arcpy.ListTables():
                with da.SearchCursor(table, ['DATA', 'ATT_NAME', 'REL_GLOBALID']) as cursor:
                    count = 0
                    for item in cursor:
                        attachment = item[0]
                        fcList = arcpy.ListFeatureClasses()
                        with arcpy.da.SearchCursor(fcList[0], ["COMMENT", "PHOTO_DIRECTION"], "{0} = '{1}'".format("GlobalID", item[2])) as cursor2:
                            for row2 in cursor2:
                                PhotoComment = str(row2[0])
                                photoname = PhotoComment.replace(" ", "_") + "_" + str(row2[1]) + "_"
                        filename = photoname + str(item[1])
                        print(filename)
                        open(os.path.join(i, filename), 'wb').write(attachment.tobytes())
                        del item
                        del filename
                        del attachment
                        count += 1