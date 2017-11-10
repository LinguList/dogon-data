from lingpy import *
from clldutils.text import split_text_with_context, strip_brackets

# load data, I do it the lazy way, loading with lingpy's csv2list function, but
# ideally, use clldutils
data = csv2list('jenaama.tsv', strip_lines=False)

# make a dictionary in simple lingpy form, which can be imported into a
# wordlist, D[0] is the header, the rest is the ID in a wordlist, etc.
D = {0: ['doculect', 'id_in_source', 'concept', 'concept_french', 'value', 'form']}

idx = 1
for i, (line_id, value, english, french) in enumerate(data[1:]):
    # we use clldutils to check the usefulness of the form
    forms = split_text_with_context(strip_brackets(value), separators=",;/")
    for f in forms:
        if f.strip() not in ['', '?', '-']:
            # we need to replace whitespace by underscore
            D[idx] = ['Jenaama', line_id, english, french, value, f]
            idx += 1

# now it's simple
wl = Wordlist(D)
wl.output('tsv', filename='jenaama-wordlist', ignore='all', prettify=False)


