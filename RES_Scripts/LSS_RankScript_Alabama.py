import arcpy
import time

"""
========================================================================
LSS_RankScript_Alabama.py
========================================================================
Author: Joe Touzel
========================================================================
Date			Modifier	Description of Change
2019/07/01      KC          Published
2019/12/26  	JT			Modified
2020/05/21      JT          Alabama updates
========================================================================
Description:
This script is based on a model made in Model Builder for ArcGIS by Amy
Ferguson for RES. The model takes a parcel data set and adds a standard
set of fields that are used to rank parcels in the RES land search system.
The ranking categories are multiplied together to calculate a final ranking.
Current script written by Katherine Clark, July 2019.

Inputs:
- Parcel Data with spatial analysis and Publishing Prep complete
- Rank classes as specified by the Land Search Request
"""




def Add_Rank_Fields(parcel_input):
    new_fields = ['Canopy_cover_parcelR',
                  'Canopy_cover_riparian_bufferR',
                  'Stream_Linear_FeetR',
                  'LULC_bufferR',
                  'LULC_parcelR',
                  'NWI_PWSLR']
                  # 'WetlandRestR',
                  # 'WetlandPresR',
                  # 'LF_Strm_HWR',
                  # 'NHDR',
                  # 'PriorityR']

    attribute_type = 'SHORT'
    for field in new_fields:
        arcpy.AddMessage("Adding field: {}".format(field))  # print the field we're adding
        arcpy.AddField_management(parcel_input, field_name=field,
                                  field_type=attribute_type)



def Canopy_Parcel_Rank_Calc(Canopy_Mean):

    val = 1

    if Canopy_Mean < 50:
        val = 3
    elif Canopy_Mean >= 50:
        val = 1

    return val

def Canopy_Buffer_Rank_Calc(Canopy_Buffer_Mean):

    val = 1

    if Canopy_Buffer_Mean < 50:
        val = 3
    elif Canopy_Buffer_Mean >= 50:
        val = 1

    return val


def Stream_Linear_Ft_Rank_Calc(Stream):
    val = 0

    if Stream < 15000:
        val = 0
    elif Stream < 16000:
        val = 1
    elif Stream < 17000:
        val = 2
    elif Stream < 18000:
        val = 3
    elif Stream > 18001:
        val = 4

    return val


def LULC_Buffer_Rank_Calc(lulc, lc1, lc2, lc3, lc4, lc5, lc6, lc7, lc8, lc9, lc10, lc11, lc12, lc13, lc14, lc15):

    val = 1

    if(lulc == lc1 or lulc == lc4 or lulc == lc5):
        val = 0
    if(lulc == lc2 or lulc == lc3 or lulc == lc6 or lulc == lc10 or lulc == lc13):
        val = 1
    if(lulc == lc7 or lulc == lc8 or lulc == lc9):
        val = 2
    if(lulc == lc11 or lulc == lc12):
        val = 3
    if(lulc == lc14 or lulc == lc15):
        val = 4

    return val

def LULC_Parcel_Rank_Calc(lulc, lc1, lc2, lc3, lc4, lc5, lc6, lc7, lc8, lc9, lc10, lc11, lc12, lc13, lc14, lc15):

    val = 1

    if(lulc == lc1 or lulc == lc4 or lulc == lc5):
        val = 0
    if(lulc == lc2 or lulc == lc3 or lulc == lc6 or lulc == lc10 or lulc == lc13):
        val = 1
    if(lulc == lc7 or lulc == lc8 or lulc == lc9):
        val = 2
    if(lulc == lc11 or lulc == lc12):
        val = 3
    if(lulc == lc14 or lulc == lc15):
        val = 4

    return val

def NWI_PWSL_Rank_Calc(nwi, pwsl):

    val = 1
    Tot_ac_pot = nwi + pwsl

    if Tot_ac_pot < 20:
        val = 1
    elif Tot_ac_pot < 40:
        val = 2
    elif Tot_ac_pot < 60:
        val = 3
    elif Tot_ac_pot >= 60:
        val = 4
    return val

def Restoration_Rank_Calc(Restor):

    val = 1

    if Restor < 1:
        val = 1
    elif Restor < 5:
        val = 2
    elif Restor < 10:
        val = 3
    elif Restor >= 15:
        val = 4

    return val

def Preservation_Rank_Calc(Preserv):

    val = 1

    if Preserv > 0:
        val = 2
    
    return val

def LF_Strm_HW_Calc(LF_Strm_HW):

    val = 1

    if LF_Strm_HW < 1000:
        val = 1
    elif LF_Strm_HW < 2000:
        val = 2
    elif LF_Strm_HW < 3000:
        val = 3
    elif LF_Strm_HW >= 3000:
        val = 4

    return val

def NHD_Calc(NHD):

    val = 0

    if NHD < 15000:
        val = 0
    elif NHD < 16000:
        val = 1
    elif NHD < 17000:
        val = 2
    elif NHD < 18000:
        val = 3
    elif NHD > 18001:
        val = 4
    
    return val

def main():

    county_parcel_data = arcpy.GetParameterAsText(0)

    # Write to Log
    arcpy.AddMessage('')
    arcpy.AddMessage("===================================================================")
    sVersionInfo = 'LSS_RankScript_Alabama.py, v20200521'
    arcpy.AddMessage('LSS Ranking Script, {}'.format(sVersionInfo))
    arcpy.AddMessage("")
    arcpy.AddMessage("Support: jtouzel@res.us, 281-715-9109")
    arcpy.AddMessage("")
    arcpy.AddMessage("Input FC: {}".format(county_parcel_data))
    field_names = [f.name for f in arcpy.ListFields(county_parcel_data)]
    arcpy.AddMessage("Field Names: {}".format(", ".join(field_names)))
    arcpy.AddMessage("===================================================================")


    Add_Rank_Fields(county_parcel_data)

    fields = ['Canopy_cover_parcel', 'Canopy_cover_parcelR']
    arcpy.AddMessage("===================================================================")
    arcpy.AddMessage("Calculate Parcel Canopy Cover Ranking")  # Print the Ranking info for Parcel Canopy
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = Canopy_Parcel_Rank_Calc(row[0])
            row[1] = rank_val
            cursor.updateRow(row)
    time.sleep(1)  # gives a 1 second pause before going to the next step

    fields = ['Canopy_cover_riparian_buffer', 'Canopy_cover_riparian_bufferR']
    arcpy.AddMessage("===================================================================")
    arcpy.AddMessage("Calculate Buffer Canopy Cover Ranking")  # Print the Ranking info for Buffer Canopy
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = Canopy_Buffer_Rank_Calc(row[0])
            row[1] = rank_val
            cursor.updateRow(row)
    time.sleep(1)  # gives a 1 second pause before going to the next step

    fields = ['NHD', 'Stream_Linear_FeetR']
    arcpy.AddMessage("===================================================================")
    arcpy.AddMessage("Calculate NHD Stream LF Ranking")  # Print the Ranking info
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = Stream_Linear_Ft_Rank_Calc(row[0])
            row[1] = rank_val
            cursor.updateRow(row)
    time.sleep(1)  # gives a 1 second pause before going to the next step

    fields = ['LULC_riparian_buffer', 'LULC_bufferR']
    arcpy.AddMessage("===================================================================")
    arcpy.AddMessage("Calculate Buffer LULC Ranking")  # Print the Ranking info
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = LULC_Buffer_Rank_Calc(row[0], "Open Water", "Developed, Open Space", "Developed, Low Intensity", "Developed, Medium Intensity", "Developed, High Intensity", "Barren Land", "Deciduous Forest", "Evergreen Forest", "Mixed Forest", "Woody Wetlands", "Herbaceuous", "Shrub/Scrub", "Emergent Herbaceuous Wetlands", "Cultivated Crops", "Hay/Pasture")
            row[1] = rank_val
            cursor.updateRow(row)
    time.sleep(1)  # gives a 1 second pause before going to the next step

    fields = ['LULC_parcel', 'LULC_parcelR']
    arcpy.AddMessage("===================================================================")
    arcpy.AddMessage("Calculate Parcel LULC Ranking")  # Print the Ranking info
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = LULC_Parcel_Rank_Calc(row[0], "Open Water", "Developed, Open Space", "Developed, Low Intensity", "Developed, Medium Intensity", "Developed, High Intensity", "Barren Land", "Deciduous Forest", "Evergreen Forest", "Mixed Forest", "Woody Wetlands", "Herbaceous", "Shrub/Scrub", "Emergent Herbaceous Wetlands", "Cultivated Crops", "Hay/Pasture")
            row[1] = rank_val
            cursor.updateRow(row)
    time.sleep(1)  # gives a 1 second pause before going to the next step

    fields = ['NWI_acres','PWSL_acres', 'NWI_PWSLR']
    arcpy.AddMessage("===================================================================")
    arcpy.AddMessage("Calculate NWI PWSL Ranking")  # Print the Ranking info
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = NWI_PWSL_Rank_Calc(row[0], row[1])
            row[2] = rank_val
            cursor.updateRow(row)
    time.sleep(1)  # gives a 1 second pause before going to the next step

    # fields = ['Restor', 'WetlandRestR']
    # arcpy.AddMessage("===================================================================")
    # arcpy.AddMessage("Calculate Restoration Rank Ranking")  # Print the Ranking info
    # with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
    #     for row in cursor:
    #         rank_val = Restoration_Rank_Calc(row[0])
    #         row[1] = rank_val
    #         cursor.updateRow(row)
    # time.sleep(1)  # gives a 1 second pause before going to the next step

    # fields = ['Preserv', 'WetlandPresR']
    # arcpy.AddMessage("===================================================================")
    # arcpy.AddMessage("Calculate Preservation Ranking")  # Print the Ranking info
    # with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
    #     for row in cursor:
    #         rank_val = Preservation_Rank_Calc(row[0])
    #         row[1] = rank_val
    #         cursor.updateRow(row)
    # time.sleep(1)  # gives a 1 second pause before going to the next step

    # fields = ['LF_Strm_HW', 'LF_Strm_HWR']
    # arcpy.AddMessage("===================================================================")
    # arcpy.AddMessage("Calculate Stream Headwater Ranking")  # Print the Ranking info
    # with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
    #     for row in cursor:
    #         rank_val = LF_Strm_HW_Calc(row[0])
    #         row[1] = rank_val
    #         cursor.updateRow(row)
    # time.sleep(1)  # gives a 1 second pause before going to the next step

    # fields = ['NHD', 'NHDR']
    # arcpy.AddMessage("===================================================================")
    # arcpy.AddMessage("Calculate NHD stream LF Ranking")  # Print the Ranking info
    # with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
    #     for row in cursor:
    #         rank_val = NHD_Calc(row[0])
    #         row[1] = rank_val
    #         cursor.updateRow(row)
    # time.sleep(1)  # gives a 1 second pause before going to the next step
            
if __name__ == '__main__':
    main()

