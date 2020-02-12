import arcpy
import os, time, datetime

"""
========================================================================
1LSS_FormatParcelData_Analysis.py
========================================================================
Author: Joe Touzel
========================================================================
Date			Modifier	Description of Change
2020/02/12  	JT			Published
========================================================================
Description:
This script is designed to run the initial analysis on the parcel data
for a given county. This will add all of the necessary fields and 
calculate any that exist in the incoming parcel data.

Inputs:
- Parcel Feature Class for a given county
"""

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = True

# Script parameters
County = arcpy.GetParameterAsText(0) # this can be derived from the county boundary
Input_Parcels = arcpy.GetParameterAsText(3) # Get the parcel data to be processed
FinalData_OutputGeodatabase = arcpy.GetParameterAsText(6) # This is where all of our finalized output will be stored
Output_CoordinateSystem = arcpy.GetParameterAsText(8) # choose a state plane coordinate system
Minimum_ParcelAcreage = arcpy.GetParameterAsText(9)

# REMOVE AFTER TESTING IS COMPLETE
County = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb\WilliamsonCounty" # this can be derived from the county boundary
Input_Parcels = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb\stratmap19_landparcels_48491_williamson_201905" # Get the parcel data to be processed
FinalData_OutputGeodatabase = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb" # This is where all of our finalized output will be stored
Output_CoordinateSystem = r"C:\Users\jtouzel\AppData\Roaming\Esri\Desktop10.6\ArcMap\Coordinate Systems\NAD_1983_StatePlane_Texas_Central_FIPS_4203_Feet.prj"
Minimum_ParcelAcreage = 5