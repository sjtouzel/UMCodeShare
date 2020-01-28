# -*- coding: utf-8 -*-
"""Generated by ArcGIS ModelBuilder on: 2020-01-28 08:51:56
All ModelBuilder functionality may not be exported. Edits may be required for equivalency with the original model.
"""

import arcpy
import os

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = False

# Script parameters
county_extent = arcpy.GetParameterAsText(0) # this can be derived from the county boundary
Cell_Size_Height = arcpy.GetParameterAsText(1) or "5280" # We'll create a fishnet with 1 sq mile cells
Cell_Size_Width = arcpy.GetParameterAsText(2) or "5280" # We'll create a fishnet with 1 sq mile cells
Input_Parcels = arcpy.GetParameterAsText(3) # Get the parcel data to be processed
Parcel_FID = arcpy.GetParameterAsText(4) #
Output_Join_Field = arcpy.GetParameterAsText(6) #
FinalData_OutputGeodatabase = arcpy.GetParameterAsText(7) # This is where all of our finalized output will be stored
TempOutput_Geodatabase = arcpy.GetParameterAsText(8) # This is where all of our temporary output will be stored

#Create the grid from the county boundary
arcpy.CreateFishnet_management(out_feature_class=os.join.pathNC_Fishnet_shp, origin_coord="", y_axis_coord="", cell_width=Cell_Size_Width,
                               cell_height=Cell_Size_Height, number_rows="", number_columns="", corner_coord="", labels="NO_LABELS", template=Template_Extent, geometry_type="POLYGON")


