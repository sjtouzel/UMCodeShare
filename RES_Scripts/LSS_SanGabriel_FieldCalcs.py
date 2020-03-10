# Return a score that combines all our ranking fields
def rank(streams, input2, input3, input4, input5):
    stream_per = 10
    input_per = 3.75
    if streams is 0:
        return 0
    else:
        perCalc = streams*stream_per + input2*input_per + input3*input_per + input4*input_per + input5*input_per
        return perCalc

rank(!Stream_Linear_FeetR!,!Canopy_cover_parcelR!,!Canopy_cover_riparian_bufferR!,!LULC_bufferR!,!LULC_parcelR!)

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
    elif rankField >= 65:
        return 'B'
    elif rankField >= 55:
        return 'C'
    elif rankField >= 42.5:
        return 'D'
    else:
        return 'E'

