# Return a score that combines all our ranking fields
def rank(coastalzoneR, LCR, NWIPWSLR, RestorationR, PreservationR, ManagedLandR, RestrictedR, ParcelsAcreageR):
    # Set percentage multipliers
    restoration_per = 7.5
    other_per = 2.5

    if 0 in (coastalzoneR, LCR, NWIPWSLR, RestorationR, PreservationR, ManagedLandR, RestrictedR, ParcelsAcreageR):
        return 0
    else:
        perCalc = RestorationR*restoration_per +  coastalzoneR*other_per + \
                  LCR*other_per + NWIPWSLR*other_per + PreservationR*other_per + ManagedLandR*other_per + \
                  RestrictedR*other_per + ParcelsAcreageR*other_per
        return perCalc

rank(!CoastalZone_R!,!LandCover_R!,!NWI_PWSL_R!,!RestorationAcres_R!,!PreservationAcres_R!,!ManagedLand_R!,!Restricted_R!,!ParcelAcreage_R!)

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


# testing biz
a = 1
b=2
c=4

if 0 in (a,b,c):
    print("YEs")

