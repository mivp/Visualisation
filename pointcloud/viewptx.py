#!/usr/bin/env python
import lavavu
import numpy as np
import sys
import ptxreader

"""
Load a ptx file and view aligned scans
Expects at least 7 fields, x,y,z,I,R,G,B
 - Extract all scans
 - Filter null points
 - Subsample
"""

if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " filepath subsample"
    exit(1)

fn = sys.argv[1]

ss = 0
if len(sys.argv) > 2:
    ss = int(sys.argv[2])

lv = lavavu.Viewer()

#Iterate the scans
for scan in ptxreader.load(fn, ss):
    #Load positions and RGB
    print("Creating vis object ")
    pts = lv.points()
    pts.vertices(scan[0])
    pts.rgb(scan[1][:,1:])

lv.interactive()
