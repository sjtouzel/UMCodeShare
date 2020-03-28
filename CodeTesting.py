import arcpy
from arcpy import env
import time, os

featureClass = ['in', 'out', 'up', 'down']
print("_".join(featureClass))
print("Field Names: {}".format(", ".join(featureClass)))

item1 = 'red'
item2 = 'blue'
item3 = ''

newlist = [item1, item2, item3]
newlist2 = [i for i in newlist if i]
if item2:
    print(True)


# extract raster by mask
arcpy.env.scratchWorkspace = r"C:"
scratchGDB = arcpy.env.scratchGDB # Path to scratch GDB
arcpy.env.overwriteOutput = True
nlcdGDB = r"E:\Dropbox (RES)\@RES GIS\Data\OK\OK_Vector\NLCD\OK_NLCD.gdb"
env.workspace = nlcdGDB
fc_list = arcpy.ListDatasets()
nlcd = os.path.join(nlcdGDB, fc_list[0])
maskGDB = r"E:\Dropbox (RES)\@RES GIS\projects\OK\PRJ101582_AEP_ABB_HCP_Phase1\SHP\ProjectData_20200116.gdb"
env.workspace = maskGDB
fc_list2 = arcpy.ListFeatureClasses()
mask = os.path.join(maskGDB, fc_list2[0])
outExtractByMask = arcpy.sa.ExtractByMask(nlcd, mask)


##### adjusting symbology #####
import arcpy
import pprint
project = arcpy.mp.ArcGISProject(r"C:\Users\jtouzel\Documents\ArcGIS\Projects\ProjectTemplate\ProjectTemplate.aprx") # access the current project
map_1 = project.listMaps("Map")[0] # get the first map called "Map" in the current project
for lyr in map_1.listLayers():
    print(lyr.name) # print out the names of all the layers in the map

# Making Unique Value Renderer updates
lyr = map_1.listLayers()[0] # get the first layer from the map
sym = lyr.symbology # access the layers symbology
sym.updateRenderer("UniqueValueRenderer")
sym.renderer.fields = ["NAME"]
lyr.symbology = sym

# adjust outline of polygon symbols
sym.renderer.symbol.applySymbolFromGallery("Extent Transparent Wide Gray")
sym.renderer.symbol.color = {'RGB' : [255, 0, 0, 60]}
sym.renderer.symbol.outlineColor = {'CMYK' : [25, 50, 75, 25, 100]}

# adjust just the transparency
lyr_3 = map_1.listLayers()[3] # select a layer
lyr_3.transparency = 30 # set the transparency

# Making Simple Renderer updates
lyr_2 = map_1.listLayers()[1]
sym_2 = lyr_2.symbology
sym_2.updateRenderer("SimpleRenderer")
sym_2.renderer.symbol.applySymbolFromGallery("Black Outline (1pt)")
lyr_2.symbology = sym_2

# get connection info about layer
pprint.pprint(lyr.connectionProperties)

# get list of items in a folder
OutputTest_Folder = r"C:\Users\jtouzel\AppData\Roaming\Esri\Desktop10.6\ArcMap\Coordinate Systems"
for i in os.listdir(OutputTest_Folder):
    print(i)

# Get list of fields
descFC = arcpy.Describe(UTM_List[0])
fieldList = [f.name for f in arcpy.ListFields(ParcelGridFeatureLayer)]

for f in fieldList:
    print(f)
# delete a field
arcpy.DeleteField_management(newFC,fieldList[2])

for fields in arcpy.ListFields(newFC):

    if fields.name not in keep_fields:
        arcpy.DeleteField_management(newFC, fields.name)

# make a copy of a feature class
newFC = os.path.join(database, "RogersCountyParcel_Copy")
arcpy.CopyFeatures_management(UTM_List[0], newFC)

# delete a feature class
arcpy.Delete_management(newFC)

# list feature classes
arcpy.ListFeatureClasses()

# Fix symbology for LSS rankings
project = arcpy.mp.ArcGISProject("CURRENT")
map_1 = project.listMaps("Map")[0]
lyr = map_1.listLayers()
for f in range(1,5):
    lyr_symbology = lyr[f].symbology
    lyr_symbology.updateRenderer('UniqueValueRenderer')
    lyr_symbology.renderer.fields = ['Priority_streams']
    lyr[f].symbology = lyr_symbology
    lyr_symbology = lyr[f].symbology

# reproject a feature class
import arcpy
import os

arcpy.env.workspace = r"C:\Users\jtouzel\Desktop\TEMP\PRO_DEFAULT_GDB\Pro_Default.gdb"
arcpy.env.overwriteOutput = True

FC_List = arcpy.ListFeatureClasses()

inputFC = FC_List[2]
outputFC = 'WilliamsonCounty_Proj'
outputProjFolder = r'C:\Users\jtouzel\AppData\Roaming\Esri\Desktop10.6\ArcMap\Coordinate Systems'
ProjList = []
for i in os.listdir(outputProjFolder):
    ProjList.append(i)
outputProj = os.path.join(outputProjFolder, ProjList[6])

FC_Description = arcpy.Describe(inputFC)
FC_Description.spatialReference.name

arcpy.Project_management(inputFC, outputFC, outputProj)

# get the last part of a file path
os.path.basename(os.path.normpath(outputProjFolder))

# return a string with double quotes
teststring = 'butts'
print('"{}"'.format(teststring))

# Calc Null Values
def calculateNull(field):
    if field is None:
        return 0
    else:
        return field

#use a dictionary to get the abbreviation and full name of a state
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
StateName = "vermont"
if len(StateName) == 2: # Get a lower case list of the state name and abbreviation depending on what the input is
    StateNameList = [name.lower() for abbr, name in StateListDictionary.items() if abbr.lower() == StateName.lower()]
    StateNameList.append(StateName.lower())
else:
    StateNameList = [abbr.lower() for abbr, name in StateListDictionary.items() if name.lower() == StateName.lower()]
    StateNameList.append(StateName.lower())

# Remove fields from an FC that don't exist in a list
OriginalFieldObjects = arcpy.ListFields(FeatureClass)
OriginalFieldList = []
for field in OriginalFieldObjects:
    if not field.required: # don't list the required fields
        OriginalFieldList.append(field.name)
NewFieldsList = [LandAgent,DateContacted,LandStatus,DealType,LegalStatus,SiteProtection,Notes,Attachments,Survey123,
                 StateField,CountyField,JobCode,ParcelID,ParcelOwner,ParcelAddress,ParcelAcreage,TotalCost,CostPerAcre,OwnerType,
                 OwnerOnOffSite,Grid2,HUC8,DeliveryFactorTN,DeliveryFactorTP,DeliveryFactorTSS,StreamLinearFeet,
                 StreamOrder,StreamSlope,BufferAcreage,LULCParcel,LULCRiparianBuffer,CanopyCoverParcel,CanopyCoverRB,
                 NWIAcres,NWIPercent,Soils,FEMAFZ,CriticalHabitat,ConservationEase,PriorityStreams,PriorityWetlands,
                 PriorityNutrientBank,PrioritySpecies,CreditYieldES,CreditYieldEW,CreditYieldENB,PropertySubcode,
                 ConfidenceIndicator]
RemoveTheseFields = []
for x in OriginalFieldList: # find all the fields form the original FC that we can remove
    if x.lower() not in [b.lower() for b in NewFieldsList]: # don't delete any of the new fields we just added
        RemoveTheseFields.append(x)
arcpy.AddMessage("Deleting all the incoming parcel fields we don't need anymore")
arcpy.DeleteField_management(FCWithFieldsToDelete,RemoveTheseFields)

# string to float
aNumber = "4"
aFloat = float(aNumber)

#update the Potential attribute with the updated Priority Streams data
##we need to maintain the current Potential data if there's a value there
##no value then we'll update it with the a yes if there's a value in the Priority Streams

def updatePotential(potential,priority):
    if potential:
        return potential
    else:
        if priority:
            return "Yes"
        else:
            return None

updatePotential(!Potential!,!Priority_streams!)


def typefun(rankfield):
    if rankfield == "high":
        return "Class 1"
    elif rankfield == "mod":
        return "Class 2"
    else:
        return "Class 3"

def calcsqft1(rankfield):
    c1 = 4
    c2 = 3
    c3 = 2
    if rankfield == "Class 1":
        return 20 * c1
    if rankfield == "Class 2":
        return 20 * c2
    if rankfield == "Class 3":
        return 20 * c3

def calcsqft2(rankfield):
    c1 = 600
    c2 = 400
    c3 = 200
    if rankfield == "Class 1":
        return 20 * c1 * 2
    if rankfield == "Class 2":
        return 20 * c2 * 2
    if rankfield == "Class 3":
        return 20 * c3 * 2

def calcsqft3(rankfield):
    c1 = 600
    c2 = 400
    c3 = 200
    presBuffer = 100
    if rankfield == "Class 1":
        return (20 * c1 * 2) + (c1 * 2 * presBuffer * 2)
    if rankfield == "Class 2":
        return (20 * c2 * 2) + (c2 * 2 * presBuffer * 2)
    if rankfield == "Class 3":
        return (20 * c3 * 2) + (c3 * 2 * presBuffer * 2)

# make sure outgoing file names for feature classes have an acceptable file name - remove all unacceptable characters
import arcpy
tablename = "123abcdokj-two...*ham!@#123"
tablename = arcpy.ValidateTableName(tablename)

# make sure input is a number
user_input = input ("Enter your Age")
try:
   val = int(user_input)
   print("Input is an integer number. Number = ", val)
except ValueError:
  try:
    val = float(user_input)
    print("Input is a float  number. Number = ", val)
  except ValueError:
      print("No.. input is not a number. It's a string")

# test values
inputnum = "3"
if type(inputnum) == str:
    print("Yes")

#Remove all non numeric values from a string
rawdata = ['1234frt', 'hoiun1234']
rawdata2 = filter(lambda x: x in '.0123456789', rawdata)
