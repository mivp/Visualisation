#!/usr/bin/env python
import numpy as np
from itertools import islice
import math
import sys
import os

"""
Split ptx file into separate files per scan
"""

if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " filepath"
    exit(1)
fn = sys.argv[1]
print(fn)

headerlen = 10
with open(fn, 'r') as infile:
    #PTX contains multiple scans, prefixed by a 10 row header
    count = 0
    while True:
        header_gen = islice(infile, 10)
        header = list(header_gen)
        if len(header) != 10:
            #Done
            break
        cols = int(header[0])
        rows = int(header[1])
        pos = [float(e) for e in header[2].split()]
        XYZ = [[float(e) for e in row.split()] for row in header[3:6]]
        transform = [[float(e) for e in row.split()] for row in header[6:10]]
        print(rows,cols)
        print(pos)
        print(XYZ)
        print(transform)

        lines_gen = islice(infile, rows*cols)

        #Write to another file
        outfn = os.path.splitext(fn)[0] + "_split_" + str(count) + ".ptx"
        print("Writing " + outfn)
        with open(outfn, 'w') as outfile:
            for line in header:
                outfile.write(line)
            for line in lines_gen:
                outfile.write(line)
        count += 1

