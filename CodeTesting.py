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

