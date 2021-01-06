#!/usr/bin/evn python3

'''
This tool look for input in the form of a file name, if it doesn't get that, it look for intput from stdin.
The input should be in tab6 format.

'''

import sys
import os
import gzip
from optparse import OptionParser

# Set up option parsing:
usage = "usage: %prog [options] -o sample_name inputfile.tab6"
usage += "\nor\nhts_Application | %prog [options] -o sample_name"
parser = OptionParser(usage=usage)

parser.add_option('-u', '--uncompressed', help="leave output files uncompressed",
                  action="store_true", dest="uncompressed")
parser.add_option('-o', '--sample_name', help="sample_name prefix for output files",
                  action="store", type="str", dest="output_base",default="sample1")


(options, args) = parser.parse_args()

## Check for command line argument (file) or use sys.stdin if it wasn't provided.
# Open stdin / file / gzipped file depending on what was provided.
if len(sys.argv) == 1:
    intab6 = sys.stdin
elif len(sys.argv) == 2:
    infile = sys.argv[1]
    if infile.split('.')[-1] == 'gz':
        intab6 = gzip.open(infile, 'rb')
    else:
        intab6 = open(infile, 'r')
else:
    print(f"Error, {len(sys.arg) -1} options detected, expected 0 or 1.")
    sys.exit()


## Outputs will contain a set of keys indicating which 
outputs = {}


## Now parse each line of input, figure out which primer (or locus?) it came from

for line in intab6:
    line2 = line.strip().split()  # strip line return and split on delimiters
    read1ID = read1 = read1q = read2ID = read2 = read2q = None
    if len(line2) >= 3:  # this should grab data for SE and skip blank lines
        read1ID = line2[0]
        read1 = line2[1]
        read1q = line2[2]
    if len(line2) == 6:  # this should grab data for PE if it is available
        read2ID = line2[3]
        read2 = line2[4]
        read2q = line2[5]
    
    # Parse read1ID, figure out which primer/locus it came from.

    # Check if an output file alread exists for the primer/locus of interest.

    # 


# Close all file handles in outputs{}
