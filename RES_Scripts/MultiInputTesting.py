import arcpy
import http.client



MultiInputs = arcpy.GetParameterAsText(0) # Get all the layers

MultiInputsList = MultiInputs.split(";")  # multi value input needs to be parsed
for i in MultiInputsList:
    arcpy.AddMessage(i)


httpConn = http.client.HTTPSConnection("https://gis.corp.res.us/server",6443)
httpConn.request("GET","/")



from arcgis.gis.server import Server
server_base_url = "https://gis.corp.res.us/server"
server = Server(url="{}:6443/arcgis/admin".format(server_base_url),
                tokenurl="{}:6443/arcgis/rest/generateToken".format(server_base_url),
                username="Jtouzel@RES",
                password="XSW@mko0")


