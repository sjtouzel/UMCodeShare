# Return a score that combines all our ranking fields
def rank(streams, input2, input3, input4, input5):
    stream_per = 10
    input_per = 3.75
    if streams is 0:
        return 0
    else:
        perCalc = streams*stream_per + input2*input_per + input3*input_per + input4*input_per + input5*input_per
        return perCalc

# convert null values to 0 for those fields that we're using to calc ranks
def calc(field):
    if field is None:
        return 0
    else:
        return field
