#!/usr/bin/env python
"""
Load point cloud from Wavefront OBJ with 6d vertices (x,y,z,r,g,b)
"""
import pywavefront
import numpy
import sys
import lavavu

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " filepath subsample")
    exit(1)

scene = pywavefront.Wavefront(sys.argv[1])

ss = 1
if len(sys.argv) > 2:
    ss = int(sys.argv[2])

V = numpy.array(scene.vertices)
print(V.shape)

#SubSample
if ss > 1:
    V = V[::ss]
print(V.shape)

verts = V[:,0:3]
colours = V[:,3:] * 255
print(verts.shape,colours.shape)

#Load positions and RGB
print("Creating visualisation ")
lv = lavavu.Viewer()
pts = lv.points()
pts.vertices(verts)
pts.rgb(colours)

lv.interactive()
