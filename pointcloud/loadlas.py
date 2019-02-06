#!/usr/bin/env python
import laspy
import sys
import lavavu
import numpy as np

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " filepath subsample")
    exit(1)

infile = laspy.file.File(sys.argv[1], mode="r")

ss = None
if len(sys.argv) > 2:
    ss = int(sys.argv[2])

print(infile)
print(infile.point_format)
for spec in infile.point_format:
   print(spec.name)
print(infile.header)
print(infile.header.dataformat_id)

print(infile.header.offset)
print(infile.header.scale)

#Grab all of the points from the file.
#point_records = infile.points
#print(point_records)
#print(point_records.shape)

#Load positions and RGB
lv = lavavu.Viewer()
print("Creating vis object ")
pts = lv.points()
ss = 1

#Convert colours from short to uchar
print(infile.red.dtype)
if infile.red.dtype == np.uint16:
    R = (infile.red / 255).astype(np.uint8)
    G = (infile.green / 255).astype(np.uint8)
    B = (infile.blue / 255).astype(np.uint8)
else:
    R = infile.red
    G = infile.green
    B = infile.blue

if ss > 1:
    pts.vertices([infile.x[::ss], infile.y[::ss], infile.z[::ss]])
    pts.rgb([R[::ss],G[::ss],B[::ss]])
else:
    pts.vertices([infile.x, infile.y, infile.z])
    pts.rgb([R,G,B])

lv.interactive()
