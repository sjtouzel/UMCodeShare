# lets take some notes on map automation

# Cartographic Information Model - CIM

# MAPX, PAGX, LYRX - different property files for different parts of a pro doc
#   all in JSON format

# cim_obj = object.getdefinition(version) -- version is the ESRI version, i currently am on version 3 so i would use 'V3'
# object.setDefinition(cim_obj) -- this is how you push the changes to the object

####EXAMPLE
import arcpy.mp

p = arcpy.mp.ArcGISProject('current') # get the project
m = p.listMaps('GreatLakes')[0] # get the map
l = m.listLayers('GreatLakes')[0] # get the layer

l_cim = l.getDefinition('V3') # get the layer info (aka CIM)
for f in l_cim.featureTable.fieldDescriptions: # access the attribute data
    if f.fieldName == "OBJECTID" or f.fieldName == "Shape": # if the field name is one of these we'll make it invisible
        f.visible = False # set the visible option to False to turn it off


