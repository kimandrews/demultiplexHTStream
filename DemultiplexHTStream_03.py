import sys
import os
import argparse
import gzip

# Takes HTStream output (a tab6-formatted file for PE or SE reads) as input, 
# and looks for probe names in the read ID of the forward read 
# (does not look for probe names in reverse read ID).
# Outputs fastq.gz files, with a separate output file containing reads for each probe.
# Can also take a tab6-formatted infile as stdin (when piped from HTStream).
# Probe names must be provided in a fasta file.
# The path to an output directory can be provided.

# Usage: scriptname.py infile probes [-outpath]

parser = argparse.ArgumentParser(description = "DemultiplexByProbes")
parser.add_argument('infile', default=sys.stdin)
parser.add_argument('probes')
parser.add_argument('-outpath')
args = parser.parse_args()

os.makedirs('%s' %args.outpath, exist_ok=True)

tabfile = open(args.infile, 'r')
tablists = [(line.strip()).split('\t') for line in tabfile]
probenames = open(args.probes, 'r')
d=[]
for line in probenames:
    if ">" in line:
        line=line[1:]
        d.append(line.strip())
            
if len(tablists[0]) == 6:
    for i in range(0,len(tablists)):
        tablists[i].insert(2,'+')
        tablists[i].insert(6,'+')  
    for probe in d:
        tabreads=[]
        for i in range(0,len(tablists)):
            if probe in tablists[i][0]:
                tabreads.append(tablists[i])
        fwd=[]
        for j in range(0,len(tabreads)):
            fwd.append('\n'.join(tabreads[j][0:4]))
        rev=[]
        for k in range(0,len(tabreads)):
            rev.append('\n'.join(tabreads[k][4:8]))
        fwd_out = os.path.join(args.outpath, '%s_R1.fastq.gz' % (probe))
        with gzip.open(fwd_out, 'wt') as probeout:
            for read in fwd:
                probeout.write('%s\n' % read)
        rev_out = os.path.join(args.outpath, '%s_R2.fastq.gz' % (probe))
        with gzip.open(rev_out, 'wt') as probeout:
            for read in rev:
                probeout.write('%s\n' % read)

elif len(tablists[0]) == 3:
    for i in range(0,len(tablists)):
        tablists[i].insert(2,'+') 
    for probe in d:
        tabreads=[]
        for i in range(0,len(tablists)):
            if probe in tablists[i][0]:
                tabreads.append('\n'.join(tablists[i]))
        fwd_out_single = os.path.join(args.outpath, '%s_R1.fastq.gz' % (probe))
        with gzip.open(fwd_out_single, 'wt') as probeout:
                for read in tabreads:
                    probeout.write('%s\n' % (read))