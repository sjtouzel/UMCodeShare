## Iterate through a folder to find all the shapefiles in sub-folders, then create a list, then merge those shapes together
import os
from arcpy import env
import arcpy

path = r"C:/Users/z02sjt/Desktop/PythonWorkspace/By State Tiger Data UNSD"
env.workspace = path

folderlist = [] # Create empty list for all the folder names
for x in os.listdir(path):  # This will create path names for all the folders in the path folder
    folderlist.append(path + "/" + x)

# Now lets build a list of all of the shapefiles from all of these subfolders
fcList = [] # Create empty list for all the shapefiles
for x in range(0,len(folderlist)):  # Run through each folder
    env.workspace = folderlist[x]  # Set the folder as the workspace so our ListFeatureClasses function will look there
    shapeTemp = arcpy.ListFeatureClasses()  # find the shapefile info in each folder
    fcList.append(folderlist[x] + "/" + shapeTemp[0])  # Create a file path for each shapefile

# Now lets try to do our merge
OutPath = r"C:/Users/z02sjt/Desktop/PythonWorkspace/ArcPyFun.gdb"
mergedSchoolDistricts = "C:/Users/z02sjt/Desktop/PythonWorkspace/ArcPyFun.gdb/All_SchoolDists"
arcpy.Merge_management(fcList, mergedSchoolDistricts, OutPath)  # It fuckin worked!

# Now lets re-project
env.workspace = OutPath
outCS = "C:/Users/z02sjt/AppData/Roaming/ESRI/Desktop10.5/ArcMap/Coordinate Systems/NAD83 Albers Equal Area, 48 States, Panhandle, US Foot.prj"
input_features = "C:/Users/z02sjt/Desktop/PythonWorkspace/ArcPyFun.gdb/All_SchoolDists"
output_features = os.path.join(OutPath, "All_SchoolDists_Proj")
arcpy.Project_management(input_features, output_features, outCS)