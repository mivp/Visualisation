#!/usr/bin/env python
"""
Load point cloud from PLY with plyfile
"""
from plyfile import PlyData, PlyElement
import numpy
import sys
import lavavu

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " filepath subsample")
    exit(1)

plydata = PlyData.read(sys.argv[1])

ss = None
if len(sys.argv) > 2:
    ss = int(sys.argv[2])

#SubSample
#if ss > 1:
#    V = V[::ss]
#print(V.shape)

if plydata:
    print(plydata.elements[0].name)
    print(plydata.elements[0].properties)
    print(plydata.elements[0].data[0])
    #print(plydata.elements[0].data['x'])
    #print(plydata['face'].data['vertex_indices'][0])
    #print(plydata['vertex']['x'])
    #print(plydata['vertex'][0])
    #print(plydata.elements[0].ply_property('x'))


    x = plydata['vertex']['x']
    y = plydata['vertex']['y']
    z = plydata['vertex']['z']

    r = plydata['vertex']['red']
    g = plydata['vertex']['green']
    b = plydata['vertex']['blue']
    a = plydata['vertex']['alpha']
    #r = plydata['vertex']['diffuse_red']
    #g = plydata['vertex']['diffuse_green']
    #b = plydata['vertex']['diffuse_blue']

    print("Creating visualisation ")
    lv = lavavu.Viewer()
    pts = lv.points()

    pts.vertices([x, y, z])
    #pts.rgb([r, g, b])
    pts.rgba([r, g, b, a])

    lv.interactive()

