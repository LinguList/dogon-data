from lingpy import *
from lingpy.compare.partial import Partial
print("hello world")
wl = Wordlist('Final.tsv')
wl.output('tsv', filename='Final1', ignore='all')

for idx, tokens in wl.iter_rows('tokens'):
    try:
        classes = tokens2class(tokens, 'dolgo')
        
        new_tokens = []
        for t, c in zip(tokens, classes):
            if c == '0':
                pass
            else:
                new_tokens += [t]

        if new_tokens[-1] in ['+', '_']:
            new_tokens = new_tokens[:-1]
        if new_tokens[0] in ['+', '_']:
            new_tokens = new_tokens[1:]
        if '+ +' in ' '.join(new_tokens):
            new_tokens = ' '.join(new_tokens).replace('+ +', '+').split(' ')
        if not new_tokens:
            new_tokens = ['k', 'a', 'o' 's']
    except:
        new_tokens = ['k', 'a', 'o', 's']
    wl[idx, 'tokens'] = new_tokens

from lingpy.settings import rcParams
rcParams['tones'] = ''

lex = ('Final1.tsv', cldf=True, check=True)
lex.get_scorer(runs=10000, restricted_chars="_")
lex.output('tsv', filename='_dogon-bin')
lex.cluster(method='sca', ref='cogids',
        split_on_tones=False)
lex.output('tsv', filename='Final2', ignore='all')
lex=LexStat('Final2.tsv')
alm = Alignments(lex, ref='cogids', split_on_tones=False)
alm.align(restricted_chars='')
alm.output('tsv', filename='Final3', ignore='all')