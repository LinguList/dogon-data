from lingpy import *
from lingpy.compare.sanity import *
from tabulate import tabulate

lex = Wordlist('DataSet_ALL.tsv') #, url='dogon.sqlite3',

table = [['minimal coverage', 'taxa', 'concepts', 'varieties']]
for i in [300, 250, 200, 150, 100]:
    taxa, rest = mutual_coverage_subset(lex, i)
    concepts, rest_ = rest[0]
    table += [[i, taxa, concepts, ', '.join(rest_)]]

print(tabulate(table, tablefmt='pipe', headers='firstrow'))


#for i in range(lex.height, 1, -1):
#    if mutual_coverage_check(lex, i):
#        print('mutual coverage is {0}'.format(i))
#        break

def average_coverage(wordlist):
    mc = mutual_coverage(wordlist)
    score = []
    for v in mc.values():
        for key, val in v.items():
            score += [val]
    return sum(score) / len(score) / wordlist.height

def sublist(wordlist, concepts, languages):
    D = {0: wordlist.columns}
    for idx, concept, language in wordlist.iter_rows('concept', 'doculect'):
        if concept in concepts and language in languages:
            D[idx] = wordlist[idx]
    return Wordlist(D)

etd = lex.get_etymdict(ref='concept')
setd = sorted(etd, key=lambda x: len([y for y in etd[x] if y]), reverse=True)

cov = lex.coverage()
langs = sorted(cov, key=lambda x: cov[x], reverse=True)

print('Concepts | Languages | Average Coverage | Varieties')
print('--- | --- | --- ')
myf = open('subsets.tsv', 'w')
myf.write('concepts\tlanguages\taverage coverage\tvarieties\n')
# exclude some upper bounds
for i in [100, 125,  150, 175,  200, 225, 250, 275, 300]:
    for j in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
        languages = langs[:-j]
        concepts = setd[:i]
        cv = average_coverage(sublist(lex, concepts, languages))
        if cv >= 0.8:
            print(i, '|', len(languages), '| {0:.2f} | '.format(
                average_coverage(sublist(lex, concepts, languages))),
                ', '.join(languages))
            myf.write('\t'.join(
                    [str(len(concepts)), str(len(languages)),
                        '{0:.2f}'.format(cv), 
                        ','.join(['"{0}"'.format(l) for l in languages]),
                        ','.join(['"{0}"'.format(cc) for cc in
                            sorted(concepts)])])+'\n')
myf.close()