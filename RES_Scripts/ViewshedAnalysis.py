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

# Get the point layer and create a cursor to go through the points to run the analysis
PointLayerGDB = r"E:\Dropbox (RES)\@RES GIS\projects\CA\Klamath\SHP\EagleTerritoryDesignation_20191227\EagleTerritoryData.gdb"
