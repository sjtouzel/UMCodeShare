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
ParcelOwner_Column = arcpy.GetParameterAsText(4) # we'll select this column to calculate the field later
ParcelAddress_Column = arcpy.GetParameterAsText(5) # make it a SQL expression paramater in case the address field needs to be concatenated
FinalData_OutputGeodatabase = arcpy.GetParameterAsText(5) # This is where all of our output will be stored
Output_CoordinateSystem = arcpy.GetParameterAsText(6) # choose a state plane coordinate system
Minimum_ParcelAcreage = arcpy.GetParameterAsText(7) # a minimum acreage for our incoming parcel data
StateName = arcpy.GetParameterAsText(8)
JobCodeInput = arcpy.GetParameterAsText(9) # this will be supplied by the PM requesting the Land Search
TotalCostField = arcpy.GetParameterAsText(9) # we'll select this column to calculate the field later
MailStateField = arcpy.GetParameterAsText(9) # we'll select this column to calculate the field later

#REMOVE AFTER TESTING IS COMPLETE
County = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb\WilliamsonCounty" # this can be derived from the county boundary
CountyName = "Williamson"
Input_Parcels = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb\stratmap19_landparcels_48491_williamson_201905" # Get the parcel data to be processed
ParcelID_Column = "PROP_ID"
ParcelOwner_Column = "OWNER_NAME"
ParcelAddress_Column = "SITUS_ADDR"
FinalData_OutputGeodatabase = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb" # This is where all of our output will be stored
Output_CoordinateSystem = r"C:\Users\jtouzel\AppData\Roaming\Esri\Desktop10.6\ArcMap\Coordinate Systems\NAD_1983_StatePlane_Texas_Central_FIPS_4203_Feet.prj"
Minimum_ParcelAcreage = 5
StateNameABBR = "TX"
JobCodeInput = "1234"
TotalCostField = "GIS_AREA"
MailStateField = "MAIL_STAT"

dateTag = datetime.datetime.today().strftime('%Y%m%d') # we'll tag some of our output with this. looks somethin like # this 20181213
StateListDictionary = {'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas','AS': 'American Samoa','AZ': 'Arizona','CA': 'California',
                       'CO': 'Colorado','CT': 'Connecticut','DC': 'District of Columbia','DE': 'Delaware','FL': 'Florida',
                       'GA': 'Georgia','GU': 'Guam','HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho','IL': 'Illinois','IN': 'Indiana',
                       'KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland',
                       'ME': 'Maine','MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MP': 'Northern Mariana Islands',
                       'MS': 'Mississippi','MT': 'Montana','NA': 'National','NC': 'North Carolina','ND': 'North Dakota',
                       'NE': 'Nebraska','NH': 'New Hampshire','NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada',
                       'NY': 'New York','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','RI': 'Rhode Island',
                       'SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah',
                       'VA': 'Virginia','VI': 'Virgin Islands','VT': 'Vermont','WA': 'Washington','WI': 'Wisconsin',
                       'WV': 'West Virginia','WY': 'Wyoming'}

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

##add a field to the parcel layer called County
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
if JobCodeInput:
    arcpy.AddMessage('Calculating the Job Code field as: {}'.format(JobCodeInput))
    arcpy.CalculateField_management(in_table=ParcelProj, field=JobCode, expression='"{}"'.format(JobCodeInput),
                                    expression_type="PYTHON3", code_block="")
    time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Parcel_ID
ParcelID = "Parcel_ID"
arcpy.AddMessage('Adding a Parcel ID field to the Parcel Layer. Field Name: {}'.format(ParcelID))
arcpy.AddField_management(in_table=ParcelProj, field_name=ParcelID, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
if ParcelID_Column:
    arcpy.AddMessage('Calculating the Parcel ID field from the field, {}, from the imported parcel data'.format(ParcelID_Column))
    arcpy.CalculateField_management(in_table=ParcelProj, field=ParcelID, expression="!" + ParcelID_Column + "!",
                                    expression_type="PYTHON3", code_block="")
    time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Parcel_owner
ParcelOwner = "Parcel_owner"
arcpy.AddMessage('Adding a Parcel Owner field to the Parcel Layer. Field Name: {}'.format(ParcelOwner))
arcpy.AddField_management(in_table=ParcelProj, field_name=ParcelOwner, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
if ParcelOwner_Column:
    arcpy.AddMessage('Calculating the Parcel Owner field from the field, {}, from the imported parcel data'.format(ParcelOwner_Column))
    arcpy.CalculateField_management(in_table=ParcelProj, field=ParcelOwner, expression="!" + ParcelOwner_Column + "!",
                                    expression_type="PYTHON3", code_block="")
    time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Parcel_address
ParcelAddress = "Parcel_address"
arcpy.AddMessage('Adding a Parcel Address field to the Parcel Layer. Field Name: {}'.format(ParcelAddress))
arcpy.AddField_management(in_table=ParcelProj, field_name=ParcelAddress, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
if ParcelAddress_Column:
    arcpy.AddMessage('Calculating the Parcel Address field from the field, {}, from the imported parcel data'.format(ParcelAddress_Column))
    arcpy.CalculateField_management(in_table=ParcelProj, field=ParcelAddress, expression="!" + ParcelAddress_Column + "!",
                                    expression_type="PYTHON3", code_block="")
    time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Parcel_acreage
ParcelAcreage = "Parcel_acreage"
arcpy.AddMessage('Adding a Parcel Acreage field to the Parcel Layer. Field Name: {}'.format(ParcelAcreage))
arcpy.AddField_management(in_table=ParcelProj, field_name=ParcelAcreage, field_type="FLOAT", field_precision="",
                          field_scale=2, field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
arcpy.AddMessage('Calculating the Parcel Acreage')
arcpy.CalculateField_management(in_table=ParcelProj, field=ParcelAcreage, expression="!shape.area@acres!",
                                expression_type="PYTHON3", code_block="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Total_cost
TotalCost = "Total_cost"
arcpy.AddMessage('Adding a Total Cost field to the Parcel Layer. Field Name: {}'.format(TotalCost))
arcpy.AddField_management(in_table=ParcelProj, field_name=TotalCost, field_type="FLOAT", field_precision="",
                          field_scale=2, field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
if TotalCostField:
    arcpy.AddMessage('Calculating the Total Cost field from the field, {}, from the imported parcel data'.format(
        TotalCostField))
    arcpy.CalculateField_management(in_table=ParcelProj, field=TotalCost,
                                    expression="!" + TotalCostField + "!",
                                    expression_type="PYTHON3", code_block="")
    time.sleep(1)  # gives a 1 second pause before going to the next step
##add a field to the parcel layer called Cost_per_acre
CostPerAcre = "Cost_per_acre"
arcpy.AddMessage('Adding a Cost Per Acre field to the Parcel Layer. Field Name: {}'.format(CostPerAcre))
arcpy.AddField_management(in_table=ParcelProj, field_name=CostPerAcre, field_type="DOUBLE", field_precision="",
                          field_scale=2, field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
if TotalCostField:
    arcpy.AddMessage('Calculating the Cost Per Acre field from the this equation: {} / {}'.format(
        TotalCost,ParcelAcreage))
    arcpy.CalculateField_management(in_table=ParcelProj, field=TotalCost,
                                    expression="!" + TotalCost + "!" + " / " + "!" + ParcelAcreage + "!",
                                    expression_type="PYTHON3", code_block="")
    time.sleep(1)  # gives a 1 second pause before going to the next step
##add a field to the parcel layer called Owner_type
OwnerType = "Owner_type"
arcpy.AddMessage('Adding a Owner Type field to the Parcel Layer. Field Name: {}'.format(OwnerType))
arcpy.AddField_management(in_table=ParcelProj, field_name=OwnerType, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
### Now we'll calculate this Owner Type field
corporationStringList = ["llc", "lllp", "l l l p", "inc", " co", "lp", "corporation", "corp", "association", "l l c"]
with arcpy.da.UpdateCursor(ParcelProj, [ParcelOwner, OwnerType]) as cursor1:  # look through point FC to get the related info for each photo
    for row in cursor1:
        if "city" in row[0].lower():
            row[1] = "Municipal"
        elif "county" in row[0].lower():
            row[1] = "County"
        elif "state" in row[0].lower():
            row[1] = "State"
        elif any(part in row[0].lower() for part in corporationStringList):
            row[1] = "Partnership/Corporation"
        else:
            row[1] = "Private individual"
        cursor1.updateRow(row)

##add a field to the parcel layer called Owner_on_off_site
OwnerOnOffSite = "Owner_on_off_site"
arcpy.AddMessage('Adding a Owner On/Off Site field to the Parcel Layer. Field Name: {}'.format(OwnerOnOffSite))
arcpy.AddField_management(in_table=ParcelProj, field_name=OwnerOnOffSite, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step
if MailStateField:
    arcpy.AddMessage('Calculating the Owner On/Off Site field from the this equation: {} / {}'.format(
        TotalCost,ParcelAcreage))
    arcpy.CalculateField_management(in_table=ParcelProj, field=TotalCost,
                                    expression="!" + TotalCost + "!" + " / " + "!" + ParcelAcreage + "!",
                                    expression_type="PYTHON3", code_block="")
    time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Grid2
Grid2 = "Grid2"
arcpy.AddMessage('Adding a Grid 2 field to the Parcel Layer. Field Name: {}'.format(Grid2))
arcpy.AddField_management(in_table=ParcelProj, field_name=Grid2, field_type="SHORT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called HUC_8
HUC8 = "HUC_8"
arcpy.AddMessage('Adding a HUC 8 field to the Parcel Layer. Field Name: {}'.format(HUC8))
arcpy.AddField_management(in_table=ParcelProj, field_name=HUC8, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Delivery_Factor_TN
DeliveryFactorTN = "Delivery_Factor_TN"
arcpy.AddMessage('Adding a Delivery Factor TN field to the Parcel Layer. Field Name: {}'.format(DeliveryFactorTN))
arcpy.AddField_management(in_table=ParcelProj, field_name=DeliveryFactorTN, field_type="DOUBLE", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Delivery_Factor_TP
DeliveryFactorTP = "Delivery_Factor_TP"
arcpy.AddMessage('Adding a Delivery Factor TP field to the Parcel Layer. Field Name: {}'.format(DeliveryFactorTP))
arcpy.AddField_management(in_table=ParcelProj, field_name=DeliveryFactorTP, field_type="DOUBLE", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Delivery_Factor_TSS
DeliveryFactorTSS = "Delivery_Factor_TSS"
arcpy.AddMessage('Adding a Delivery Factor TSS field to the Parcel Layer. Field Name: {}'.format(DeliveryFactorTSS))
arcpy.AddField_management(in_table=ParcelProj, field_name=DeliveryFactorTSS, field_type="DOUBLE", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Stream_linear_feet
StreamLinearFeet = "Stream_linear_feet"
arcpy.AddMessage('Adding a Stream Linear Feet field to the Parcel Layer. Field Name: {}'.format(StreamLinearFeet))
arcpy.AddField_management(in_table=ParcelProj, field_name=StreamLinearFeet, field_type="FLOAT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Stream_order
StreamOrder = "Stream_order"
arcpy.AddMessage('Adding a Stream Order field to the Parcel Layer. Field Name: {}'.format(StreamOrder))
arcpy.AddField_management(in_table=ParcelProj, field_name=StreamOrder, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Stream_Slope
StreamSlope = "Stream_Slope"
arcpy.AddMessage('Adding a Stream Slope field to the Parcel Layer. Field Name: {}'.format(StreamSlope))
arcpy.AddField_management(in_table=ParcelProj, field_name=StreamSlope, field_type="DOUBLE", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Buffer_acreage
BufferAcreage = "Buffer_acreage"
arcpy.AddMessage('Adding a Buffer Acreage field to the Parcel Layer. Field Name: {}'.format(BufferAcreage))
arcpy.AddField_management(in_table=ParcelProj, field_name=BufferAcreage, field_type="FLOAT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called LULC_parcel
LULCParcel = "LULC_parcel"
arcpy.AddMessage('Adding an LULC Parcel field to the Parcel Layer. Field Name: {}'.format(LULCParcel))
arcpy.AddField_management(in_table=ParcelProj, field_name=LULCParcel, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called LULC_riparian_buffer
LULCRiparianBuffer = "LULC_riparian_buffer"
arcpy.AddMessage('Adding an LULC Riparian Buffer field to the Parcel Layer. Field Name: {}'.format(LULCRiparianBuffer))
arcpy.AddField_management(in_table=ParcelProj, field_name=LULCRiparianBuffer, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Canopy_cover_parcel
CanopyCoverParcel = "Canopy_cover_parcel"
arcpy.AddMessage('Adding a Canopy Cover Parcel field to the Parcel Layer. Field Name: {}'.format(CanopyCoverParcel))
arcpy.AddField_management(in_table=ParcelProj, field_name=CanopyCoverParcel, field_type="FLOAT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Canopy_cover_riparian_buffer
CanopyCoverRB = "Canopy_cover_riparian_buffer"
arcpy.AddMessage('Adding a Canopy Cover Riparian Buffer field to the Parcel Layer. Field Name: {}'.format(CanopyCoverRB))
arcpy.AddField_management(in_table=ParcelProj, field_name=CanopyCoverRB, field_type="FLOAT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called NWI_acres
NWIAcres = "NWI_acres"
arcpy.AddMessage('Adding an NWI Acres field to the Parcel Layer. Field Name: {}'.format(NWIAcres))
arcpy.AddField_management(in_table=ParcelProj, field_name=NWIAcres, field_type="FLOAT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called NWI_percent
NWIPercent = "NWI_percent"
arcpy.AddMessage('Adding an NWI Percent field to the Parcel Layer. Field Name: {}'.format(NWIPercent))
arcpy.AddField_management(in_table=ParcelProj, field_name=NWIPercent, field_type="FLOAT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Soils
Soils = "Soils"
arcpy.AddMessage('Adding a Soils field to the Parcel Layer. Field Name: {}'.format(Soils))
arcpy.AddField_management(in_table=ParcelProj, field_name=Soils, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called FEMA_flood_zone
FEMAFZ = "FEMA_flood_zone"
arcpy.AddMessage('Adding a FEMA Flood Zone field to the Parcel Layer. Field Name: {}'.format(FEMAFZ))
arcpy.AddField_management(in_table=ParcelProj, field_name=FEMAFZ, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Critical_habitat
CriticalHabitat = "Critical_habitat"
arcpy.AddMessage('Adding a Critical Habitat field to the Parcel Layer. Field Name: {}'.format(CriticalHabitat))
arcpy.AddField_management(in_table=ParcelProj, field_name=CriticalHabitat, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Conservation_easement
ConservationEase = "Conservation_easement"
arcpy.AddMessage('Adding a Conservation Easement field to the Parcel Layer. Field Name: {}'.format(ConservationEase))
arcpy.AddField_management(in_table=ParcelProj, field_name=ConservationEase, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Priority_streams
PriorityStreams = "Priority_streams"
arcpy.AddMessage('Adding a Priority Streams field to the Parcel Layer. Field Name: {}'.format(PriorityStreams))
arcpy.AddField_management(in_table=ParcelProj, field_name=PriorityStreams, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Priority_wetlands
PriorityWetlands = "Priority_wetlands"
arcpy.AddMessage('Adding a Priority Wetlands field to the Parcel Layer. Field Name: {}'.format(PriorityWetlands))
arcpy.AddField_management(in_table=ParcelProj, field_name=PriorityWetlands, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Priority_nutrientbank
PriorityNutrientBank = "Priority_nutrientbank"
arcpy.AddMessage('Adding a Priority Nutrient Bank field to the Parcel Layer. Field Name: {}'.format(PriorityNutrientBank))
arcpy.AddField_management(in_table=ParcelProj, field_name=PriorityNutrientBank, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Priority_species
PrioritySpecies = "Priority_species"
arcpy.AddMessage('Adding a Priority Species field to the Parcel Layer. Field Name: {}'.format(PrioritySpecies))
arcpy.AddField_management(in_table=ParcelProj, field_name=PrioritySpecies, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Credit_yield_estimate_streams
CreditYieldES = "Credit_yield_estimate_streams"
arcpy.AddMessage('Adding a Credit Yield Estimate Streams field to the Parcel Layer. Field Name: {}'.format(CreditYieldES))
arcpy.AddField_management(in_table=ParcelProj, field_name=CreditYieldES, field_type="FLOAT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Credit_yield_estimate_wetland
CreditYieldEW = "Credit_yield_estimate_wetland"
arcpy.AddMessage('Adding a Credit Yield Estimate Wetland field to the Parcel Layer. Field Name: {}'.format(CreditYieldEW))
arcpy.AddField_management(in_table=ParcelProj, field_name=CreditYieldEW, field_type="FLOAT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Credit_yield_estimate_nutrient_bank
CreditYieldENB = "Credit_yield_estimate_nutrient_bank"
arcpy.AddMessage('Adding a Credit Yield Estimate Nutrient Bank field to the Parcel Layer. Field Name: {}'.format(CreditYieldENB))
arcpy.AddField_management(in_table=ParcelProj, field_name=CreditYieldENB, field_type="FLOAT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Property_subcode
PropertySubcode = "Property_subcode"
arcpy.AddMessage('Adding a Property Subcode field to the Parcel Layer. Field Name: {}'.format(PropertySubcode))
arcpy.AddField_management(in_table=ParcelProj, field_name=PropertySubcode, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##add a field to the parcel layer called Confidence_indicator
ConfidenceIndicator = "Confidence_indicator"
arcpy.AddMessage('Adding a Confidence Indicator field to the Parcel Layer. Field Name: {}'.format(ConfidenceIndicator))
arcpy.AddField_management(in_table=ParcelProj, field_name=ConfidenceIndicator, field_type="TEXT", field_precision="",
                          field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",
                          field_is_required="NON_REQUIRED", field_domain="")
time.sleep(1)  # gives a 1 second pause before going to the next step

##Filter out all parcels smaller than the Minimum_ParcelAcreage
ParcelFeatureLayerFilter = "ParcelFeatureLayerFilter" + dateTag
arcpy.MakeFeatureLayer_management(ParcelProj, ParcelFeatureLayerFilter)
arcpy.AddMessage('Filtering out all parcels less than {} acres'.format(Minimum_ParcelAcreage))
Selection1 = '"{}" >= {}'.format(ParcelAcreage,Minimum_ParcelAcreage)
arcpy.SelectLayerByAttribute_management(ParcelFeatureLayerFilter, 'NEW_SELECTION',
                                        Selection1)
ParcelFilter_FC = "ParcelFilterFC_" + dateTag
time.sleep(1)  # gives a 1 second pause before going to the next step
##copy the updated parcel layer to a new FC
arcpy.AddMessage('Export the updated Parcel layer to a new Feature Class: {}'.format(ParcelFilter_FC))
arcpy.CopyFeatures_management(ParcelFeatureLayerFilter, ParcelFilter_FC)
time.sleep(1)  # gives a .5 second pause before going to the next step


