import arcpy, sys, os, datetime, time
from arcpy import env

"""
========================================================================
HydrologyAnalysis_ESRI_Script.py
========================================================================
Author: Joe Touzel
========================================================================
Date			Modifier	Description of Change
2020/02/19  	JT			Published
========================================================================
Description:
This script is designed to run hydro analysis on DEM data
and generating conservation easements for exhibits

Inputs:
- Property Boundary
- DEM(s)
"""

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = True

# Script parameters
propBoundary = arcpy.GetParameterAsText(0) # Property Boundary Feature Class
outPath = arcpy.GetParameterAsText(1) # This is where all of our output will be stored
outCS = arcpy.GetParameterAsText(2) # Choose a state plane coordinate system
FlowAccumThresh = arcpy.GetParameterAsText(3) # Get the threshold for stream designation
lidarRasterFolder = arcpy.GetParameterAsText(4) # Get the folder where lidar/DEM tiles are
ConEaseBuf = arcpy.GetParameterAsText(5) or 200 # Get the conservation easement size. this will usually be 200 ft

#REMOVE AFTER TESTING IS COMPLETE
propBoundary = r"C:/Users/jtouzel/Desktop/PythonTempInput/GlockzinProperty_20190906.gdb/GlockzinBoundary_20190906" # Property Boundary Feature Class
outPath = r"C:\Users\jtouzel\Desktop\PythonTempOutput\HydroTestingOutput.gdb" # This is where all of our output will be stored
outCS = r"C:/Users/jtouzel/AppData/Roaming/Esri/Desktop10.6/ArcMap/Coordinate Systems/NAD 1983 UTM Zone 14N.prj" # Choose a state plane coordinate system
FlowAccumThresh = 3.5 # Get the threshold for stream designation
lidarRasterFolder = r"C:\Users\jtouzel\Downloads\RasterImport" # Get the folder where lidar/DEM tiles are
ConEaseBuf = 200 # Get the conservation easement size. this will usually be 200 ft

arcpy.AddMessage('')
arcpy.AddMessage("===================================================================")
sVersionInfo = 'HydrologyAnalysis_ESRI_Script.py, v20200218'
arcpy.AddMessage('Hydrology Analysis and Conservation Easement Tool, {}'.format(sVersionInfo))
arcpy.AddMessage("")
arcpy.AddMessage("Support: jtouzel@res.us, 281-715-9109")
arcpy.AddMessage("")
arcpy.AddMessage("Input FCs: {}".format(propBoundary))
arcpy.AddMessage("Input Folder of Rasters: {}".format(lidarRasterFolder))
arcpy.AddMessage("Input Conservation Easement buffer radius: {} ft".format(ConEaseBuf))
arcpy.AddMessage("===================================================================")



# Static things we need to import
dateTag = datetime.datetime.today().strftime('%Y%m%d') # looks somethin like this 20181213

###### Create Temp Geodatabase ######
arcpy.env.scratchWorkspace = r"C:"
scratchGDB = arcpy.env.scratchGDB # Path to scratch GDB

# reproject this merged boundary
env.workspace = outPath
arcpy.AddMessage("Projecting our incoming Parcel Boundary Data: {}".format(os.path.basename(os.path.normpath(propBoundary))))
propBoundaryReproj = os.path.basename(os.path.normpath(propBoundary)) + "_Proj" # Create the output path for the reprojected layer
arcpy.Project_management(propBoundary, propBoundaryReproj, outCS) # projecting
time.sleep(1)  # gives a 1 second pause before going to the next step
arcpy.AddMessage('Output is: {}'.format(propBoundaryReproj))
# if there is more than one property boundary
parcelCount = arcpy.GetCount_management(propBoundaryReproj)
arcpy.AddMessage("There's {} parcel(s) in this dataset".format(parcelCount))
time.sleep(1) # gives a 1 second pause before going to the next step
arcpy.AddMessage("Merging and Dissolving these for processing purposes")
propBoundaryMerge = os.path.join(propBoundaryReproj + "Merge") # create path for merge output ### USE THIS FOR ANALYSIS ###
arcpy.Dissolve_management(propBoundaryReproj, propBoundaryMerge)# merge multiple parcels into one
time.sleep(1) # gives a 1 second pause before going to the next step
arcpy.AddMessage('Output is: {}'.format(propBoundaryMerge))
# create an all encompassing boundary 1/2 mile around this boundary
envelopeBoundary = os.path.join(scratchGDB, "envelopeBoundary_" + dateTag)
arcpy.MinimumBoundingGeometry_management(propBoundaryMerge, envelopeBoundary, "ENVELOPE", "ALL") # first create a rectangular boundary around everything
extendedBoundary = "ExtendedBoundary_" + dateTag ### USE THIS FOR ANALYSIS ###
arcpy.AddMessage("Creating an all encompassing boundary 1/2 mile around our parcel boundary(s). Output is: {}".format(extendedBoundary))
arcpy.Buffer_analysis(envelopeBoundary, extendedBoundary, ".5 Miles", "FULL", "ROUND", "ALL", None, "PLANAR")
time.sleep(1) # gives a 1 second pause before going to the next step
# Create string with extent info. We'll need this for the raster clipping process later
ExtentString = ""
describeBoundaryExtent = arcpy.Describe(extendedBoundary)
ExtentString += str(describeBoundaryExtent.extent.XMin)
ExtentString += " " + str(describeBoundaryExtent.extent.YMin)
ExtentString += " " + str(describeBoundaryExtent.extent.XMax)
ExtentString += " " + str(describeBoundaryExtent.extent.YMax)

###### Import LiDAR Raster(s) ######
lidarRasterList = [] # empty list for all of our intersecting rasters
lidarRasterMosaic = "rasterMosaic_" + dateTag
arcpy.AddMessage("Creating a list of LIDAR/DEM rasters that intersect our boundary to mosaic.")
lidarRasterMosaicPath = os.path.join(scratchGDB, lidarRasterMosaic)
sExt = describeBoundaryExtent.extent
env.workspace = lidarRasterFolder
for i in arcpy.ListRasters(): # lets go through our folder to get all the raster files that intersect
    rDesc = arcpy.Describe(i)
    rExt = rDesc.extent
    if sExt.disjoint(rExt):
        arcpy.AddMessage("Raster {} is outside the boundary".format(i))
    else:
        arcpy.AddMessage("Raster {} is within the boundary".format(i))
        lidarRasterList.append(os.path.join(lidarRasterFolder, i))
arcpy.AddMessage("Creating a mosaic of the LIDAR/DEM rasters that intersect our boundary. Output is: {}".format(lidarRasterMosaic))
arcpy.MosaicToNewRaster_management(lidarRasterList, scratchGDB, lidarRasterMosaic, outCS, "32_BIT_FLOAT", "1", "1", "LAST", "FIRST") # lets merge all the rasters
lidarRasterClip = os.path.join(outPath, "lidarRasterClip_" + dateTag) ### USE THIS FOR ANALYSIS ###
arcpy.AddMessage("Clipping our mosaic to the boundary. Output is: {}".format(lidarRasterClip))
arcpy.Clip_management(lidarRasterMosaicPath, ExtentString, lidarRasterClip)

###### Run Hydrology Analysis ######
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
arcpy.AddMessage("Running a FILL analysis. Output is: {}".format(Fill))
outFill = arcpy.sa.Fill(lidarRasterClip) # Allow for overwrites
outFill.save(Fill)
time.sleep(1) # gives a 1 second pause before going to the next step
# Calc flow direction
arcpy.AddMessage("Running a FLOW DIRECTION analysis. Output is: {}".format(FlowDirection))
outFlowDir = arcpy.sa.FlowDirection(Fill, "NORMAL")
outFlowDir.save(FlowDirection)
time.sleep(1) # gives a 1 second pause before going to the next step
# Calc flow accumulation
arcpy.AddMessage("Running a FLOW ACCUMULATION analysis. Output is: {}".format(FlowAccum))
outFlowAcc = arcpy.sa.FlowAccumulation(FlowDirection, "", "FLOAT", "D8")
outFlowAcc.save(FlowAccum)
time.sleep(1) # gives a 1 second pause before going to the next step
# Calc Flow accumulation threshold raster
arcpy.AddMessage("Running a FLOW ACCUMULATION THRESHOLD RASTER analysis. Output is: {}".format(FlowAccumRC))
env.scratchWorkspace = scratchGDB
env.workspace = scratchGDB
arcpy.env.overwriteOutput = True
outRasterCalc = arcpy.sa.Con(arcpy.sa.Log10("FlowAccum") >= FlowAccumThresh, arcpy.sa.Log10("FlowAccum"))
outRasterCalc.save(FlowAccumRC)
time.sleep(1) # gives a 1 second pause before going to the next step
# Calc Stream Order
arcpy.AddMessage("Running a STREAM ORDER analysis. Output is: {}".format(StreamOrder))
env.workspace = scratchGDB
env.scratchWorkspace = scratchGDB
arcpy.env.overwriteOutput = True
outStreamOrder = arcpy.sa.StreamOrder(FlowAccumRC, FlowDirection, "STRAHLER") #### error shit
outStreamOrder.save(StreamOrder)
time.sleep(1) # gives a 1 second pause before going to the next step
# Create the stream line features
arcpy.AddMessage("Exporting final STREAM THALWEGS to a Feature Class. Output is: {}".format(StreamFeatureClass))
arcpy.sa.StreamToFeature(StreamOrder, FlowDirection, StreamFeatureClass, "SIMPLIFY")
time.sleep(1) # gives a 1 second pause before going to the next step
# Clip the streams to the Property boundary
env.workspace = outPath
StreamFC_Clip = os.path.basename(os.path.normpath(StreamFeatureClass)) + "_Clip" # Create the output name for our clipped streams
arcpy.AddMessage("Clipping the stream thalwegs to our property boundary. Output is: {}".format(StreamFC_Clip))
arcpy.Clip_analysis(StreamFeatureClass,propBoundaryMerge,StreamFC_Clip)
time.sleep(1) # gives a 1 second pause before going to the next step
# Create conservation easements
arcpy.AddMessage("Creating the {} ft radius conservation easements".format(ConEaseBuf))
ConEaseBufFC = "ConEaseBufFC{}_{}Ft_".format(FlowAccumThresh,ConEaseBuf) + dateTag # Create the output name for our conservation easement
arcpy.Buffer_analysis(StreamFC_Clip, ConEaseBufFC, "{} Feet".format(ConEaseBuf), "FULL", "ROUND", "ALL", None, "PLANAR")
time.sleep(1) # gives a 1 second pause before going to the next step
# Clip our conservation easements to the property boundary
ConEaseBufFC_Clip = ConEaseBufFC + "_Clip" # Create the output name for our clipped streams
arcpy.AddMessage("Clipping the easements to our property boundary. Output is: {}".format(ConEaseBufFC_Clip))
arcpy.Clip_analysis(ConEaseBufFC,propBoundaryMerge,ConEaseBufFC_Clip)
time.sleep(1) # gives a 1 second pause before going to the next step

