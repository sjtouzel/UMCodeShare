import arcpy
import os, time, datetime

"""
========================================================================
1LSS_HUC_GRID_Analysis.py
========================================================================
Author: Joe Touzel
========================================================================
Date			Modifier	Description of Change
2020/04/21  	JT			Published
2020/06/03      JT          removed huc8 and grid layer additions to 
                            active pro doc
2020/06/26      JT          Using units as an input for cell dimensions
========================================================================
Description:
This script is designed to add HUC 8 and grid values to the unformatted
parcel data.

Inputs:
- Parcel Feature Class for a given county
"""

#Function for adding fields to our Projected Parcel Layer
def addFields(parcelData,fieldName,fieldType,fieldAlias):
    arcpy.AddMessage('Adding {} field to the Parcel Layer. Field Name: {}'.format(fieldAlias,fieldName))
    arcpy.AddMessage('------------')
    arcpy.AddField_management(in_table=parcelData, field_name=fieldName, field_type=fieldType, field_precision="",
                              field_scale="", field_length="", field_alias=fieldAlias, field_is_nullable="NULLABLE",
                              field_is_required="NON_REQUIRED", field_domain="")
    time.sleep(1)  # gives a 1 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

def main():

    # To allow overwriting the outputs change the overwrite option to true.
    arcpy.env.overwriteOutput = True

    # Script parameters
    ParcelData = arcpy.GetParameterAsText(0)  # import the parcel data
    Output_CoordinateSystem = arcpy.GetParameterAsText(1)  # choose a state plane coordinate system
    Cell_Size_Height = arcpy.GetParameterAsText(2) or "5280"  # We'll create a fishnet with 1 sq mile cells
    Cell_Size_Width = arcpy.GetParameterAsText(3) or "5280"  # We'll create a fishnet with 1 sq mile cells
    HUC8_FC = arcpy.GetParameterAsText(4)  # Get the HUC 8 feature class or shapefile
    HUC8_FC_FieldName = arcpy.GetParameterAsText(5)  # Get the HUC8 field name for our HUC 8 FC
    FinalData_OutputGeodatabase = arcpy.GetParameterAsText(6)  # This is where all of our finalized output will be stored
    OutputFC_FileName = arcpy.GetParameterAsText(7) # we'll create a name for our output feature class

    # REMOVE AFTER TESTING IS COMPLETE
    # ParcelData = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT\Pro_Default.gdb\TestingParcelFormatOutput"  # import the parcel data
    # Cell_Size_Height = "5280"  # We'll create a fishnet with 1 sq mile cells
    # Cell_Size_Width = "5280"  # We'll create a fishnet with 1 sq mile cells
    # GridID_FieldName = "Grid"  # get the field for the Grid ID from the incoming formatted parcel data
    # HUC8_FieldName = "HUC_8"  # get the field name for the HUC8 field from the incoming formatted parcel data
    # HUC8_FC = r"R:\Resgis\dropboxgis\Data\National\USGS\NATIONAL_WBD_GDB.gdb\WBD\WBDHU8"  # Get the HUC 8 feature class or shapefile
    # HUC8_FC_FieldName = "HUC8"  # get the HUC8 field name for our HUC 8 FC
    # FinalData_OutputGeodatabase = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT\Pro_Default.gdb"  # This is where all of our finalized output will be stored


    # Write to Log
    arcpy.AddMessage('')
    arcpy.AddMessage("===================================================================")
    sVersionInfo = '1LSS_HUC_GRID_Analysis.py, v20200603'
    arcpy.AddMessage('Creating GridID and HUC8 data for the Parcel Dataset, {}'.format(sVersionInfo))
    arcpy.AddMessage("")
    arcpy.AddMessage("Support: jtouzel@res.us, 281-715-9109")
    arcpy.AddMessage("")
    arcpy.AddMessage("Input FCs: {0}, {1}".format(os.path.basename(os.path.normpath(ParcelData)),
                                                  os.path.basename(os.path.normpath(HUC8_FC))))
    arcpy.AddMessage("===================================================================")

    arcpy.env.workspace = FinalData_OutputGeodatabase # Set the workspace

    # Static things we need to import
    dateTag = datetime.datetime.today().strftime('%Y%m%d')  # we'll tag some of our output with this. looks somethin like this 20181213
    arcpy.SetProgressor("step", "Processing Parcels...", 0, 20, 1)  # Progress Bar setup

    arcpy.AddMessage(Cell_Size_Height + " ---- " + Cell_Size_Width)

    #### Reproject the incoming parcel data to our chosen State Plane Coord System
    arcpy.AddMessage('Reprojecting input Parcels, {}'.format(os.path.basename(os.path.normpath(ParcelData))))
    arcpy.AddMessage('------------')
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar
    ParcelProj = arcpy.ValidateTableName(os.path.basename(os.path.normpath(ParcelData))) + "_Proj"
    arcpy.Project_management(ParcelData, ParcelProj, Output_CoordinateSystem)
    time.sleep(1)  # gives a 1 second pause before going to the next step
    arcpy.AddMessage('Output is: {}'.format(ParcelProj))
    arcpy.AddMessage('------------')
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    # Repair geometry - this will prevent any problems with self intersecting parcels and other topology errors
    arcpy.AddMessage('Running the Repair Geometry tool to correct any geometry errors within the parcel data')
    arcpy.AddMessage('------------')
    arcpy.RepairGeometry_management(ParcelProj)
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    # Add an FID field to the parcel layer so we can join our datasets after processing
    FID_FieldName_1 = "FID_v1"
    arcpy.AddMessage('Adding an FID field to the Parcel layer. Field Name: {}'.format(FID_FieldName_1))
    arcpy.AddMessage('------------')
    arcpy.AddField_management(in_table=ParcelProj, field_name=FID_FieldName_1, field_type="LONG", field_precision="",
                              field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                              field_is_required="NON_REQUIRED", field_domain="")
    time.sleep(1)  # gives a 1 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    ## Calculate FID field as a copy of the OID field
    oidFieldName2 = arcpy.Describe(ParcelProj).OIDFieldName
    arcpy.AddMessage('Calculating the Parcel FID field as a copy of the ObjectID field')
    arcpy.AddMessage('------------')
    arcpy.CalculateField_management(in_table=ParcelProj, field=FID_FieldName_1, expression="!" + oidFieldName2 + "!",
                                    expression_type="PYTHON3", code_block="")
    time.sleep(1)  # gives a 1 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    #### Create the Fishnet Grid and add Grid ID data to the Parcel Layer
    # Create the grid from the county boundary
    fishnetFileName = "FishnetGrid_" + dateTag  # create a filename for the fishnet grid
    ParcelDataDesc = arcpy.Describe(ParcelProj)  # get the details of the county data
    arcpy.AddMessage('Creating the square mile Fishnet Grid: {}'.format(fishnetFileName))
    arcpy.AddMessage('------------')
    arcpy.CreateFishnet_management(out_feature_class=os.path.join(FinalData_OutputGeodatabase, fishnetFileName),
                                   origin_coord=str(ParcelDataDesc.extent.lowerLeft),
                                   y_axis_coord=str(ParcelDataDesc.extent.XMin) + " " + str(ParcelDataDesc.extent.YMax),
                                   cell_width=Cell_Size_Width,
                                   cell_height=Cell_Size_Height,
                                   number_rows="", number_columns="",
                                   corner_coord=str(ParcelDataDesc.extent.upperRight), labels="NO_LABELS",
                                   template=ParcelProj, geometry_type="POLYGON")
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    # add a field to the fishnet grid called GRID_FID
    Grid_FID = "Grid_FID"
    arcpy.AddMessage('Adding a GRID_FID field to the fishnet grid. Field Name: {}'.format(Grid_FID))
    arcpy.AddMessage('------------')
    arcpy.AddField_management(in_table=fishnetFileName, field_name=Grid_FID, field_type="LONG", field_precision="",
                              field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                              field_is_required="NON_REQUIRED", field_domain="")
    time.sleep(1)  # gives a 1 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    # Calculate FID field as a copy of the OID field
    oidFieldName1 = arcpy.Describe(fishnetFileName).OIDFieldName
    arcpy.AddMessage('Calculating the GRID_FID field as a copy of the ObjectID field')
    arcpy.AddMessage('------------')
    arcpy.CalculateField_management(in_table=fishnetFileName, field=Grid_FID, expression="!" + oidFieldName1 + "!",
                                    expression_type="PYTHON3", code_block="")
    time.sleep(1)  # gives a 1 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    ##### Add Grid ID numbers to our parcel layer #####
    # run a spatial join on the parcel data and the grid layer so we can add a Grid ID to the parcel layer
    ParcelGridJoin = "ParcelGridJoin_" + dateTag
    arcpy.AddMessage('Running a spatial join on the Parcels and Fishnet Grid')
    arcpy.AddMessage('------------')
    arcpy.SpatialJoin_analysis(target_features=ParcelProj, join_features=fishnetFileName,
                               out_feature_class=ParcelGridJoin,
                               join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",
                               match_option='HAVE_THEIR_CENTER_IN')
    time.sleep(1)  # gives a 1 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    ### join the parcel data and the parcel grid join so we can calculate the GRID_ID field

    # Add Grid field to the incoming parcel data
    Grid = "Grid2"
    addFields(ParcelProj, Grid, "LONG", "Grid2")

    # Add HUC 8 field to the incoming parcel data
    HUC8 = "HUC_8_RES"
    addFields(ParcelProj, HUC8, "TEXT", "HUC 8 RES")

    # Join the parcel data and the parcel grid spatial join data
    ParcelFeatureLayer = "ParcelFeatureLayer_" + dateTag  # create a copy of our parcel data as a feature layer so we can join
    arcpy.MakeFeatureLayer_management(ParcelProj, ParcelFeatureLayer)
    arcpy.AddMessage('Joining the Parcels with the spatially joined Parcel/Grid table')
    arcpy.AddMessage('------------')
    arcpy.AddJoin_management(in_layer_or_view=ParcelFeatureLayer, in_field=FID_FieldName_1, join_table=ParcelGridJoin,
                             join_field=FID_FieldName_1, join_type="KEEP_ALL")
    time.sleep(1)  # gives a 1 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    ## Calculate the Grid ID from the joined table Grid ID
    CalcParcelGridField = os.path.basename(os.path.normpath(ParcelProj)) + "." + Grid
    CalcGridField = ParcelGridJoin + "." + Grid_FID
    arcpy.AddMessage('Calculating the GRID ID field for the Parcel layer and removing join')
    arcpy.AddMessage('------------')
    arcpy.CalculateField_management(in_table=ParcelFeatureLayer, field=CalcParcelGridField,
                                    expression="!" + CalcGridField + "!", expression_type="PYTHON3", code_block="")
    arcpy.RemoveJoin_management(in_layer_or_view=ParcelFeatureLayer)
    time.sleep(1)  # gives a .5 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    ##### Add HUC8 numbers to our parcel layer #####
    ## copy the HUC 8 data to our geodatabase - select any intersecting HUCs and export them to a new FC
    HUC8_Copy_FC = "HUC8_Copy_FC"  # Create filename and we'll copy our incoming HUC8 FC to our output GDB so we can edit it
    #HUC8_Selection = arcpy.SelectLayerByLocation_management(HUC8_FC, "INTERSECT", ParcelProj)
    #matchcount = int(arcpy.GetCount_management(HUC8_Selection)[0])
    arcpy.CopyFeatures_management(HUC8_FC, HUC8_Copy_FC)
    arcpy.AddMessage('Copying our intersected HUC watersheds to {}'.format(HUC8_Copy_FC))
    arcpy.AddMessage('------------')
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    ### add a "HUC8_RES" field to the HUC8 FC we just created, we'll copy the HUC8 values over from this field
    HUC8_RES = "HUC8_RES"
    addFields(HUC8_Copy_FC, HUC8_RES, "TEXT", HUC8_RES)
    arcpy.CalculateField_management(in_table=HUC8_Copy_FC, field=HUC8_RES,
                                    expression="!" + HUC8_FC_FieldName + "!", expression_type="PYTHON3", code_block="")
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    ## run a spatial join on the parcels and the HUC8 FC
    ParcelHUC8Join = "ParcelHUC8Join_" + dateTag
    arcpy.AddMessage('Running a spatial join on the Parcels and HUC8 layer')
    arcpy.AddMessage('------------')
    arcpy.SpatialJoin_analysis(target_features=ParcelProj, join_features=HUC8_Copy_FC,
                               out_feature_class=ParcelHUC8Join, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",
                               match_option='HAVE_THEIR_CENTER_IN')
    time.sleep(1)  # gives a 1 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    ## join the parcels and the parcel/huc8 spatial join tables
    arcpy.AddMessage('Joining the Parcels with the spatially joined Parcel/HUC8 table')
    arcpy.AddMessage('------------')
    arcpy.AddJoin_management(in_layer_or_view=ParcelFeatureLayer, in_field=FID_FieldName_1, join_table=ParcelHUC8Join,
                             join_field=FID_FieldName_1, join_type="KEEP_ALL")
    time.sleep(1)  # gives a 1 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    ## Calculate the HUC8 field from the joined table HUC8
    CalcParcelHUC8Field = os.path.basename(os.path.normpath(ParcelProj)) + "." + HUC8
    CalcHUC8Field = ParcelHUC8Join + "." + HUC8_RES
    arcpy.AddMessage('Calculating the HUC8 field for the Parcel layer and removing join')
    arcpy.AddMessage('------------')
    arcpy.CalculateField_management(in_table=ParcelFeatureLayer, field=CalcParcelHUC8Field,
                                    expression="!" + CalcHUC8Field + "!", expression_type="PYTHON3", code_block="")
    arcpy.RemoveJoin_management(in_layer_or_view=ParcelFeatureLayer)
    time.sleep(1)  # gives a .5 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    ##export the updated layer to a new FC
    OutputFC_FileName = arcpy.ValidateTableName(OutputFC_FileName)  # make sure the output feature class name is legal
    arcpy.AddMessage('Export the updated Parcel layer to a new Feature Class: {}'.format(OutputFC_FileName))
    arcpy.AddMessage('------------')
    arcpy.CopyFeatures_management(ParcelFeatureLayer, OutputFC_FileName)
    time.sleep(1)  # gives a 1 second pause before going to the next step
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar

    ## Delete the two spatial join FCs we made and any other FCs we don't need anymore
    arcpy.Delete_management(ParcelHUC8Join)
    arcpy.Delete_management(ParcelGridJoin)
    arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar
    arcpy.AddMessage('HUC 8 and GRID process is complete')
    arcpy.AddMessage('########################')

    # add the final formatted feature class to the map
    p = arcpy.mp.ArcGISProject("CURRENT")
    promap = p.listMaps()[0]
    promap.addDataFromPath(os.path.join(FinalData_OutputGeodatabase, OutputFC_FileName))
    p.save()

if __name__ == '__main__':
    main()


##### ARCHIVE CODE

    # # add the HUC8 Selection feature class to the map
    # p = arcpy.mp.ArcGISProject("CURRENT")
    # promap = p.listMaps()[0]
    # promap.addDataFromPath(os.path.join(FinalData_OutputGeodatabase, HUC8_Selection_FC))
    # p.save()

    # # add the Grid feature class to the map
    # p = arcpy.mp.ArcGISProject("CURRENT")
    # promap = p.listMaps()[0]
    # promap.addDataFromPath(os.path.join(FinalData_OutputGeodatabase, fishnetFileName))
    # p.save()
    # time.sleep(1)  # gives a 1 second pause before going to the next step
    # arcpy.SetProgressorPosition()  # everywhere we put one of these is going to move us along on the progress bar