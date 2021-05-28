# Return a score that combines all our ranking fields
def rank(coastalzoneR, LCR, NWIPWSLR, RestorationR, PreservationR):
    # Set percentage multipliers
    restoration_per = 7.5
    other_per = 2.5

    if streams is 0:
        return 0
    else:
        perCalc = streams*stream_per +  canopyCoverB*other_per + \
                  landCoverP*other_per + landCoverB*other_per + Ecoregion * eco_per
        return perCalc

rank(!NHDR!,!Canopy_cover_riparian_bufferR!,!LULC_parcelR!,!LULC_bufferR!, !EcoregionR!)

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
    elif rankField >= 90:
        return 'A'
    elif rankField >= 80:
        return 'B'
    elif rankField >= 70:
        return 'C'
    elif rankField >= 60:
        return 'D'
    else:
        return 'E'

