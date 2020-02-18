import arcpy, os, datetime, time
from arcpy import env

"""
========================================================================
1LSS_FormatParcelData_Analysis.py
========================================================================
Author: Katie Clark, Joe Touzel
========================================================================
Date			Modifier	Description of Change
2020/02/12  	JT			Published
========================================================================
Description:
This script is designed to run the initial formatting on the parcel data
for a given county. This will add all of the necessary fields and 
calculate any that exist in the incoming parcel data.

Inputs:
- Parcel Feature Class for a given county
"""

# User interface for running hydro analysis on DEM data
# and generating conservation easements for exhibits

###### Get date for tagging our output files ######
dateTag = datetime.datetime.today().strftime('%Y%m%d') # looks somethin like this 20181213

###### Create Temp Geodatabase ######
arcpy.env.scratchWorkspace = r"C:"
scratchGDB = arcpy.env.scratchGDB # Path to scratch GDB
arcpy.env.overwriteOutput = True

###### Designate Output GDB ######
outPath = r"C:\Users\jtouzel\Desktop\PythonTempOutput\HydroTestingOutput.gdb" ### NEEDS TO BE A PARAMETER ###

###### Designate projection info ######
outCS = r"C:/Users/jtouzel/AppData/Roaming/Esri/Desktop10.6/ArcMap/Coordinate Systems/NAD 1983 UTM Zone 14N.prj" ### NEEDS TO BE A PARAMETER ###

###### Designate flow accumulation threshold ######
FlowAccumThresh = 3.5 ### NEEDS TO BE A PARAMETER ###

###### Data input GDB - will not be needed in final GUI, they'll just designate all the input layers individually ######
inputDataGDB = r"C:/Users/jtouzel/Desktop/PythonTempInput/GlockzinProperty_20190906.gdb"
env.workspace = inputDataGDB
arcpy.env.overwriteOutput = True
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

###### Run Hydrology Analysis ######
FlowAccumThresh = 3.5 # Set stream delineation value ### NEEDS TO BE A PARAMETER ###
# Scratch variables we'll use in our analysis
Fill = os.path.join(scratchGDB, 'Fill')
FlowDrop = os.path.join(scratchGDB, 'FlowDrop')
FlowDirection = os.path.join(scratchGDB, 'FlowDirection')
FlowAccum = os.path.join(scratchGDB, 'FlowAccum')
FlowAccumRC = os.path.join(scratchGDB, 'FlowAccumRC')
StreamOrder = os.path.join(scratchGDB, 'StreamOrder')
StreamFeatureClass = os.path.join(outPath, 'StreamThalwegs_Thresh' + str(FlowAccumThresh).replace(".","") + "_" + dateTag)
# Fill the DEM
env.scratchWorkspace = scratchGDB
env.workspace = scratchGDB
arcpy.env.overwriteOutput = True
outFill = arcpy.sa.Fill(lidarRasterClip) # Allow for overwrites
outFill.save(Fill)
# Calc flow direction
outFlowDir = arcpy.sa.FlowDirection(Fill, "NORMAL")
outFlowDir.save(FlowDirection)
# Calc flow accumulation
outFlowAcc = arcpy.sa.FlowAccumulation(FlowDirection, "", "FLOAT", "D8")
outFlowAcc.save(FlowAccum)
# Calc Flow accumulation threshold raster
env.scratchWorkspace = scratchGDB
env.workspace = scratchGDB
arcpy.env.overwriteOutput = True
outRasterCalc = arcpy.sa.Con(arcpy.sa.Log10("FlowAccum") >= FlowAccumThresh, arcpy.sa.Log10("FlowAccum"))
outRasterCalc.save(FlowAccumRC)
# Calc Stream Order
env.workspace = scratchGDB
env.scratchWorkspace = scratchGDB
arcpy.env.overwriteOutput = True
outStreamOrder = arcpy.sa.StreamOrder(FlowAccumRC, FlowDirection, "STRAHLER") #### error shit
outStreamOrder.save(StreamOrder)
# Create the stream line features
arcpy.sa.StreamToFeature(StreamOrder, FlowDirection, StreamFeatureClass, "SIMPLIFY")
# Clip the streams to the Property boundary
arcpy.Clip_analysis()



############ import all layers and databases ################### REMOVE AFTER DEVELOPEMENT IS DONE
import os
from arcpy import env
import arcpy
import datetime
import time

dateTag = datetime.datetime.today().strftime('%Y%m%d') # looks somethin like this 20181213
arcpy.env.scratchWorkspace = r"C:"
scratchGDB = arcpy.env.scratchGDB # Path to newly created gdb.
outPath = r"C:\Users\jtouzel\Desktop\PythonTempOutput\HydroTestingOutput.gdb" # NEEDS TO BE A PARAMETER
outCS = r"C:/Users/jtouzel/AppData/Roaming/Esri/Desktop10.6/ArcMap/Coordinate Systems/NAD 1983 UTM Zone 14N.prj" # NEEDS TO BE A PARAMETER
inputDataGDB = r"C:/Users/jtouzel/Desktop/PythonTempInput/GlockzinProperty_20190906.gdb"
env.workspace = inputDataGDB
arcpy.env.overwriteOutput = True
FC_List = arcpy.ListFeatureClasses()
propBoundary = os.path.join(inputDataGDB, FC_List[0]) # NEEDS TO BE A PARAMETER
propBoundaryReproj = os.path.join(outPath, FC_List[0] + "Project") # Create the output path for the reprojected layer
propBoundaryMerge = os.path.join(propBoundaryReproj + "Merge") # create path for merge output ### USE THIS FOR ANALYSIS ###
envelopeBoundary = os.path.join(scratchGDB, "envelopeBoundary_20191112")
extendedBoundary = os.path.join(outPath, "ExtendedBoundary_20191112") ### USE THIS FOR ANALYSIS ###
lidarRasterFolder = r"C:\Users\jtouzel\Downloads\RasterImport"
lidarRasterClip = os.path.join(outPath, "lidarRasterClip_20191112") ### USE THIS FOR ANALYSIS ###
FlowAccumThresh = 3.5 # Set stream delineation value ### NEEDS TO BE A PARAMETER ###