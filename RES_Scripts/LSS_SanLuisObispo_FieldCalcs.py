# Return a score that combines all our ranking fields
def rank(CalcAcrR, input2, input3, input4, input5, input6, input7, input8, input9):
    ranking_per = 3.7
    Inputlist = [CalcAcrR, input2, input3, input4, input5, input6, input7, input8, input9]
    if CalcAcrR == 0:
        return 0
    else:
        score = 0
        for i in Inputlist:
            score += i*ranking_per
        return score

rank(!CalcAcrR!,!M_SJK_FoxR!,!BNLLR!,!CJFR!,!FRAP_OaksR!,!Gav_PlantR!,!GKRR!,!NAGSR!,!TKRR!)

# convert null values to 0 for those fields that we're using to calc ranks
def calc(field):
    if field is None:
        return 0
    else:
        return field

# calculate the priority field letter scores
def priority(rankField):
    if rankField == 0:
        return 'X'
    elif rankField >= 70:
        return 'A'
    elif rankField >= 55:
        return 'B'
    elif rankField >= 47.5:
        return 'C'
    elif rankField >= 40:
        return 'D'
    else:
        return 'E'

