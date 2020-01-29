import arcpy, os

#this line is for using a script tool in arcmap
input_parameter = arcpy.GetParameterAsText(0)
input_parameter = r'C:\Users\jtouzel\Desktop\TEMP\ROCO_PARCEL.kmz'

direct = os.path.dirname(input_parameter)
arcpy.conversion.KMLToLayer(input_parameter, direct)
arcpy.env.overwriteOutput = True

database = input_parameter[:-3] + 'gdb'
dataset = database + '\Placemarks'

arcpy.env.workspace = dataset
GCS_List = arcpy.ListFeatureClasses()

coord_sys = arcpy.GetParameter(1)
coord_sys = r"C:\Users\jtouzel\AppData\Roaming\Esri\Desktop10.6\ArcMap\Coordinate Systems\NAD 1983 UTM Zone 15N.prj"

e_count = 0

for FC in GCS_List:

   arcpy.Project_management(FC, database + '\\' + FC + '_Proj', coord_sys)

arcpy.env.workspace = database
UTM_List = arcpy.ListFeatureClasses()

# mxd = arcpy.mapping.MapDocument('CURRENT')
# df = arcpy.mapping.ListDataFrames(mxd)[0]

#### Start the new FC here
arcpy.Delete_management(newFC)
keep_fields = ['OBJECTID', 'Shape', 'SHAPE', 'PopupInfo', 'Shape_Length', 'Shape_Area', 'SHAPE_Length', 'SHAPE_Area']

newFC = os.path.join(database, "RogersCountyParcel_Copy")
arcpy.CopyFeatures_management(UTM_List[0], newFC)

for fields in arcpy.ListFields(newFC):

    if fields.name not in keep_fields:
        arcpy.DeleteField_management(newFC, fields.name)

keep_fields = ['OID', 'Shape', 'SHAPE', 'PopupInfo', 'Shape_Length', 'Shape_Area', 'SHAPE_Length', 'SHAPE_Area']
fieldList = [f.name for f in arcpy.ListFields(newFC)]
fieldList.append('SHAPE_Area')

for FC in UTM_List:

##### first add the fields

    SC = arcpy.da.SearchCursor(FC, keep_fields)
    for row in SC:

      pop_string = row[3]
      pop_array = pop_string.split("<")
      n += 1
      fields_array = []
      names_array = []


      for tag in pop_array:
         if "td>" in tag and "/td>" not in tag:
            fields_array.append(tag)
      break

   # for fields in arcpy.ListFields(FC):
   #
   #    if fields.name not in keep_fields:
   #       arcpy.DeleteField_management(newFC,fields.name)

   #this will list the field names and field values
   #even indexes are field names (starts at 0)
   #and odd indexes are field values
   del fields_array[:2]

   for x in range(0,len(fields_array)):
      fields_array[x]=fields_array[x].replace("td>","")
      if x%2 == 0:
         if fields_array[x] not in fieldList:
            print(fields_array[x])
            names_array.append(fields_array[x])
            arcpy.AddField_management(newFC, fields_array[x], "TEXT")

   # default is all TEXT fields but I could change this later to reference the values
   #now we update the values
   names_array.append("PopupInfo")

   with arcpy.da.UpdateCursor(newFC,names_array) as UC:

      for row in UC:

         pop_string = row[-1]
         pop_array = pop_string.split("<")
         fields_array = []
         values_array = []

         for segment in pop_array:
            if "td>" in segment and "/td>" not in segment:
               fields_array.append(segment)

         del fields_array[:2]

         for x in range(0,len(fields_array)):
            if x % 2 != 0:
               if fields_array[x-1] not in keep_fields:
                  fields_array[x]=fields_array[x].replace("td>","")
                  values_array.append(fields_array[x])

         for y in range(0,len(values_array)):
            try:
               row[y] = values_array[y]
               UC.updateRow(row)
            except IndexError:
               e_count = e_count + 1

      



