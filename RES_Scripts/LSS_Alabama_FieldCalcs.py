# Return a score that combines all our ranking fields
def rank(streams, canopyCoverB, landCoverP, landCoverB):
    # Set percentage multipliers
    stream_per = 12.5
    canopyCover_per = 4.25
    BufflandCover_per = 4.25
    ParcLandCover_per = 4
    #nwi_pwsl_per = 3.33

    if streams is 0:
        return 0
    else:
        perCalc = streams*stream_per + canopyCoverB*canopyCover_per + \
                  landCoverP*ParcLandCover_per + landCoverB*BufflandCover_per
        return perCalc

rank(!Stream_Linear_FeetR!,!Canopy_cover_riparian_bufferR!,!LULC_parcelR!,!LULC_bufferR!)

# convert null values to 0 for those fields that we're using to calc ranks
def calc(field):
    if field is None:
        return 0
    else:
        return field

# calculate the priority field letter scores
def priority(rankField):
    if rankField == 0:
        return None
    elif rankField >= 80:
        return 'A'
    elif rankField >= 75:
        return 'B'
    elif rankField >= 55:
        return 'C'
    elif rankField >= 40:
        return 'D'
    else:
        return 'E'

priority(!RankingAg_Percentage!)

##### UPDATE RANK SCORES

def Canopy_Parcel_Rank_Calc(Canopy_Mean, BufferAcreage):
    if BufferAcreage == 0:
        return 0
    else:
        if Canopy_Mean > 70:
            return 1
        elif Canopy_Mean > 40:
            return 2
        elif Canopy_Mean >= 20:
            return 3
        else:
            return 4

def LULC_Buffer_Rank_Calc(lulc, lc1, lc2, lc3, lc4, lc5, lc6, lc7, lc8, lc9, lc10, lc11, lc12, lc13, lc14, lc15, lc16):

    if(lulc == lc1 or lulc == lc4 or lulc == lc5 or lulc == lc13):
        return 0
    if(lulc == lc2 or lulc == lc3 or lulc == lc6 or lulc == lc10):
        return 0
    if(lulc == lc7 or lulc == lc8 or lulc == lc9):
        return 2
    if(lulc == lc11 or lulc == lc12 or lulc == lc14):
        return 3
    if(lulc == lc15 or lulc == lc16):
        return 4
    else:
        return 0

LULC_Buffer_Rank_Calc(!LULC_parcel!, "Open Water", "Developed, Open Space", "Developed, Low Intensity", "Developed, Medium Intensity",
                                     "Developed, High Intensity", "Barren Land", "Deciduous Forest", "Evergreen Forest", "Mixed Forest",
                                     "Woody Wetlands", "Herbaceous", "Shrub/Scrub", "Emergent Herbaceous Wetlands", "Grassland/Herbaceous", "Cultivated Crops", "Pasture/Hay")

LULC_Buffer_Rank_Calc(!LULC_riparian_buffer!, "Open Water", "Developed, Open Space", "Developed, Low Intensity", "Developed, Medium Intensity",
                                              "Developed, High Intensity", "Barren Land", "Deciduous Forest", "Evergreen Forest", "Mixed Forest",
                                              "Woody Wetlands", "Herbaceous", "Shrub/Scrub", "Emergent Herbaceous Wetlands", "Grassland/Herbaceous",
                                              "Cultivated Crops", "Pasture/Hay")

def Stream_Linear_Ft_Rank_Calc(Stream):

    if Stream < 5000:
        return 0
    elif Stream < 10000:
        return 1
    elif Stream < 12000:
        return 2
    elif Stream < 15000:
        return 3
    elif Stream >= 15000:
        return 4

Stream_Linear_Ft_Rank_Calc(!NHD!)

# Calculate Potential field
def calc(rankfield):
    if rankfield is None:
        return "No"
    else:
        return "Yes"

calc(!Priority_streams!)
