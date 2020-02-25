import arcpy
import os, time, datetime

"""
========================================================================
2LSS_GridID_HUC8_Analysis.py
========================================================================
Author: Katie Clark, Joe Touzel
========================================================================
Date			Modifier	Description of Change
2020/02/21  	JT			Published
========================================================================
Description:
This script is designed to run part two of the parcel data analysis
for a given county. it will calculate values for the GRID_ID and HUC_8
fields. This is in preparation for more specific analysis to
be completed by the analyst. 

Inputs:
- From Step 1: Projected County Boundary, Output GDB, Formatted Parcels
- Fishnet grid Cell size
- Parcel Feature Class for the county
"""


# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = True

# Script parameters
CountyProj = arcpy.GetParameterAsText(0) # this can be derived from the county boundary
Cell_Size_Height = arcpy.GetParameterAsText(1) or "5280" # We'll create a fishnet with 1 sq mile cells
Cell_Size_Width = arcpy.GetParameterAsText(2) or "5280" # We'll create a fishnet with 1 sq mile cells
Input_Parcels = arcpy.GetParameterAsText(3) # Get the parcel data to be processed
HUC_8 = arcpy.GetParameterAsText(4) # Get the HUC 8 feature class or shapefile
HUC8_FieldName = arcpy.GetParameterAsText(5) # get the HUC8 field name for adding it to the Parcel layer
FinalData_OutputGeodatabase = arcpy.GetParameterAsText(6) # This is where all of our finalized output will be stored
# TempOutput_Geodatabase = arcpy.GetParameterAsText(7) # This is where all of our temporary output will be stored
Output_CoordinateSystem = arcpy.GetParameterAsText(8) # choose a state plane coordinate system


# REMOVE AFTER TESTING IS COMPLETE
CountyProj = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb\WilliamsonCounty" # this can be derived from the county boundary
Cell_Size_Height = "5280" # We'll create a fishnet with 1 sq mile cells
Cell_Size_Width = "5280" # We'll create a fishnet with 1 sq mile cells
Input_Parcels = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb\ParcelFilterFC_20200224" # Get the parcel data to be processed
GridID_FieldName = "Grid2" # get the field for the Grid ID from the incoming formatted parcel data
ParcelHUC8_FieldName = "HUC_8"
HUC_8 = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb\HUC8_FC" # Get the HUC 8 feature class or shapefile
HUC8_FieldName = 'HUC_8' # what field in the incoming HUC8 layer contains the HUC8 numbers
FinalData_OutputGeodatabase = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb" # This is where all of our finalized output will be stored
# TempOutput_Geodatabase = arcpy.GetParameterAsText(8)
Output_CoordinateSystem = r"C:\Users\jtouzel\AppData\Roaming\Esri\Desktop10.6\ArcMap\Coordinate Systems\NAD_1983_StatePlane_Texas_Central_FIPS_4203_Feet.prj"


# Write to Log
arcpy.AddMessage('')
arcpy.AddMessage("===================================================================")
sVersionInfo = 'LSS_CombinedProcess.py, v20200207'
arcpy.AddMessage('Running initial analysis for Land Search Parcels, {}'.format(sVersionInfo))
arcpy.AddMessage("")
arcpy.AddMessage("Support: jtouzel@res.us, 281-715-9109")
arcpy.AddMessage("")
arcpy.AddMessage("Input FCs: {0}, {1}, {2}".format(os.path.basename(os.path.normpath(CountyProj)),
                                                   os.path.basename(os.path.normpath(Input_Parcels)),
                                                   os.path.basename(os.path.normpath(HUC_8))))
field_names = [f.name for f in arcpy.ListFields(Input_Parcels)]
arcpy.AddMessage("Field Names: {}".format(", ".join(field_names)))
arcpy.AddMessage("===================================================================")


# #Reproject all incoming data
# arcpy.AddMessage('Reprojecting input County, {}'.format(os.path.basename(os.path.normpath(County))))
# arcpy.env.workspace = FinalData_OutputGeodatabase
# CountyProj = os.path.basename(os.path.normpath(County)) + "_Proj"
# time.sleep(1)  # gives a .5 second pause before going to the next step
# arcpy.AddMessage('Output is: {}'.format(CountyProj))
# arcpy.Project_management(County, CountyProj, Output_CoordinateSystem)
# arcpy.AddMessage('Reprojecting input Parcels, {}'.format(os.path.basename(os.path.normpath(Input_Parcels))))
# ParcelProj = os.path.basename(os.path.normpath(Input_Parcels)) + "_Proj"
# arcpy.Project_management(Input_Parcels, ParcelProj, Output_CoordinateSystem)
# time.sleep(1)  # gives a .5 second pause before going to the next step
# arcpy.AddMessage('Output is: {}'.format(ParcelProj))

#### Create the Fishnet Grid and add Grid ID to the Parcel Layer
#Create the grid from the county boundary
dateTag = datetime.datetime.today().strftime('%Y%m%d') # we'll tag our output with this. looks somethin like this 20181213
fishnetFileName = "FishnetGrid_" + dateTag # create a filename for the fishnet grid
CountyProjDesc = arcpy.Describe(CountyProj) # get the details of the county data
arcpy.AddMessage('Creating the square mile Fishnet Grid: {}'.format(fishnetFileName))
arcpy.CreateFishnet_management(out_feature_class=os.path.join(FinalData_OutputGeodatabase, fishnetFileName),
                               origin_coord=str(CountyProjDesc.extent.lowerLeft),
                               y_axis_coord=str(CountyProjDesc.extent.XMin) + " " + str(CountyProjDesc.extent.YMax),
                               cell_width=Cell_Size_Width,
                               cell_height=Cell_Size_Height,
                               number_rows="", number_columns="",
                               corner_coord=str(CountyProjDesc.extent.upperRight), labels="NO_LABELS",
                               template=CountyProj, geometry_type="POLYGON")
time.sleep(1)  # gives a .5 second pause before going to the next step
##add a field to the fishnet grid called GRID_FID
Grid_FID = "Grid_FID"
arcpy.AddMessage('Adding a GRID_FID field to the fishnet grid. Field Name: {}'.format(Grid_FID))
arcpy.AddField_management(in_table=fishnetFileName, field_name=Grid_FID, field_type="LONG", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
###Calculate FID field as a copy of the OID field
oidFieldName1 = arcpy.Describe(fishnetFileName).OIDFieldName
arcpy.AddMessage('Calculating the GRID_FID field as a copy of the ObjectID field')
arcpy.CalculateField_management(in_table=fishnetFileName, field=Grid_FID, expression="!" + oidFieldName1 + "!",
                                expression_type="PYTHON3", code_block="")
time.sleep(1)  # gives a 1 second pause before going to the next step
#Add an FID field to the parcel layer
FID_FieldName_1 = "FID_v1"
arcpy.AddMessage('Adding an FID field to the Parcel layer. Field Name: {}'.format(FID_FieldName_1))
arcpy.AddField_management(in_table=Input_Parcels, field_name=FID_FieldName_1, field_type="LONG", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
##Calculate FID field as a copy of the OID field
oidFieldName2 = arcpy.Describe(Input_Parcels).OIDFieldName
arcpy.AddMessage('Calculating the Parcel FID field as a copy of the ObjectID field')
arcpy.CalculateField_management(in_table=Input_Parcels, field=FID_FieldName_1, expression="!" + oidFieldName2 + "!",
                                expression_type="PYTHON3", code_block="")
time.sleep(1)  # gives a 1 second pause before going to the next step
##Add a Grid_ID field and an ACRES field
# GridID_FieldName = "GRID_ID"
# Acres_FieldName = "ACRES_v1"
# arcpy.AddMessage('Adding a GRID_ID, and an ACRES field to the Parcel layer. Field Names: {}, {}'.format(GridID_FieldName
#                                                                                                         ,Acres_FieldName))
# arcpy.AddField_management(in_table=ParcelProj, field_name=GridID_FieldName, field_type="LONG", field_precision="",
#                           field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
#                           field_is_required="NON_REQUIRED", field_domain="")
# arcpy.AddField_management(in_table=ParcelProj, field_name=Acres_FieldName, field_type="DOUBLE", field_precision="",
#                           field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
#                           field_is_required="NON_REQUIRED", field_domain="")
# time.sleep(1)  # gives a .5 second pause before going to the next step
###Calculate acreage
# arcpy.AddMessage('Calculating the Parcel Acreage')
# arcpy.CalculateField_management(in_table=ParcelProj, field=Acres_FieldName, expression="!shape.area@acres!",
#                                 expression_type="PYTHON3", code_block="")
# time.sleep(1)  # gives a .5 second pause before going to the next step

##### Add Grid ID numbers to our parcel layer #####
#run a spatial join on the parcel data and the grid layer so we can add a Grid ID to the parcel layer
ParcelGridJoin = "ParcelGridJoin_" + dateTag
arcpy.AddMessage('Running a spatial join on the Parcels and Fishnet Grid')
arcpy.SpatialJoin_analysis(target_features=Input_Parcels, join_features=fishnetFileName, out_feature_class=ParcelGridJoin,
                           join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option='HAVE_THEIR_CENTER_IN')
time.sleep(1)  # gives a .5 second pause before going to the next step
#join the parcel data and the parcel grid join so we can calculate the GRID_ID field
ParcelFeatureLayer = "ParcelFeatureLayer_" + dateTag
arcpy.MakeFeatureLayer_management(Input_Parcels, ParcelFeatureLayer)
arcpy.AddMessage('Joining the Parcels with the spatially joined Parcel/Grid table')
arcpy.AddJoin_management(in_layer_or_view=ParcelFeatureLayer, in_field=FID_FieldName_1, join_table=ParcelGridJoin,
                         join_field=FID_FieldName_1, join_type="KEEP_ALL")
time.sleep(1)  # gives a .5 second pause before going to the next step
##Calculate the Grid ID from the joined table Grid ID
CalcParcelGridField = Input_Parcels + "." + GridID_FieldName
CalcGridField = ParcelGridJoin + "." + Grid_FID
arcpy.AddMessage('Calculating the GRID_ID field for the Parcel layer and removing join')
arcpy.CalculateField_management(in_table=ParcelFeatureLayer, field=CalcParcelGridField,
                                expression="!" + CalcGridField + "!", expression_type="PYTHON3", code_block="")
arcpy.RemoveJoin_management(in_layer_or_view=ParcelFeatureLayer)
time.sleep(1)  # gives a .5 second pause before going to the next step
# ###Filter out all parcels smaller than Minimum Parcel Acreage
# arcpy.AddMessage('Filtering out all parcels less than {} acres'.format(Minimum_ParcelAcreage))
# Selection1 = '"{}" >= {}'.format(Acres_FieldName,Minimum_ParcelAcreage)
# arcpy.SelectLayerByAttribute_management(ParcelFeatureLayer, 'NEW_SELECTION',
#                                         Selection1)
#
# time.sleep(1)  # gives a .5 second pause before going to the next step
##copy the updated parcel layer to a new FC
ParcelFeatureClass_WithGrid = "ParcelsGridID_" + dateTag
arcpy.AddMessage('Export the updated Parcel layer to a new Feature Class: {}'.format(ParcelFeatureClass_WithGrid))
arcpy.CopyFeatures_management(ParcelFeatureLayer, ParcelFeatureClass_WithGrid)
time.sleep(1)  # gives a 1 second pause before going to the next step

##### Add HUC8 numbers to our parcel layer #####
##add HUC8 Field to the parcel layer
# ParcelHUC8_FieldName = "HUC8_v1"
# arcpy.AddMessage('Adding a HUC 8 field to the Parcel layer. Field Name: {}'.format(ParcelHUC8_FieldName))
# arcpy.AddField_management(in_table=ParcelFeatureClass_WithGrid, field_name=ParcelHUC8_FieldName, field_type="TEXT", field_precision="",
#                           field_scale="", field_length=8, field_alias="", field_is_nullable="NULLABLE",
#                           field_is_required="NON_REQUIRED", field_domain="")
##copy the HUC 8 data to our geodatabase
HUC8_FC = "HUC8_FC" # Create filename and we'll copy our incoming HUC8 FC to our output GDB so we can edit it
arcpy.FeatureClassToFeatureClass_conversion(HUC_8, FinalData_OutputGeodatabase, HUC8_FC)
###add a "HUC8_RES" field to the HUC8 FC we just created, we'll copy the HUC8 values over from this field
HUC8_RES = "HUC8_RES"
arcpy.AddField_management(in_table=HUC8_FC, field_name=HUC8_RES, field_type="LONG", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=HUC8_FC, field=HUC8_RES,
                                expression="!" + HUC8_FieldName + "!", expression_type="PYTHON3", code_block="")
##run a spatial join on the parcels and the HUC8 FC
ParcelHUC8Join = "ParcelHUC8Join_" + dateTag
arcpy.AddMessage('Running a spatial join on the Parcels and HUC8 layer')
arcpy.SpatialJoin_analysis(target_features=ParcelFeatureClass_WithGrid, join_features=HUC8_FC,
                           out_feature_class=ParcelHUC8Join, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",
                           match_option='HAVE_THEIR_CENTER_IN')
time.sleep(1)  # gives a .5 second pause before going to the next step
##export the spatial join data to a feature layer and join the parcel and huc8 spatial join tables
ParcelGridFeatureLayer = "ParcelGridFeatureLayer_" + dateTag
arcpy.MakeFeatureLayer_management(ParcelFeatureClass_WithGrid, ParcelGridFeatureLayer)
arcpy.AddMessage('Joining the Parcels with the spatially joined Parcel/HUC8 table')
arcpy.AddJoin_management(in_layer_or_view=ParcelGridFeatureLayer, in_field=FID_FieldName_1, join_table=ParcelHUC8Join,
                         join_field=FID_FieldName_1, join_type="KEEP_ALL")
time.sleep(1)  # gives a .5 second pause before going to the next step
##Calculate the HUC8 field from the joined table HUC8
CalcParcelHUC8Field = ParcelFeatureClass_WithGrid + "." + ParcelHUC8_FieldName
CalcHUC8Field = ParcelHUC8Join + "." + HUC8_RES
arcpy.AddMessage('Calculating the HUC8 field for the Parcel layer and removing join')
arcpy.CalculateField_management(in_table=ParcelGridFeatureLayer, field=CalcParcelHUC8Field,
                                expression="!" + CalcHUC8Field + "!", expression_type="PYTHON3", code_block="")
arcpy.RemoveJoin_management(in_layer_or_view=ParcelGridFeatureLayer)
time.sleep(1)  # gives a .5 second pause before going to the next step
##export the updated layer to a new FC
ParcelsGridHuc_FC = "ParcelsGridHuc_" + dateTag
arcpy.AddMessage('Export the updated Parcel layer to a new Feature Class: {}'.format(ParcelsGridHuc_FC))
arcpy.CopyFeatures_management(ParcelGridFeatureLayer, ParcelsGridHuc_FC)
time.sleep(1)  # gives a .5 second pause before going to the next step

##### Calculate Stream LF from input stream data in another process #####

