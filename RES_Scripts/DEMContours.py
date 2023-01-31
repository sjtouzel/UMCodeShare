import arcpy
from arcpy.sa import *

# we gonna create some contours from a DEM

try:
    inputDEM = arcpy.GetParameterAsText(0)
    outputContourLines = arcpy.GetParameterAsText(1)


    arcpy.Contour_3d(Raster(inputDEM),outputContourLines,"100 feet")

except:
    arcpy.AddError("This biz broke homie")
    arcpy.AddMessage(arcpy.GetMessages())


