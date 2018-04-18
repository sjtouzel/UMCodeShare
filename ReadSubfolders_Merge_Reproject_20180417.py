## Iterate through a folder to find all the shapefiles in sub-folders, then create a list, then merge those shapes together
import os
from arcpy import env
import arcpy

path = r"C:/Users/z02sjt/Desktop/PythonWorkspace/By State Tiger Data UNSD"
env.workspace = path

'''
Use os.walk to isolate the different objects within the directory.
Append the root, or directory location for files/folders, to the folder list.
'''

folderlist = [] # Create empty list for all the folder names
for root, dirs, files in os.walk(): # Walk through the input path
    folderlist.append(root) # Append the directories to folderlist

'''
Iterate through the folderlist, calling os.listdir() on each folder to isolate
each file in the directory.  If that file has a '.shp' extension, append it
to the shapefiles list using os.path.join() to connect the file to its directory
'''

shapefiles = []
for folder in folderlist: # Loop through the folder list
    for i in os.listdir(folder): # Call listdir on the folder
        if i.endswith('.shp'): # Use a conditional statement to verify if the file has a '.shp' extension
            shapefiles.append(os.path.join(folder, i)) # Append the file to the shapefiles list using the join method

# Now lets try to do our merge
OutPath = r"C:/Users/z02sjt/Desktop/PythonWorkspace/ArcPyFun.gdb"
mergedSchoolDistricts = "C:/Users/z02sjt/Desktop/PythonWorkspace/ArcPyFun.gdb/All_SchoolDists"
arcpy.Merge_management(shapefiles, mergedSchoolDistricts, OutPath)  # It fuckin worked!

# Now lets re-project
env.workspace = OutPath
outCS = "C:/Users/z02sjt/AppData/Roaming/ESRI/Desktop10.5/ArcMap/Coordinate Systems/NAD83 Albers Equal Area, 48 States, Panhandle, US Foot.prj"
input_features = "C:/Users/z02sjt/Desktop/PythonWorkspace/ArcPyFun.gdb/All_SchoolDists"
output_features = os.path.join(OutPath, "All_SchoolDists_Proj")
arcpy.Project_management(input_features, output_features, outCS)
