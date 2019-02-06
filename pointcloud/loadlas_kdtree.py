#!/usr/bin/env python
import laspy
import sys
import lavavu
import numpy as np

"""
Experiment with kdtree on a point cloud
"""

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " filepath")
    exit(1)

infile = laspy.file.File(sys.argv[1], mode="r")

print(infile)
print(infile.point_format)
for spec in infile.point_format:
   print(spec.name)
print(infile.header)
print(infile.header.dataformat_id)

print(infile.header.offset)
print(infile.header.scale)

# Grab all of the points from the file.
#point_records = infile.points
#print(point_records)
#print(point_records.shape)

verts3 = np.vstack((infile.x, infile.y, infile.z)).reshape([3, -1]).transpose()

xmin = np.min(infile.x)
ymin = np.min(infile.y)
zmin = np.min(infile.z)

xmax = np.max(infile.x)
ymax = np.max(infile.y)
zmax = np.max(infile.z)

minpt = [xmin,ymin,zmin]
maxpt = [xmax,ymax,zmax]
range = [xmax-xmin,ymax-ymin,zmax-zmin]
midpt = [xmin+0.5*range[0],ymin+0.5*range[1],zmax+0.5*range[2]]
print(minpt)

#KDtree for finding nearest neighbour points
from scipy import spatial
sys.setrecursionlimit(10000)
tree = spatial.cKDTree(verts3)
#tree = spatial.KDTree(verts3)

#Query camera position
print("Tree query")
q = tree.query(midpt, k=500000)
#Query result is tuple of two arrays, distances, indices

print("Result get ", q[0].shape, q[1].shape)
print(q[0][0:10], q[1][0:10], [tree.data[i] for i in q[1][0:10]])
verts = np.array([tree.data[i] for i in q[1]])
print(verts.shape)
#for r in range(len(q[0])):
#    print("result, distance, point")
#    print(r, q[0][r], tree.data[q[1][r]])
#    #Index of nearest grid point is in q[1][r]

print("Vis")
#Load positions and RGB
lv = lavavu.Viewer()
print("Creating vis object ")
pts = lv.points()
pts.vertices(verts)
#pts.vertices([infile.x, infile.y, infile.z])
#pts.rgb([infile.red, infile.green, infile.blue])

#origin = lv.points(vertices=[0,0,0], pointsize=10, colour="red")

lv.interactive()
