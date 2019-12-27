import arcpy
from arcpy import da
from arcpy import env
import sys, os, datetime

"""
========================================================================
CollectorAppPhotos_ESRI_Script.py
========================================================================
Author: Joe Touzel
========================================================================
Date			Modifier	Description of Change
2019/12/26  	JT			Published
========================================================================
Description:
This script is designed to customize the process of downloading photos
from collector app data. The user can customize the attributes to include
and format the output filename accordingly.

Inputs:
- collector app layer with photos to be extracted
- collector app table with joining info and photos
- output folder
"""

# Inputs
inputPhotoFC = arcpy.GetParameterAsText(0)
inputPhotoTable = arcpy.GetParameterAsText(1)
attribute1 = arcpy.GetParameterAsText(2)
attribute2 = arcpy.GetParameterAsText(3)
attribute3 = arcpy.GetParameterAsText(4)
outputFolder = arcpy.GetParameterAsText(5)

# Write to Log
arcpy.AddMessage('')
arcpy.AddMessage("===================================================================")
sVersionInfo = 'CollectorAppPhotos_ESRI_Script.py, v20191226'
arcpy.AddMessage('Collector App Photo Extractor, {}'.format(sVersionInfo))
arcpy.AddMessage("")
arcpy.AddMessage("Support: jtouzel@res.us, 281-715-9109")
arcpy.AddMessage("")
arcpy.AddMessage("Input FC: {}".format(inputPhotoFC))
field_names = [f.name for f in arcpy.ListFields(inputPhotoFC)]
arcpy.AddMessage("Field Names: {}".format(", ".join(field_names)))
arcpy.AddMessage("===================================================================")

# Set up our attribute list
allattributeList = [attribute1, attribute2, attribute3]
attributeList = [i for i in allattributeList if i] # this will make a list of all the attributes that were selected


# Get the photo and name it
with inputPhotoTable:
    with da.SearchCursor(inputPhotoTable, ['DATA', 'ATT_NAME', 'REL_GLOBALID']) as cursor: # get this data from each row
        count = 0
        for item in cursor:
            attachment = item[0]
            with arcpy.da.SearchCursor(inputPhotoFC, attributeList,"{0} = '{1}'".format("GlobalID", item[2])) as cursor2:  # look through point FC to get the related info for each photo
                for row2 in cursor2:
                    photonameList = []
                    for i in range(0, len(attributeList)):
                        photonameList.append(str(row2[i]).replace(" ", "_"))
                    photoname = "_".join(photonameList)
                    filename = photoname + "_" + str(count) + ".jpg"  # create the complete file name for each photo
                    print(filename)  # see what the name looks like
                    open(os.path.join(outputFolder, filename), 'wb').write(attachment.tobytes())  # write it out
                    del item
                    del filename
                    del attachment
                    count += 1
