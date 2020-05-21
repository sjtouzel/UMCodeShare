# Return a score that combines all our ranking fields
def rank(streams, canopyCoverP, canopyCoverB, landCoverP, landCoverB, nwi_pwsl):
    # Set percentage multipliers
    stream_per = 12.5
    canopyCover_per = 3.33
    landCover_per = 2.5
    nwi_pwsl_per = 3.33

    if streams is 0:
        return 0
    else:
        perCalc = streams*stream_per + canopyCoverP*canopyCover_per + canopyCoverB*canopyCover_per + \
                  landCoverP*landCover_per + landCoverB*landCover_per + nwi_pwsl * nwi_pwsl_per
        return perCalc

rank(!Stream_Linear_FeetR!,!Canopy_cover_parcelR!,!Canopy_cover_riparian_bufferR!,!LULC_parcelR!,!LULC_bufferR!,!NWI_PWSLR!)

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

