import sys
import os
import argparse
import gzip

### Demultiplexes the output from HTStream hts_Primers based on probes detected at the beginning of Read 1, and subsamples to a maximum of 600 reads per sample ###

#Inputs = tab-delimited output from hts_Primers (either PE or SE) and fasta file with probe names 
#Optional input = path to the output directory
#Output = PE or SE fastq.gz files demultiplexed by Read1 probe. Output files are named by probe name. This script does not look for probes in Read 2.
#Input can be piped directly from hts_Primers (i.e., this script can take a tab-delimited infile as stdin)

#Usage:
#htstream_demultiplex_R1probes.py -i infile -P probefile [-o path]

parser = argparse.ArgumentParser(description = "DemultiplexByProbes")
parser.add_argument('-i', '--infile', default=sys.stdin, type = argparse.FileType('r'))
parser.add_argument('-P', '--probes', required=True, type = argparse.FileType('r'))
parser.add_argument('-o', '--outdir')
args = parser.parse_args()

os.makedirs('%s' %args.outdir, exist_ok=True)

tablists = [(line.strip()).split('\t') for line in args.infile]
probenames=[]
for line in args.probes:
    if ">" in line:
        line=line[1:]
        probenames.append(line.strip())
probe_reads = {key:[] for key in probenames}

if len(tablists[0]) == 8:
    for read in tablists:
        read[0] = '@' + read[0]
        read[3] = '@' + read[3]
        read.insert(2,'+')
        read.insert(6,'+') 
    j=1 
    for read in tablists:
        if j >600:
            break
        for key in probe_reads.keys():
            if key in read[8]:
                probe_reads[key].append(read)
                j+=1
    for key in probe_reads.keys():
        fwd=[]
        for i in range(0,len(probe_reads[key])):
            fwd.append('\n'.join(probe_reads[key][i][0:4]))
        rev=[]
        for i in range(0,len(probe_reads[key])):
            rev.append('\n'.join(probe_reads[key][i][4:8]))
        fwd_out = os.path.join(args.outdir, '%s_R1.fastq.gz' % (key))
        with gzip.open(fwd_out, 'wt') as probeout:
            for read in fwd:
                probeout.write('%s\n' % read)
        rev_out = os.path.join(args.outdir, '%s_R2.fastq.gz' % (key))
        with gzip.open(rev_out, 'wt') as probeout:
            for read in rev:
                probeout.write('%s\n' % read)

elif len(tablists[0]) == 4:
    for read in tablists:
        read[0] = '@' + read[0]
        read.insert(2,'+') 
    for read in tablists:
        for key in probe_reads.keys():
            if 'P5:Z:%s' %key in read[4]:
                probe_reads[key].append(read)
    for key in probe_reads.keys():
        fwd=[]
        for i in range(0,len(probe_reads[key])):
            fwd.append('\n'.join(probe_reads[key][i][0:4]))		
        fwd_out_single = os.path.join(args.outdir, '%s_R1.fastq.gz' % (key))
        with gzip.open(fwd_out_single, 'wt') as probeout:
            for read in fwd:
                probeout.write('%s\n' % (read))