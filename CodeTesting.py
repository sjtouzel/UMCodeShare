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
fieldList = [f.name for f in arcpy.ListFields(newFC)]

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