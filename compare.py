from lingpy import *
from lingpy.evaluate.acd import bcubes, diff

from sys import argv

# change this to 0.45 for SCA and to about 0.55 for lexstat!!!
t = 0.55

lex = LexStat('dogon-bangime-corr.tsv')

if 'sca' in argv:
    lex.cluster(method='sca', threshold=t, ref='autocogid',
            restricted_chars='+_')
if 'lexstat' in argv:
    # complicated analysis
lex.get_scorer(runs=10000, restricted_chars='+_')
lex.cluster(method='lexstat', threshold=t, ref='autocogid',
        restricted_chars='+_')

if argv[1] in ['sca', 'lexstat']:
    p, r, f = bcubes(lex, 'cogid', 'autocogid', pprint=False)
    print('{0:.2f}  {1:.2f}  {2:.2f}'.format(p, r, f))

diff(lex, 'cogid', 'autocogid', filename='differences', pprint=False)
lex.output('tsv', filename='dogon-autor', ignore='all')
