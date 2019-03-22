import os
import re
import sys

"""
Splits groups in a WaveFront OBJ file into separate files
"""

def writeOBJ(group, header, buf):
    print(group)
    g2 = re.sub(r"\s+", '_', group)
    ofn = g2 + '.obj'
    ctr = 0
    while os.path.exists(ofn):
        ctr += 1
        ofn = g2 + '_' + str(ctr) + '.obj'
    print(" - " + ofn)
    w = open(ofn, "w")
    #Write the current buffer
    w.write(header)
    w.write(buf)
    w.close()

def splitOBJ(fp):
    r = open(fp, "r")
    buf = ""
    header = ""
    group = None
    for line in r:
        if line[0:2] == 'g ':
            if group is not None:
                #Write a file for each group
                writeOBJ(group, header, buf)
                buf = ""

            #Get next group
            group = line[2:]

        elif group is None:
            #Append all initial lines to a header
            header += line
        else:
            buf += line

    if group is None:
        print("No groups found")
    else:
        #Write a file for each group
        writeOBJ(group, header, buf)

    r.close()


if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " filepath")
    exit(1)

splitOBJ(sys.argv[1])

