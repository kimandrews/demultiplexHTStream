d=[]
with open("Probes_cox1_short.fasta") as probenames:
    for line in probenames:
        if ">" in line:
            line=line[1:]
            d.append(line.strip())
for probe in d:
    open('%s.fasta'%(probe), 'w').writelines(line for line in open('Test_tab6file.tsv') if probe in line)