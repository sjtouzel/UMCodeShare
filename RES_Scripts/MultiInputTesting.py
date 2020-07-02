import arcpy

MultiInputs = arcpy.GetParameterAsText(0) # Get all the layers

MultiInputsList = MultiInputs.split(";")  # multi value input needs to be parsed
for i in MultiInputsList:
    arcpy.AddMessage(i)