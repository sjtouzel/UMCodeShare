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
arcpy.env.scratchWorkspace = r"C:"   # *****
scratchGDB = arcpy.env.scratchGDB # Path to scratch GDB  # *****
outPathScratch = scratchGDB  # *****

# Standard projection
ProjectAll = r"C:\Users\jtouzel\AppData\Roaming\Esri\Desktop10.6\ArcMap\Coordinate Systems\NAD 1983 UTM Zone 10N.prj"  # *****

# Get DEM to use
DEM_GDB = r"E:\Dropbox (RES)\@RES GIS\projects\CA\Klamath\DEM\USGS_NED\USGS_NED.gdb"  # *****
env.workspace = DEM_GDB
FC_List_DEM = arcpy.ListDatasets()
DEM = os.path.join(DEM_GDB, FC_List_DEM[3])
descDEM = arcpy.Describe(DEM)
descDEM.spatialReference.name
# project DEM to UTM zone 10N
DEM_Proj = os.path.join(outPathScratch, "Klamath_DEM_Proj_v2")  # *****
arcpy.ProjectRaster_management(DEM, DEM_Proj, ProjectAll)


# Get the point layer and create a cursor to go through the points to run the analysis
PointLayerGDB = r"E:\Dropbox (RES)\@RES GIS\projects\CA\Klamath\SHP\EagleTerritoryDesignation_20191227\EagleTerritoryData.gdb"  # *****
env.workspace = PointLayerGDB  # *****
FC_List = arcpy.ListFeatureClasses()  # *****
PointLayer = os.path.join(PointLayerGDB, FC_List[0])  # *****
descFC = arcpy.Describe(PointLayer) # *****
descFC.spatialReference.name
OID_field = descFC.OIDFieldName  # *****
[f.name for f in arcpy.ListFields(PointLayer)] #check what fields are in this layer

PointNameList = []
count = 0
env.workspace = scratchGDB
with da.SearchCursor(PointLayer, [OID_field, 'RES_NAME', 'RES_NOTE']) as cursor: # get this data from each row
    for row in cursor:
        if row[2] == 'Golden Eagle':
            count += 1
            print(row[1])
            PointNameList.append(row[1])

arcpy.env.overwriteOutput = True
env.workspace = scratchGDB
filenameList = []
for n in PointNameList:
    filename = n.replace(" ", "_").replace(".", "_").replace(",","_")
    print("**********************\n", filename)
    outfc = os.path.join(scratchGDB, filename)
    where_clause = '"RES_NAME" = \'%s\'' % n
    arcpy.Select_analysis(PointLayer, outfc, where_clause)
    viewshed_RasterFC = 'ViewshedRaster_' + filename
    print("Running ViewShed Analysis")
    arcpy.Viewshed_3d(DEM, outfc, viewshed_RasterFC)
    print("Running Raster to Polygon")
    viewshed_PolyFC = 'ViewshedPoly_' + filename
    arcpy.RasterToPolygon_conversion(viewshed_RasterFC, viewshed_PolyFC, "SIMPLIFY", "Value", "MULTIPLE_OUTER_PART")
    print("Extract viewshed polygons")
    positive_viewshed = "PositiveViewshed_" + filename
    where_clause = '"gridcode" = 1'
    arcpy.Select_analysis(viewshed_PolyFC, positive_viewshed, where_clause)
    filenameList.append(os.path.join(scratchGDB, positive_viewshed))
    print("Adding SITE_ID field, calculating values")
    arcpy.AddField_management(positive_viewshed, "SITE_ID", "TEXT", field_length=50)
    arcpy.CalculateField_management(positive_viewshed, "SITE_ID", expression='"%s"' % n)
