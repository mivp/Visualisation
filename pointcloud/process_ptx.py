#!/usr/bin/env python
import numpy as np
import sys
import os
import ptxreader

"""
Load a list of ptx files
Expects at least 7 fields, x,y,z,I,R,G,B
 - Filter null points
 - Apply provided transformation matrix to all points
 - Write output to CSV or LAS file
"""

if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] + " outformat(csv/las) input_files")
    exit(1)

outext = sys.argv[1].lower()
if outext != 'las' and outext != 'csv':
    print(outext)
    print("Outformat must be 'las' or 'csv'")
    exit(1)

def writeLAS(fn, verts, irgb):
    print("Writing " + fn)
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

def writeCSV(fn, verts, rgb):
    print("Writing " + fn)
    import csv
    with open(fn, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
        for i in range(len(verts)):
            #writer.writerow(verts[i].tolist() + [int(e) for e in rgb[i]])
            row = verts[i].tolist()
            row.append(int(rgb[i][0]))
            row.append(int(rgb[i][1]))
            row.append(int(rgb[i][2]))
            writer.writerow(row)

for fn in sys.argv[2:]:
    count = 0
    print(fn)

    #Iterate the scans
    for scan in ptxreader.load(fn):
        print("Scan",count)
        outfile = os.path.splitext(os.path.basename(fn))[0] + '.' + str(count).zfill(3) + '.' + outext
        if os.path.exists(outfile):
            #Skip if output file exists
            print('Skipping existing file, ' + outfile) 
            continue

        #Write LAS/CSV file
        if outext == 'las':
            writeLAS(outfile, scan[0], scan[1]) 
        elif outext == 'csv':
           writeCSV(outfile, scan[0], scan[1][:,1:]) 

        count += 1

