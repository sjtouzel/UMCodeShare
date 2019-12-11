import arcpy
from arcpy import da
from arcpy import env
import os

MotherShipFolder = r"C:/Users/jtouzel/Downloads/DomainFieldDataDownload" # All our downloaded data is here
folderlist = [] # Create empty list for all the sub-folder paths
for i in os.listdir(MotherShipFolder): # get a list of all the sub-folders
    folderlist.append(MotherShipFolder + "/" + i)
for i in folderlist: # get into each sub-folder
    for n in os.listdir(i):# get the geodatabase out of the sub-folder
        if n.endswith('.gdb'):
            env.workspace = os.path.join(i,n) # set the gdb as the workspace
            for table in arcpy.ListTables(): # get the attachments table
                with da.SearchCursor(table, ['DATA', 'ATT_NAME', 'REL_GLOBALID']) as cursor: # get this data from each row
                    count = 0
                    for item in cursor:
                        attachment = item[0] # get the blob
                        fcList = arcpy.ListFeatureClasses() # get a list of feature classes
                        with arcpy.da.SearchCursor(fcList[0], ["COMMENT", "PHOTO_DIRECTION"], "{0} = '{1}'".format("GlobalID", item[2])) as cursor2: # look through point FC to get
                                                                                                                                                    # the related info for each photo
                            for row2 in cursor2:
                                PhotoComment = str(row2[0])
                                photoname = PhotoComment.replace(" ", "_") + "_" + str(row2[1]) # create a photoname based on point attributes
                        AttName = str(item[1])
                        filename = photoname + "_" + str(count) + ".jpg" # create the complete file name for each photo
                        print(filename) # see what the name looks like
                        open(os.path.join(i, filename), 'wb').write(attachment.tobytes()) # write it out
                        del item
                        del filename
                        del attachment
                        count += 1
