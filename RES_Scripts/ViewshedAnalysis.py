import arcpy
from arcpy import da
from arcpy import env
import time, os

"""
========================================================================
ViewshedAnalysis.py
========================================================================
Author: Joe Touzel
========================================================================
Date			Modifier	Description of Change
2020/01/13  	JT			Published
========================================================================
Description:
This script is designed to create viewsheds for a bunch of points, 
convert those viewsheds to polygons, add a field with a unique name,
and then aggregate them into one shapefile 

Inputs:
- Point Layer
- Smoothed DEM
- output folder
"""
# Scratch workspace
arcpy.env.scratchWorkspace = r"C:"
scratchGDB = arcpy.env.scratchGDB # Path to scratch GDB
outPathScratch = scratchGDB

# Standard projection
ProjectAll = r"C:\Users\jtouzel\AppData\Roaming\Esri\Desktop10.6\ArcMap\Coordinate Systems\NAD 1983 UTM Zone 10N.prj"

# Get DEM to use
DEM_GDB = r"E:\Dropbox (RES)\@RES GIS\projects\CA\Klamath\DEM\USGS_NED\USGS_NED.gdb"
env.workspace = DEM_GDB
FC_List_DEM = arcpy.ListDatasets()
DEM = os.path.join(DEM_GDB, FC_List_DEM[3])
descDEM = arcpy.Describe(DEM)
descDEM.spatialReference.name
# project DEM to UTM zone 10N
DEM_Proj = os.path.join(outPathScratch, "Klamath_DEM_Proj")
arcpy.ProjectRaster_management(DEM, DEM_Proj, ProjectAll)


# Get the point layer and create a cursor to go through the points to run the analysis
PointLayerGDB = r"E:\Dropbox (RES)\@RES GIS\projects\CA\Klamath\SHP\EagleTerritoryDesignation_20191227\EagleTerritoryData.gdb"
env.workspace = PointLayerGDB
FC_List = arcpy.ListFeatureClasses()
PointLayer = os.path.join(PointLayerGDB, FC_List[0])
descFC = arcpy.Describe(PointLayer)
descFC.spatialReference.name
arcpy.ListFields(PointLayer) #check what fields are in this layer


with da.SearchCursor(PointLayer, ['RES_NAME']) as cursor: # get this data from each row
    for row in cursor:
        print(row[0])


