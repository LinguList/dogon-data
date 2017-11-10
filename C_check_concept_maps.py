from lingpy import *
from sys import argv
from collections import defaultdict

csv = csv2list(argv[1], strip_lines=False)

header = csv[0]
reste = csv[1:]

# get concepticon indenx
cidx = header.index('CONCEPTICON_ID')
gidx = header.index('CONCEPTICON_GLOSS')
eidx = header.index("ENGLISH")

concepts = defaultdict(list)
for line in csv:
    concept = line[eidx]
    cid = line[cidx]
    gid = line[gidx]
    
    d
