import arcpy

MultiInputs = arcpy.GetParameterAsText(0) # Get all the layers

arcpy.AddMessage(MultiInputs)