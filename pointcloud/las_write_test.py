#!/usr/bin/env python
import lavavu
import numpy as np
from itertools import islice
import math
import sys
import os
import re
import random

"""
Create some points and save as a LAS file
"""

lv = lavavu.Viewer()

sphere = lv.shapes(vertices=[0,1.5,0], colour="red", scaling=100)

#A bit of hackyness to extract the sphere vertices
lv.open()
lv.select(1)
lv.bake()
d = sphere.data()
spherev = d[0].get('vertices')
spherev = spherev.reshape((-1,3))
lv.clear()

sphere = lv.points(vertices=spherev, colour="red", pointsize=5)

groundv = lavavu.grid3d(corners=[[-10,0,-10], [10,0,-10], [10,0,10]], dims=(500,500))
groundv = groundv.reshape((-1,3))

for j in range(groundv.shape[0]):
    groundv[j][1] += random.uniform(0,0.25)

ground = lv.points(vertices=groundv, colour="beige", pointsize=5)
#sphere = lv.points(vertices=spherev, colour="red", pointsize=5)
lv.interactive()

def writeLAS(fn, verts, irgb):
    print("Writing " + fn)
    print(verts.shape, irgb.shape)
    import laspy
    hdr = laspy.header.Header(point_format=3)

    outfile = laspy.file.File(fn, mode="w", header=hdr)

    allx = verts[:,0]
    ally = verts[:,1]
    allz = verts[:,2]

    """
    #Offset necessary?
    xmin = np.floor(np.min(allx))
    ymin = np.floor(np.min(ally))
    zmin = np.floor(np.min(allz))

    outfile.header.offset = [xmin,ymin,zmin]
    """

    #outfile.header.scale = [0.001,0.001,0.001]
    outfile.header.scale = [1e-6,1e-6,1e-6]

    outfile.x = allx
    outfile.y = ally
    outfile.z = allz

    #print(dir(outfile))
    I = (irgb[:,0] * 65535).astype(np.uint16)
    R = irgb[:,1].astype(np.uint8)
    G = irgb[:,2].astype(np.uint8)
    B = irgb[:,3].astype(np.uint8)

    outfile.set_intensity(I)
    outfile.set_red(R)
    outfile.set_green(G)
    outfile.set_blue(B)

    print(outfile.point_format)
    for spec in outfile.point_format:
       print(spec.name,)

    outfile.close()

verts = []
irgb = []
for v in groundv:
    verts.append(v)
    irgb.append([1.0, 255,255,225])
for v in spherev:
    verts.append(v)
    irgb.append([1.0, 255,0,0])

#Write LAS file
writeLAS('test.las', np.array(verts), np.array(irgb))

