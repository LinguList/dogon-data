from clldutils.dsv import UnicodeDictReader
from clldutils.text import split_text_with_context, strip_brackets
from lingpy import *
from segments import Tokenizer
from collections import OrderedDict, defaultdict
from unicodedata import normalize

op = Tokenizer('D_profile.tsv')



languages = OrderedDict({
    "Toro Tegu (Toupere, JH)": "Toro_Tegu",
    "Ben Tey (Beni, JH)": "Ben_Tey",
    "Bankan-Tey (Walo, JH)": "Bankan_Tey",
    "Nanga (Anda, JH)": "Nanga",
    "Donno So": "Donno_So",
    "Jamsay (Douentza area, JH)": "Jamsay_Douentza_area)",
    "Perge Tegu (Pergué, JH)": "Perge_Tegu",
    "Gourou (Kiri, JH)": "Gourou",
    "Jamsay (Mondoro, JH)": "Jamsay_Mondoro",
    "Togo-Kan (Koporo-pen, JH with BT)": "Togo_Kan_Koporo_pen",
    "Yorno So (Yendouma, JH)": "Yorno_So",
    "Tomo Kan (Segue)": "Tomo Kan_Segue",
    "Tomo Kan (Diangassagou)": "Tomo_Kan_Diangassagou",
    "Tommo-So (JH)": "Tommo_So",
    "Tommo-So (Tongo Tongo, LM)": "Tommo_So_Tongo_Tongo",
    "Dogul Dom (Kundialang, JH)": "Dogul_Dom_Kundialang",
    "Dogul Dom (Bendiely & Kundialang, BC)": "Dogul_Dom_Bendiely_Kundialang",
    "Tebul Ure (JH)": "Tebul_Ure",
    "Yanda Dom (Yanda, JH)": "Yanda_Dom",
    "Najamba (Kubewel-Adia, JH)": "Najamba_Kubewel_Adia",
    "Tiranige (Boui, JH)": "Tiranige_Boui",
    "Mombo (Songho, KP)": "Mombo_Songho",
    "Ampari (Nando, KP)": "Ampari_Nando",
    "Bunoge (Boudou)": "Bunoge_Boudou",
    "Penange (Pinia)": "Penange_Pinia",
    })

# read file into lingpy wordlist
D = {}
idx = 1
concepts = defaultdict(int)
problems = 0
st = [('ADJ ', ''), ]
with UnicodeDictReader('D_dogon-wordlist.csv') as reader:
    for i, line in enumerate(reader):
        # get major aspects
        semfield = '{0}.{1}'.format(line['code (Eng)'], line['subcode (Eng)'])
        semfield_french = '{0}.{1}'.format(
                line['code (fr)'], line['sous-code (fr)'])
        concept = line['English']
        concept_french = line['français']
        short_concept = line['short']
        short_concept_french = line['court']
        ref = line['ref#']
        semfield_code = '{0}.{1}.{2}'.format(
                line['code #'],
                line['subcode #'],
                line['subsubcode #']
                )
        for language, doculect  in languages.items():
            entry = line[language].split(r'\\')[0].replace('\r', ' ').replace('\n', ' ')
            if entry.strip():
                try:
                    form = strip_brackets(
                            split_text_with_context(entry, separators=r',;/~\\')[0],
                            ).strip().replace(' ', '_').replace(',', '')
                    form = normalize('NFC', form)
                except IndexError:
                    form = False
                if form and form.strip():
                    segments = op('^'+form+'$', 'IPA')
                    if '�' in segments:
                        print(entry, ' ||| «'+form+'» ||| ', segments)
                        problems += 1
                    D[idx] = [concept, concept_french, doculect, language, entry, form, segments,
                        short_concept, short_concept_french, semfield, semfield_french,
                        ref, semfield_code]
                    idx += 1
                    concepts[concept, concept_french, short_concept, semfield_code, ref] += 1
D[0] = ['concept', 'concept_french', 'doculect', 'doculect_name_in_source', 'value', 'form', 'segments',
        'concept_abbreviated', 'concept_french_abbreviated', 'semantic_field',
        'semantic_field_french', 'semantic_reference', 'semantic_field_code']
print('Encountered {0} problems.'.format(problems))
with open('D_dogon-concepts.tsv', 'w') as f:
    f.write('ID\tNUMBER\tENGLISH\tFRENCH\tENGLISH_SHORT\tSEMFIELD_CODE\tREFERENCE\tOCCURRENCE\n')
    for i, (vals, occ) in enumerate(sorted(concepts.items(), key=lambda x:
        x[1], reverse=True)):
        if occ >= 17:
            f.write(str(i+1)+'\t'+str(i+1)+'\t'+'\t'.join(vals)+'\t'+str(occ)+'\n')
wl = Wordlist(D)
wl.output('tsv', filename='D_dogon-edictor', ignore='all', prettify=False)
