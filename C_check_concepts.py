import codecs
import logging
import os.path
import pickle
import zipfile
from itertools import zip_longest
from urllib import request

from lingpy.read.csv import csv2list
from pyconcepticon.api import Concepticon


class ConcepticonMapper:
    """
    Description.
    """

    @staticmethod
    def get_concepticon_api(refresh=False):
        if os.path.isfile('concepticon.api') and not refresh:
            logging.info('Using cached concepticon data.')
            return pickle.load(open('concepticon.api', 'rb'))
        else:
            logging.info('Fetching fresh concepticon data.')

            concepticon_master_data = request.urlopen(
                'https://github.com/clld/concepticon-data/archive/master.zip'
            )

            with open('master.zip', 'b+w') as f:
                f.write(concepticon_master_data.read())

            with zipfile.ZipFile('master.zip', 'r') as f:
                f.extractall('.')

            api = Concepticon('concepticon-data-master')
            pickle.dump(api, open('concepticon.api', 'wb'))

            return pickle.load(open('concepticon.api', 'rb'))

    def get_all_concepticon_glosses(self):
        concept_lists = [
            gloss for gloss in self.api.conceptsets.values()
        ]
        all_concepts = set()

        for gloss in concept_lists:
            all_concepts.add(gloss.gloss)

        return all_concepts

    def get_gloss_id_pairs(self):
        return {c.id: c.gloss for c in self.api.conceptsets.values()}

    def __init__(self):
        self.api = self.get_concepticon_api()


class ConceptRow:
    """
    Description.
    """

    def __init__(self, concept_line, concept_information, header_list):
        annotated_concept_information =\
            self.annotate_row_elements(concept_information, header_list)

        self.concept_dict = {
            concept_line: annotated_concept_information
        }

    @staticmethod
    def annotate_row_elements(concept_information, header_list):
        if len(concept_information) > len(header_list):
            return list(zip_longest(
                header_list, concept_information, fillvalue='MISSING_HEADER')
            )
        elif len(concept_information) < len(header_list):
            return list(zip_longest(
                header_list, concept_information, fillvalue='MISSING_VALUE')
            )
        else:
            return list(zip(header_list, concept_information))

    def check_if_gloss_is_in_concepticon(self, concepticon_concepts):
        for line, concept_information in self.concept_dict.items():
            gloss = [value for header, value
                     in concept_information
                     if header == 'CONCEPTICON_GLOSS'][0]

            return\
                (True, line, gloss)\
                if gloss in concepticon_concepts else\
                (False, line, gloss)

    def check_if_gloss_matches_id(self):
        # Check if gloss['id'] == gloss
        pass

    def check_if_proposed_gloss(self):
        for line, concept_information in self.concept_dict.items():
            gloss = [value for header, value
                     in concept_information
                     if header == 'CONCEPTICON_GLOSS'][0]

            return\
                (True, line, gloss)\
                if gloss.startswith('!') else\
                None

    def check_if_proposed_gloss_has_null_id(self):
        for line, concept_information in self.concept_dict.items():
            gloss = [value for header, value
                     in concept_information
                     if header == 'CONCEPTICON_GLOSS'][0]

            concepticon_id = [value for header, value
                              in concept_information
                              if header == 'CONCEPTICON_ID'][0]

            if gloss.startswith('!') and (int(concepticon_id or 0) == 0
                                          or concepticon_id == ''):
                return True, line, gloss
            elif gloss.startswith('!') and (int(concepticon_id or 0) > 0
                                           or concepticon_id):
                return False, line, gloss
            else:
                return None


class UniquenessError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def get_headers(concept_tsv_path):
    with codecs.open(concept_tsv_path, 'r', 'utf-8') as f:
        return f.readline().replace('\ufeff', '').rstrip('\r\n').split('\t')


def concept_to_concept_row(concept_tsv_path, headers):
    row_number = 1
    concepts = []

    def is_id(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    for row in csv2list(concept_tsv_path, comment=None):
        if is_id(row[0]):
            concepts.append(
                ConceptRow(row_number, row, headers)
            )

        row_number += 1

    return concepts


# def check_uniqueness(concept_list):
#     concept_ids = []
#
#     for concept in concept_list:
#         if concept.concept_id not in concept_ids:
#             concept_ids.append(concept.concept_id)
#         else:
#             print(
#                 f"Concept ID {concept.concept_id} doubled"
#                 f" at line {concept.line}."
#             )
#
#             # return concept_ids


# def check_id_for_uniqueness(list_of_ids: IDs):
#     gathered_ids = []
#
#     for concept_id in list_of_ids:
#         if concept_id not in gathered_ids:
#             gathered_ids.append(concept_id)
#         else:
#             raise UniquenessError(concept_id)  # We can fail better, later on.


def check_if_gloss_in_concepticon(gloss: str):
    # Check for gloss existence in concepticon API ...
    _ = gloss
    pass


# Find glosses with ! as proposed new glosses

# Check ID column for uniqueness
# Check concepticon API for proper gloss

# ------------------
# ID ENG
# 1
# 1
# ------------------

# print(my_concepts[0])

def get_concepts_not_in_concepticon(a):
    return [(x, y, z) for (x, y, z) in a if x is False]


headers_from_file = get_headers(
    'Bangime_mapped_updated.txt'
)
concepts_w = concept_to_concept_row(
    'Bangime_mapped_updated.txt', headers_from_file
)

con = ConcepticonMapper()

all_concepticon_concepts = con.get_all_concepticon_glosses()
sanity_check_concepts = []

for i in concepts_w:
    sanity_check_concepts.append(
        i.check_if_gloss_is_in_concepticon(all_concepticon_concepts)
    )

print(get_concepts_not_in_concepticon(sanity_check_concepts))

#for i in concepts_w:
#    print(i.check_if_proposed_gloss())

a = concepts_w[43]
""":type : ConceptRow"""

b = a.check_if_proposed_gloss_has_null_id()
print(b)