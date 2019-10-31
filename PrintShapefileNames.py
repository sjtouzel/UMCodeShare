import os
from arcpy import env
import arcpy
import datetime

# set workspace to the gdb you're looking for
path = r"E:/Dropbox (RES)/@RES GIS/projects/CA/Klamath/DataReceived/AECOM/UpdatedContours/UpdatedContours.gdb"
env.workspace = path

# print out all the feature classes in each feature dataset. if the layers aren't in a feature dataset you can
# just use the second version below
fdss = arcpy.ListDatasets()
fdss.append('')
listOfFCs = [] #make an empty list
for fds in fdss:
    fc_names = arcpy.ListFeatureClasses(feature_dataset=fds)
    for fc_name in fc_names:
        listOfFCs.append(fc_name)  # build the list here
        print(fc_name)

# for i in arcpy.ListFeatureClasses():
#     listofFCs.append(i)

listOfFCs # does this biz look ok

# Write the list to a text file -- this will output a text file that acts like a csv
tableOutPath = r"C:/Users/jtouzel/Desktop/PythonTempOutput/"
dateTag = datetime.datetime.today().strftime('%Y%m%d') #we'll tag our output with this. looks somethin like this 20181213
outTextPath = os.path.join(tableOutPath, fdss[0] + "_" + dateTag + ".txt")
with open(outTextPath,'w') as f:
    for item in listOfFCs:
        f.write("'%s'," % item)


