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


class UniquenessError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def get_headers(concept_tsv_path):
    with codecs.open(concept_tsv_path, 'r', 'utf-8') as f:
        return f.readline().rstrip('\r\n').split('\t')


def concept_to_proposed(concept_tsv_path, headers):
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


def temporary_gloss_has_null_id(concept_gloss: str, concept_id: int):
    # if CGL beginswith ! then CID must be 0
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

# Find glosses with ! as proposed new glosses

# Check ID column for uniqueness
# Check concepticon API for proper gloss

# ------------------
# ID ENG
# 1
# 1
# ------------------
