import codecs
import os.path
import pickle
import zipfile
from itertools import zip_longest
from typing import List
from urllib import request

from lingpy.read.csv import csv2list
from pyconcepticon.api import Concepticon

Glosses = List[str]
IDs = List[int]


def get_current_concepticon_data():
    # Just a temporary function for testing purposes.

    if os.path.isfile('concepticon.api'):
        return pickle.load(open('concepticon.api', 'rb'))
    else:
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


class UniquenessError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def get_headers(concept_tsv_path):
    with codecs.open(concept_tsv_path, 'r', 'utf-8') as f:
        return f.readline().rstrip('\r\n').split('\t')


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


def check_uniqueness(concept_list):
    concept_ids = []

    for concept in concept_list:
        if concept.concept_id not in concept_ids:
            concept_ids.append(concept.concept_id)
        else:
            print(
                f"Concept ID {concept.concept_id} doubled"
                f" at line {concept.line}."
            )

            # return concept_ids


def is_temporary_concept(concept_gloss: str):
    if concept_gloss.startswith('!'):
        return True
    else:
        return False


def find_temporary_concept(concept_dict):
    # line_numbers_temporary_concepts = []

    for line, concept_information in concept_dict.items():
        _ = [y for x, y in concept_information if x == 'CONCEPTICON_GLOSS']

    pass


def temporary_gloss_has_null_id(concept_gloss: str, concept_id: int):
    # if CGL begins with ! then CID must be 0
    # else ...
    if is_temporary_concept(concept_gloss) and concept_id != 0:
        raise ValueError


def find_proposed_glosses(glosses_list: Glosses):
    return [gloss for gloss in glosses_list if gloss.startswith('!')]


def check_id_for_uniqueness(list_of_ids: IDs):
    gathered_ids = []

    for concept_id in list_of_ids:
        if concept_id not in gathered_ids:
            gathered_ids.append(concept_id)
        else:
            raise UniquenessError(concept_id)  # We can fail better, later on.


def check_if_gloss_in_concepticon(gloss: str):
    # Check for gloss existence in concepticon API ...
    _ = gloss
    pass


def get_all_concepticon_concepts():
    if os.path.isfile('all_concepts.p'):
        return pickle.load(open('all_concepts.p', 'rb'))
    else:
        concepticon_api = get_current_concepticon_data()
        concept_lists = [
            gloss for gloss in concepticon_api.conceptsets.values()
        ]
        all_concepts = set()

        for gloss in concept_lists:
            all_concepts.add(gloss.gloss)

        pickle.dump(all_concepts, open('all_concepts.p', 'wb'))
        return pickle.load(open('all_concepts.p', 'rb'))


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


headers_from_file = get_headers('Bangime_mapped_updated.txt')
concepts_w = concept_to_concept_row('Bangime_mapped_updated.txt', headers_from_file)

all_concepticon_concepts = get_all_concepticon_concepts()
sanity_check_concepts = []

for c in concepts_w:
    sanity_check_concepts.append(
        c.check_if_gloss_is_in_concepticon(all_concepticon_concepts)
    )

print(get_concepts_not_in_concepticon(sanity_check_concepts))
