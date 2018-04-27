## Iterate through a folder to find all the shapefiles in sub-folders, then create a list, then merge those shapes together
import os
from arcpy import env
import arcpy

path = r"M:/COMPLIANCE/NPMS/EditCopy"
env.workspace = path

folderlist = [] # Create empty list for all the folder paths
folderNoPath = [] # Create empty list for all the folder names
for x in os.listdir(path):  # This will create path names for all the folders in the path folder
    folderlist.append(path + "/" + x)
    folderNoPath.append(x) # Store the folder name for later use in naming new feature classes

# Now lets build a list of all of the shapefiles from all of these subfolders
# Iterate through the folderlist, calling os.listdir() on each folder to isolate each file in the directory.
# If that file has a '.shp' extension, append it to the shapefiles list using os.path.join() to connect the
# file to its directory

arcpy.CreateFileGDB_management(path, "ArcPyFun.gdb")  # first create a geodatabase to store it cause a .shp won't work
outPath = os.path.join(path, "ArcPyFun.gdb")
defineCS = "C:/Users/z02sjt/AppData/Roaming/ESRI/Desktop10.5/ArcMap/Coordinate Systems/NAD 1983.prj"
outCS = "C:/Users/z02sjt/AppData/Roaming/ESRI/Desktop10.5/ArcMap/Coordinate Systems/Basic Albers NAD83.prj"
stateShp = "C:/Users/z02sjt/Desktop/PythonWorkspace/States.shp"

for folder in folderlist: # Loop through the folder list
    # Get the last 5 digits from the folder path and append it to the output merged shapefile name
    mergedOPIDShapes = os.path.join(outPath, "merged_" + folderNoPath[folderlist.index(folder)]) # Create a feature
                                                                                   # class path for the merged shapes
    fields = ["Mileage", "SHAPE@LENGTH"] # we'll use these fields when we calculate mileage later
    shapefile = []
    for i in os.listdir(folder): # Call listdir on the folder
        if i.endswith('.shp'): # Use a conditional statement to verify if the file has a '.shp' extension
            shapefile.append(os.path.join(folder, i)) # Append the file to the shapefiles list using the join method
    if len(shapefile) > 1: # merge and project
        print "Let's merge the layers in %s" %folder
        arcpy.Merge_management(shapefile, mergedOPIDShapes, outPath) # merge
        arcpy.DefineProjection_management(mergedOPIDShapes, defineCS) # define projection
        # Reproject to Basic Albers NAD83 projection, so we can calculate lengths
        shapeReproj = os.path.join(outPath , "reproj_" + folderNoPath[folderlist.index(folder)]) # Create a feature
                                                                                            # class path for the copy
        arcpy.Project_management(mergedOPIDShapes, shapeReproj, outCS)
        # Now we gotta do an intersect with a US states shapefile and then adjust fields
        stateIntersect = os.path.join(outPath, "stateIntersect_" + folderNoPath[folderlist.index(folder)])  # create a
                                                                        # feature class path for the intersect output
        arcpy.Intersect_analysis([shapeReproj, stateShp], stateIntersect, join_attributes="ALL", output_type="LINE")
                                                                                                    # Run the intersect
        # Add a mileage attribute and calculate mileage for each segment
        arcpy.AddField_management(stateIntersect, "Mileage", "DOUBLE", field_scale = 2) # Create the mileage field
        with arcpy.da.UpdateCursor(stateIntersect, fields) as cursor: # Calculate Mileage
            for row in cursor:
                row[0] = row[1] / 5280
                cursor.updateRow(row)
        del row, cursor
    elif 0 < len(shapefile) < 2: # just project if there's only one shp
        print "Let's project the layer in %s" % folder
        shapeProjected = os.path.join(outPath , "proj_" + folderNoPath[folderlist.index(folder)]) # Create a feature
                                                                                            # class path for the copy
        arcpy.CopyFeatures_management(shapefile[0], shapeProjected) # copy to the gdb
        arcpy.DefineProjection_management(shapeProjected, defineCS) # project
        # Reproject to Basic Albers NAD83 projection, so we can calculate lengths
        shapeReproj = os.path.join(outPath, "reproj_" + folderNoPath[folderlist.index(folder)]) # Create a feature class
                                                                                            # path for the reprojection
        arcpy.Project_management(shapeProjected, shapeReproj, outCS) # Reproject
        # Now we gotta do an intersect with a US states shapefile and then adjust fields
        stateIntersect = os.path.join(outPath, "stateIntersect_" + folderNoPath[folderlist.index(folder)]) # create a
                                                                        # feature class path for the intersect output
        arcpy.Intersect_analysis([shapeReproj,stateShp], stateIntersect,join_attributes="ALL",  output_type = "LINE")
                                                                                                    # Run the intersect
        # Add a mileage attribute and calculate mileage for each segment
        arcpy.AddField_management(stateIntersect, "Mileage", "DOUBLE", field_scale=2)  # Create the mileage field
        with arcpy.da.UpdateCursor(stateIntersect, fields) as cursor: # Calculate Mileage
            for row in cursor:
                row[0] = row[1] / 5280
                cursor.updateRow(row)
        del row, cursor
    else:
        print "No shapes here %s" %folder



