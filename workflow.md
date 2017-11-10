# Workflow for the Dogon-languages project

## Normalization: Concept Mapping

1. prepare a file (tsv) with an ID as first column (numeric), and containing one column named ENGLISH (capitabl letters important)
2. run concepticon mapping code, and refine (if you don't want to link, emtpy both CONCEPTICON_ID, and CONCEPTICON_GLOSS, if you want a new concepticon concept, empty the ID field, and write !GLOSS (where GLOSS is your proposed gloss), don't leave any question-marks in the CONCEPTICON-columns, they should be all either mapped or empty
3. run script that checks the concept mapping

To run the concepticon-mapping, do the following:

```shell
$ concepticon map_concepts INFILE.tsv > OUTFILE.tsv
```
This will produce the output file.

To run the concepticon-check of a concept-list, [...] script needs to be added and info as well [...]

## Concepticon API from within Python

To use the concepticon API from within Python, do the following: 

```python
>>> from pyconcepticon.api import Concepticon
>>> con = Concepticon()
```

Concepticon concept sets are accessed by their ID, passed as a string:

```python
>>> con.conceptsets['1']
Conceptset(id='1', gloss='CONTEMPTIBLE', semanticfield='Emotions and values', definition='Deserving of contempt or scorn.', ontological_category='Property', replacement_id='', _api=<pyconcepticon.api.Concepticon object at 0x7f2eee28a128>)
>>> con.conceptsets['1'].gloss
'CONTEMPTIBLE'
```

To get conceptsets by their glosses, you can convert them to a dictionary:
```
>>> gloss2id = {c.gloss: c.id for c in con.conceptsets.values()}
```

In this way, one can easily check whether a proposed concept set has the right key in the dataset, etc.

## Orthography Profiles and Pre-processing

1. prepare a custom script that goes from the raw "VALUE" to a "FORM", similar to the one [I show here](https://github.com/LinguList/dogon-data/blob/master/jenaama/make-wordlist.py). 
2. when running this script as ```python make-wordlist.py``` it should create a file ```language-wordlist.tsv``` (where "language" is your language)
3. check the ```language-wordlist.tsv``` file manually for obvious errors and report them in issues, to refine them
4. create initial orthography profile
5. refine orthography-profile
6. check the orthography profile, whether it conforms to CLTS format (see [here](http://calc.digling.org/clts/), and the Python repository at https://github.com/lingpy/clts)
7. apply orthography profile

To create the initial profile, run:

```shell
$ lingpy profile -i language-wordlist.tsv -o language-profile.tsv --context --column=form
```

This will create a context-profile.

To check individual conversions inside Python, do the following ("profile.tsv" is here the path to your orthography profile):

```python
>>> from segments.tokenizer import Tokenizer
>>> tk = Tokenizer('profile.tsv')
>>> tk('ábá)
'á b á'
>>> tk('ábá', column="IPA")
'a ⁵ b a ⁵'
```



