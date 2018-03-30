from lingpy import *

concepts = [c[0] for c in csv2list('concepts.tsv')]
data = csv2list('Dogon-DataSet-Phylo.tsv', strip_lines=False)
header = data[0]
gidx = header.index('CONCEPT')
with open('Dogon-DataSet-Phylo.tsv', 'w') as f:
    f.write('\t'.join(header)+'\n')
    for line in data[1:]:
        if line[gidx] in concepts:
            f.write('\t'.join(line)+'\n')
