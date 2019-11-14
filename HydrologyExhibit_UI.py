# User interface for running hydro analysis on DEM data
# and generating conservation easements for exhibits

# import libraries
import os
from arcpy import env
import arcpy
import datetime
import time

###### Get date for tagging our output files ######
dateTag = datetime.datetime.today().strftime('%Y%m%d') # looks somethin like this 20181213

###### Create Temp Geodatabase ######
arcpy.env.scratchWorkspace = r"C:"
scratchGDB = arcpy.env.scratchGDB # Path to newly created gdb.

###### Designate Output GDB ######
outPath = r"C:\Users\jtouzel\Desktop\PythonTempOutput\HydroTestingOutput.gdb" ### NEEDS TO BE A PARAMETER ###

###### Designate projection info ######
outCS = r"C:/Users/jtouzel/AppData/Roaming/Esri/Desktop10.6/ArcMap/Coordinate Systems/NAD 1983 UTM Zone 14N.prj" ### NEEDS TO BE A PARAMETER ###

###### Data input GDB - will not be needed in final GUI, they'll just designate all the input layers individually ######
inputDataGDB = r"C:/Users/jtouzel/Desktop/PythonTempInput/GlockzinProperty_20190906.gdb"
env.workspace = inputDataGDB
FC_List = arcpy.ListFeatureClasses()
arcpy.ListDatasets()

###### Import Property Boundary ######
print("Importing Property Boundary")
time.sleep(2) # gives a 2 second pause before going to the next step
propBoundary = os.path.join(inputDataGDB, FC_List[0]) ### NEEDS TO BE A PARAMETER ###
# reproject this merged boundary
print("Let's make sure this parcel data is in your designated projection.")
time.sleep(2) # gives a 2 second pause before going to the next step
propBoundaryReproj = os.path.join(outPath, FC_List[0] + "Project") # Create the output path for the reprojected layer
arcpy.Project_management(propBoundary, propBoundaryReproj, outCS) # project that shit
# if there is more than one property boundary
parcelCount = arcpy.GetCount_management(propBoundary)
print("There's {} parcel(s) in this dataset".format(parcelCount))
time.sleep(2)
propBoundaryMerge = os.path.join(propBoundaryReproj + "Merge") # create path for merge output ### USE THIS FOR ANALYSIS ###
arcpy.Dissolve_management(propBoundaryReproj, propBoundaryMerge)# merge multiple parcels into one
# create an all encompassing boundary 1/2 mile around this boundary
envelopeBoundary = os.path.join(scratchGDB, "envelopeBoundary_" + dateTag)
arcpy.MinimumBoundingGeometry_management(propBoundaryMerge, envelopeBoundary, "ENVELOPE", "ALL") # first create a rectangular boundary around everything
extendedBoundary = os.path.join(outPath, "ExtendedBoundary_" + dateTag) ### USE THIS FOR ANALYSIS ###
arcpy.Buffer_analysis(envelopeBoundary, extendedBoundary, ".5 Miles", "FULL", "ROUND", "ALL", None, "PLANAR")
# Create string with extent info. We'll need this for the raster clipping process later
ExtentString = ""
describeBoundaryExtent = arcpy.Describe(extendedBoundary)
ExtentString += str(describeBoundaryExtent.extent.XMin)
ExtentString += " " + str(describeBoundaryExtent.extent.YMin)
ExtentString += " " + str(describeBoundaryExtent.extent.XMax)
ExtentString += " " + str(describeBoundaryExtent.extent.YMax)

###### Import LiDAR Raster(s) ######
lidarRasterFolder = r"C:\Users\jtouzel\Downloads\RasterImport" ### NEEDS TO BE A PARAMETER ### Will be a list of selected rasters
lidarRasterList = [] # empty list for all of our rasters
lidarRasterMosaic = "rasterMosaic_" + dateTag
lidarRasterMosaicPath = os.path.join(scratchGDB, lidarRasterMosaic)
for i in os.listdir(lidarRasterFolder): # lets go through our folder to get all the raster files
    if i.endswith('.img'):
        lidarRasterList.append(os.path.join(lidarRasterFolder, i))
arcpy.MosaicToNewRaster_management(lidarRasterList, scratchGDB, lidarRasterMosaic, outCS, "32_BIT_FLOAT", "1", "1", "LAST", "FIRST") # lets merge all the rasters
lidarRasterClip = os.path.join(outPath, "lidarRasterClip_" + dateTag) ### USE THIS FOR ANALYSIS ###
arcpy.Clip_management(lidarRasterMosaicPath, ExtentString, lidarRasterClip)

# Set stream delineation value (examine raster calc
# formula to figure out what this number means)
streamDelinThreshold = 3.5 ### NEEDS TO BE A PARAMETER ###








############ import all layers and databases ################### REMOVE AFTER DEVELOPEMENT IS DONE
dateTag = datetime.datetime.today().strftime('%Y%m%d') # looks somethin like this 20181213
arcpy.env.scratchWorkspace = r"C:"
scratchGDB = arcpy.env.scratchGDB # Path to newly created gdb.
outPath = r"C:\Users\jtouzel\Desktop\PythonTempOutput\HydroTestingOutput.gdb" # NEEDS TO BE A PARAMETER
outCS = r"C:/Users/jtouzel/AppData/Roaming/Esri/Desktop10.6/ArcMap/Coordinate Systems/NAD 1983 UTM Zone 14N.prj" # NEEDS TO BE A PARAMETER
inputDataGDB = r"C:/Users/jtouzel/Desktop/PythonTempInput/GlockzinProperty_20190906.gdb"
env.workspace = inputDataGDB
FC_List = arcpy.ListFeatureClasses()
propBoundary = os.path.join(inputDataGDB, FC_List[0]) # NEEDS TO BE A PARAMETER
propBoundaryReproj = os.path.join(outPath, FC_List[0] + "Project") # Create the output path for the reprojected layer
propBoundaryMerge = os.path.join(propBoundaryReproj + "Merge") # create path for merge output ### USE THIS FOR ANALYSIS ###
envelopeBoundary = os.path.join(scratchGDB, "envelopeBoundary_" + dateTag)
extendedBoundary = os.path.join(outPath, "ExtendedBoundary_" + dateTag) ### USE THIS FOR ANALYSIS ###
lidarRasterFolder = r"C:\Users\jtouzel\Downloads\RasterImport"
lidarRasterClip = os.path.join(outPath, "lidarRasterClip_" + dateTag) ### USE THIS FOR ANALYSIS ###