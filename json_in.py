import hou
import json

with open('/Users/bowmant/code/gpx_to_json/sampleData/Turtles_.json', 'r') as json_file:
    data = json_file.read()
points = json.loads(data)

feetPerDegree = 364320

#hou.hipFile.clear()

print 'Get geo'
geo = obj.node('/obj/geo_for_points')
if not geo:
    geo = obj.createNode('geo', node_name='geo_for_points')

add = hou.node('/obj/geo_for_points/gps_points')
if add:
    print('Destroying /obj/geo_for_points/gps_points')
    add.destroy()
print('Creating /obj/geo_for_points/gps_points')
add = geo.createNode('add', node_name='gps_points')
print('Populating points')
add.parm('points').set(len(points))
for i, point in enumerate(points):
    base = 'pt' + str(i)
    add.parm(base + 'x').set(point['x'])
    add.parm(base + 'y').set(point['y'])
    add.parm(base + 'z').set(point['z'])
    add.parm('usept' + str(i)).set(True)
add.parm('switcher1').set(1) # Polygons by group

trans = hou.node('/obj/geo_for_points/scale_elevation')
if not trans:
    trans = geo.createNode('xform', node_name = 'scale_elevation')
trans.setFirstInput(add)
trans.parm('sz').set(1.0 / feetPerDegree * 10)

rot = hou.node('/obj/geo_for_points/point_elevation_up')
if not rot:
    rot = geo.createNode('xform', node_name = 'point_elevation_up')
rot.setFirstInput(trans)


rot.setDisplayFlag(True)
rot.setCurrent(True, clear_all_selected=True)

subd = hou.node('/obj/geo_for_points/subdivide')
if not subd:
    subd = geo.createNode('subdivide', node_name = 'subdivide')
subd.setFirstInput(rot)

endNode = subd
endNode.setDisplayFlag(True)
endNode.setCurrent(True, clear_all_selected=True)
