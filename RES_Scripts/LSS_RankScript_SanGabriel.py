#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      tduong
#
# Created:     10/01/2020
# Copyright:   (c) tduong 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

'''
This script is based on a model made in Model Builder for ArcGIS by Amy
Ferguson for RES. The model takes a parcel data set and adds a standard
set of fields that are used to rank parcels in the RES land search system.
The ranking categories are multiplied together to calculate a final ranking.
Current script written by Katherine Clark, July 2019.
'''

import arcpy


def Add_Rank_Fields(parcel_input):
    new_fields = ['Canopy_cover_parcelR',
                  'Canopy_cover_riparian_bufferR',
                  'Stream_Linear_FeetR',
                  'LULC_bufferR',
                  'LULC_parcelR',
                  'NWI_PWSLR',
                  'WetlandRestR',
                  'WetlandPresR',
                  'LF_Strm_HWR',
                  'NHDR',
                  'PriorityR']

    attribute_type = 'SHORT'
    for field in new_fields:
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

    val = 1

    if Stream < 5000:
        val = 0
    elif Stream < 7000:
        val = 1
    elif Stream < 8000:
        val = 2
    elif Stream < 9000:
        val = 3
    elif Stream > 9000:
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

def NWI_PWSL_Rank_Calc(Tot_ac_pot):

    val = 1

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

    val = 1

    if NHD < 4000:
        val = 1
    elif NHD < 6000:
        val = 2
    elif NHD < 9000:
        val = 3
    elif NHD >= 9001:
        val = 4
    
    return val

def main():

    county_parcel_data = arcpy.GetParameterAsText(0)

    Add_Rank_Fields(county_parcel_data)

    fields = ['Canopy_cover_parcel', 'Canopy_cover_parcelR']
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = Canopy_Parcel_Rank_Calc(row[0])
            row[1] = rank_val
            cursor.updateRow(row)

    fields = ['Canopy_cover_riparian_buffer', 'Canopy_cover_riparian_bufferR']
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = Canopy_Buffer_Rank_Calc(row[0])
            row[1] = rank_val
            cursor.updateRow(row)

    fields = ['Stream_Linear_Feet', 'Stream_Linear_FeetR']
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = Stream_Linear_Ft_Rank_Calc(row[0])
            row[1] = rank_val
            cursor.updateRow(row)

    fields = ['LULC_riparian_buffer', 'LULC_bufferR']
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = LULC_Buffer_Rank_Calc(row[0], "Open Water", "Developed, Open Space", "Developed, Low Intensity", "Developed, Medium Intensity", "Developed, High Intensity", "Barren Land", "Deciduous Forest", "Evergreen Forest", "Mixed Forest", "Woody Wetlands", "Herbaceuous", "Shrub/Scrub", "Emergent Herbaceuous Wetlands", "Cultivated Crops", "Hay/Pasture")
            row[1] = rank_val
            cursor.updateRow(row)

    fields = ['LULC_parcel', 'LULC_parcelR']
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = LULC_Parcel_Rank_Calc(row[0], "Open Water", "Developed, Open Space", "Developed, Low Intensity", "Developed, Medium Intensity", "Developed, High Intensity", "Barren Land", "Deciduous Forest", "Evergreen Forest", "Mixed Forest", "Woody Wetlands", "Herbaceuous", "Shrub/Scrub", "Emergent Herbaceuous Wetlands", "Cultivated Crops", "Hay/Pasture")
            row[1] = rank_val
            cursor.updateRow(row)

    fields = ['Tot_ac_pot', 'NWI_PWSLR']
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = NWI_PWSL_Rank_Calc(row[0])
            row[1] = rank_val
            cursor.updateRow(row)

    fields = ['Restor', 'WetlandRestR']
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = Restoration_Rank_Calc(row[0])
            row[1] = rank_val
            cursor.updateRow(row)

    fields = ['Preserv', 'WetlandPresR']
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = Preservation_Rank_Calc(row[0])
            row[1] = rank_val
            cursor.updateRow(row)

    fields = ['LF_Strm_HW', 'LF_Strm_HWR']
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = LF_Strm_HW_Calc(row[0])
            row[1] = rank_val
            cursor.updateRow(row)

    fields = ['NHD', 'NHDR']
    with arcpy.da.UpdateCursor(county_parcel_data, fields) as cursor:
        for row in cursor:
            rank_val = NHD_Calc(row[0])
            row[1] = rank_val
            cursor.updateRow(row)
            
if __name__ == '__main__':
    main()

