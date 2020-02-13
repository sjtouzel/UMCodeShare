import arcpy
import os, time, datetime

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

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = True

# Script parameters
County = arcpy.GetParameterAsText(0) # county boundary FC or shapefile
CountyName = arcpy.GetParameterAsText(1) # get the county name so we can use to calculate the field later
Input_Parcels = arcpy.GetParameterAsText(2) # Get the parcel data to be processed
ParcelID_Column = arcpy.GetParameterAsText(3) # we'll select this column to calculate the field later
ParcelOwner_Column = arcpy.GetParameterAsText(3) # we'll select this column to calculate the field later
FinalData_OutputGeodatabase = arcpy.GetParameterAsText(2) # This is where all of our output will be stored
Output_CoordinateSystem = arcpy.GetParameterAsText(3) # choose a state plane coordinate system
Minimum_ParcelAcreage = arcpy.GetParameterAsText(4)
StateName = arcpy.GetParameterAsText(5)


# REMOVE AFTER TESTING IS COMPLETE
County = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb\WilliamsonCounty" # this can be derived from the county boundary
CountyName = "Williamson"
Input_Parcels = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb\stratmap19_landparcels_48491_williamson_201905" # Get the parcel data to be processed
ParcelID_Column =
ParcelOwner_Column =
FinalData_OutputGeodatabase = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb" # This is where all of our output will be stored
Output_CoordinateSystem = r"C:\Users\jtouzel\AppData\Roaming\Esri\Desktop10.6\ArcMap\Coordinate Systems\NAD_1983_StatePlane_Texas_Central_FIPS_4203_Feet.prj"
Minimum_ParcelAcreage = 5
StateName = "Texas"



#Reproject all incoming data
arcpy.AddMessage('Reprojecting input County, {}'.format(os.path.basename(os.path.normpath(County))))
arcpy.env.workspace = FinalData_OutputGeodatabase
CountyProj = os.path.basename(os.path.normpath(County)) + "_Proj"
time.sleep(1)  # gives a .5 second pause before going to the next step
arcpy.AddMessage('Output is: {}'.format(CountyProj))
arcpy.Project_management(County, CountyProj, Output_CoordinateSystem)
arcpy.AddMessage('Reprojecting input Parcels, {}'.format(os.path.basename(os.path.normpath(Input_Parcels))))
ParcelProj = os.path.basename(os.path.normpath(Input_Parcels)) + "_Proj"
arcpy.Project_management(Input_Parcels, ParcelProj, Output_CoordinateSystem)
time.sleep(1)  # gives a 1 second pause before going to the next step
arcpy.AddMessage('Output is: {}'.format(ParcelProj))

#Add fields to our Projected Parcel Layer
##add a field to the parcel layer called Land_agent
LandAgent = "Land_agent"
arcpy.AddMessage('Adding a Land Agent field to the Parcel Layer. Field Name: {}'.format(LandAgent))
arcpy.AddField_management(in_table=ParcelProj, field_name=LandAgent, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Date_contacted
DateContacted = "Date_contacted"
arcpy.AddMessage('Adding a Date Contacted field to the Parcel Layer. Field Name: {}'.format(DateContacted))
arcpy.AddField_management(in_table=ParcelProj, field_name=DateContacted, field_type="DATE", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Land_status
LandStatus = "Land_status"
arcpy.AddMessage('Adding a Land Status field to the Parcel Layer. Field Name: {}'.format(LandStatus))
arcpy.AddField_management(in_table=ParcelProj, field_name=LandStatus, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Deal_type
DealType = "Deal_type"
arcpy.AddMessage('Adding a Deal Type field to the Parcel Layer. Field Name: {}'.format(DealType))
arcpy.AddField_management(in_table=ParcelProj, field_name=DealType, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Legal_status
LegalStatus = "Legal_status"
arcpy.AddMessage('Adding a Legal Status field to the Parcel Layer. Field Name: {}'.format(LegalStatus))
arcpy.AddField_management(in_table=ParcelProj, field_name=LegalStatus, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Site_protection_instrument_filed
SiteProtection = "Site_protection_instrument_filed"
arcpy.AddMessage('Adding a Site Protection Instrument Filed field to the Parcel Layer. Field Name: {}'.format(SiteProtection))
arcpy.AddField_management(in_table=ParcelProj, field_name=LegalStatus, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Notes
Notes = "Notes"
arcpy.AddMessage('Adding a Notes field to the Parcel Layer. Field Name: {}'.format(Notes))
arcpy.AddField_management(in_table=ParcelProj, field_name=Notes, field_type="TEXT", field_precision="",
                          field_scale="", field_length=2000, field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Attachments
Attachments = "Attachments"
arcpy.AddMessage('Adding a Attachments field to the Parcel Layer. Field Name: {}'.format(Attachments))
arcpy.AddField_management(in_table=ParcelProj, field_name=Attachments, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Survey123
Survey123 = "Survey123"
arcpy.AddMessage('Adding a Survey123 field to the Parcel Layer. Field Name: {}'.format(Survey123))
arcpy.AddField_management(in_table=ParcelProj, field_name=Survey123, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called State
StateField = "State"
arcpy.AddMessage('Adding a State field to the Parcel Layer. Field Name: {}'.format(StateField))
arcpy.AddField_management(in_table=ParcelProj, field_name=StateField, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
arcpy.AddMessage('Calculating the State field as: {}'.format(StateName))
arcpy.CalculateField_management(in_table=ParcelProj, field=StateField, expression='"{}"'.format(StateName),
                                expression_type="PYTHON3", code_block="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called State
CountyField = "County"
arcpy.AddMessage('Adding a County field to the Parcel Layer. Field Name: {}'.format(CountyField))
arcpy.AddField_management(in_table=ParcelProj, field_name=CountyField, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
arcpy.AddMessage('Calculating the County field as: {}'.format(CountyName))
arcpy.CalculateField_management(in_table=ParcelProj, field=CountyField, expression='"{}"'.format(CountyName),
                                expression_type="PYTHON3", code_block="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Job_code
JobCode = "Job_code"
arcpy.AddMessage('Adding a Job Code field to the Parcel Layer. Field Name: {}'.format(JobCode))
arcpy.AddField_management(in_table=ParcelProj, field_name=JobCode, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Parcel_ID
ParcelID = "Parcel_ID"
arcpy.AddMessage('Adding a Parcel ID field to the Parcel Layer. Field Name: {}'.format(ParcelID))
arcpy.AddField_management(in_table=ParcelProj, field_name=ParcelID, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
arcpy.AddMessage('Calculating the Parcel ID field from the field, {}, from the imported parcel data'.format(ParcelID_Column))
arcpy.CalculateField_management(in_table=ParcelProj, field=CountyField, expression="!" + ParcelID_Column + "!",
                                expression_type="PYTHON3", code_block="")
time.sleep(1)  # gives a 1 second pause before going to the next step