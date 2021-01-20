import sys
import os
import argparse
import gzip

# Demultiplexes the output from HTStream hts_Primers based on probes detected in Read 1

# Inputs = tab-delimited output from hts_Primers (either PE or SE) and fasta file with probe names
# Can take a tab-delimited infile as stdin when piped from hts_Primers
# Looks for probe names in the annotation column for read 1 (does not look for probe names for read 2)
# Outputs = demultiplexed PE or SE fastq.gz files, named by probe name
# Optional input = path to the output directory

# Usage: htstream_demultiplex_R1probes.py -i infile -P probefile [-o path]

parser = argparse.ArgumentParser(description = "DemultiplexByProbes")
parser.add_argument('-i', '--infile', default=sys.stdin, type = argparse.FileType('r'))
parser.add_argument('-P', '--probes', required=True, type = argparse.FileType('r'))
parser.add_argument('-o', '--outdir')
args = parser.parse_args()

os.makedirs('%s' %args.outdir, exist_ok=True)

tablists = [(line.strip()).split('\t') for line in args.infile]
d=[]
for line in args.probes:
    if ">" in line:
        line=line[1:]
        d.append(line.strip())
            
if len(tablists[0]) == 8:
    for i in range(0,len(tablists)):
        tablists[i][0] = '@' + tablists[i][0]
        tablists[i][3] = '@' + tablists[i][3]
        tablists[i].insert(2,'+')
        tablists[i].insert(6,'+')  
    for probe in d:
        tabreads=[]
        for i in range(0,len(tablists)):
            if probe in tablists[i][8]:
                tabreads.append(tablists[i])
        fwd=[]
        for j in range(0,len(tabreads)):
            fwd.append('\n'.join(tabreads[j][0:4]))
        rev=[]
        for k in range(0,len(tabreads)):
            rev.append('\n'.join(tabreads[k][4:8]))
        fwd_out = os.path.join(args.outdir, '%s_R1.fastq.gz' % (probe))
        with gzip.open(fwd_out, 'wt') as probeout:
            for read in fwd:
                probeout.write('%s\n' % read)
        rev_out = os.path.join(args.outdir, '%s_R2.fastq.gz' % (probe))
        with gzip.open(rev_out, 'wt') as probeout:
            for read in rev:
                probeout.write('%s\n' % read)

elif len(tablists[0]) == 4:
    for i in range(0,len(tablists)):
        tablists[i][0] = '@' + tablists[i][0]
        tablists[i].insert(2,'+') 
    for probe in d:
        tabreads=[]
        for i in range(0,len(tablists)):
            if 'P5:Z:%s' %probe in tablists[i][4]:
                tabreads.append('\n'.join(tablists[i]))
        fwd_out_single = os.path.join(args.outdir, '%s_R1.fastq.gz' % (probe))
        with gzip.open(fwd_out_single, 'wt') as probeout:
                for read in tabreads:
                    probeout.write('%s\n' % (read))