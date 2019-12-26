import arcpy

featureClass = ['in', 'out', 'up', 'down']
print(", ".join(featureClass))
print("Field Names: {}".format(", ".join(featureClass)))

item1 = 'red'
item2 = 'blue'
item3 = ''

newlist = [item1, item2, item3]
newlist2 = [i for i in newlist if i]
if item2:
    print(True)