# This script demultiplexes the output from HTStream hts_Primers based on probes detected in Read 1

* Inputs = tab-delimited output from hts_Primers (either PE or SE) and fasta file with probe names 
* Optional input = path to the output directory
* Output = PE or SE fastq.gz files demultiplexed by Read1 probe. Output files are named by probe name. This script does not look for probes in Read 2.
* Input can be piped directly from hts_Primers (i.e., this script can take a tab-delimited infile as stdin)

* Usage: 
```
htstream_demultiplex_R1probes.py -i infile -P probefile [-o path]
```