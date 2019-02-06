#!/usr/bin/env python
import numpy as np
from itertools import islice
import math
import sys
import os
import re

"""
Iterate scans in a ptx file with a generator
 - Extract all scans
 - Filter null points
 - Subsample
 - Apply transform matrix
 - Yields: tuple (vertices(x,y,z), Irgb(I,r,g,b))
"""

def load(fn, ss=0, limit=0):
    with open(fn, 'r') as infile:
        #PTX contains multiple scans, prefixed by a 10 row header
        while True:
            #If any errors occur in the header, assume load done
            try:
                header_gen = islice(infile, 10)
                header = list(header_gen)
                cols = int(header[0])
                rows = int(header[1])
                pos = [float(e) for e in header[2].split()]
                XYZ = [[float(e) for e in row.split()] for row in header[3:6]]
                transform = [[float(e) for e in row.split()] for row in header[6:10]]
                print("Rows,Cols",rows,cols)
                print("Position",pos)
                print("Axes X,Y,Z",XYZ)
                print("Transform Matrix",transform)
            except:
                return

            #Generator object so we can process without loading into ram
            ssize = rows*cols
            print("Loading " + str(ssize) + " points")
            lines_gen = islice(infile, ssize)

            #data = np.loadtxt(lines_gen, dtype=np.float32, delimiter=' ')
            #Because numpy.loadtxt is really damn slow, writing a reader ourselves is faster...
            data = None
            #Generator to split the lines
            splitter = re.compile(' ')
            def items(infile):
                for line in infile:
                    for item in splitter.split(line):
                        yield item

            #Use double precision for transformation precision
            data = np.fromiter(items(lines_gen), np.float64, -1)
            #data = np.fromiter(items(lines_gen), np.float32, -1)

            #Format: X,Y,Z,scalar,R,G,B,?,?,?
            elements = len(data)/ssize
            print("Data: ",len(data),"Size: ",ssize,"Elements: ",elements)
            data = data.reshape((-1, elements))
            print(data.shape)

            #Filter zeros
            print("Filtering")
            data = data[((data[:,0] != 0.0) | (data[:,1] != 0.0) | (data[:,2] != 0.0))]
            print("Filtered size: " + str(data.shape))

            #Subsample based on limit reduce to < limit per scan
            if limit > 0:
                ss = int(math.floor(scan[0].shape[0] / limit))
            if ss > 0:
                print("Subsampling " + str(data.shape[0]) + " to " + str(ss))
                data = data[::ss,:]

            #Apply the transform
            print("Transforming")
            #transform_matrix = np.matrix(transform)
            transform_matrix = np.matrix(transform).transpose()
            #Convert to 4d verts
            verts = np.zeros((data.shape[0], 4))
            verts += [0.0, 0.0, 0.0, 1.0]
            verts[:,:-1] = data[:,:3]
            #Transform
            verts = verts.dot(transform_matrix.T)
            #Convert back to array (from matrix, which is always 2d)
            verts = np.asarray(verts)

            #Yield the data for the next scan
            yield (verts[:,:3], data[:,3:7]) 


