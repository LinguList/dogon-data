import codecs
import logging
import os.path
import pickle
import zipfile
from itertools import zip_longest
from urllib import request
import sys

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
                'http://github.com/clld/concepticon-data/archive/master.zip'
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
            self.__annotate_row_elements(concept_information, header_list)

        self.concept_dict = {
            concept_line: annotated_concept_information
        }

    @staticmethod
    def __annotate_row_elements(concept_information, header_list):
        if len(concept_information) > len(header_list):
            return list(
                zip_longest(
                    header_list, concept_information, fillvalue='MISSING_HEADER'
                )
            )
        elif len(concept_information) < len(header_list):
            return list(
                zip_longest(
                    header_list, concept_information, fillvalue='MISSING_VALUE'
                )
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

    def check_if_gloss_matches_id(self, concepticon_concepts):
        for line, concept_information in self.concept_dict.items():
            gloss = [value for header, value
                     in concept_information
                     if header == 'CONCEPTICON_GLOSS'][0]

            concepticon_id = [value for header, value
                              in concept_information
                              if header == 'CONCEPTICON_ID'][0]

            if concepticon_id and concepticon_concepts[concepticon_id] == gloss:
                return True, line, gloss
            else:
                return False, line, gloss

    def check_if_proposed_gloss(self):
        """
        If a gloss is proposed (starts with '!'), returns (True, line, gloss).
        """
        for line, concept_information in self.concept_dict.items():
            gloss = [value for header, value
                     in concept_information
                     if header == 'CONCEPTICON_GLOSS'][0]

            return\
                (True, line, gloss)\
                if gloss.startswith('!') else\
                (False, line, gloss)

    def check_if_proposed_gloss_has_null_id(self):
        """
        If a gloss is proposed (starts with '!') returns (True, line, gloss)
        if the CONCEPTICON_ID is empty. If a gloss is proposed and the ID field
        is not empty, returns (False, line, gloss).
        """
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
            elif not gloss.startswith('!') and (int(concepticon_id or 0) > 0 or concepticon_id):
                return True, line, gloss
            else:
                return False, line, gloss

    def check_if_id_unique(self, list_of_concept_rows):
        clashing_ids = []

        def __get_local_id():
            for line, concept_information in self.concept_dict.items():
                id_col = [value for header, value
                          in concept_information if header == 'ID'][0]

                return line, id_col

        local = __get_local_id()

        def __rest():
            for concept_row in list_of_concept_rows:
                for line, concept_information in concept_row.\
                        concept_dict.items():
                    id_col = [value for header, value
                              in concept_information if header == 'ID'][0]

                    if local != (line, id_col) and local[1] == id_col:
                        clashing_ids.append((line, id_col))

        __rest()

        if clashing_ids:
            clashing_ids.insert(0, local)

        return clashing_ids

    def check_if_concepticon_id_unique(self, list_of_concept_rows):
        clashing_concepticon_ids = []

        def __get_local_id():
            for line, concept_information in self.concept_dict.items():
                concepticon_id = [
                    value for header, value in
                    concept_information if header == 'CONCEPTICON_ID'
                ][0]

                return line, concepticon_id

        local = __get_local_id()

        def __rest():
            for concept_row in list_of_concept_rows:
                for line, concept_information in concept_row.\
                        concept_dict.items():
                    concepticon_id = [
                        value for header, value
                        in concept_information
                        if header == 'CONCEPTICON_ID'
                    ][0]

                    if local != (line, concepticon_id)\
                            and local[1] == concepticon_id:
                        clashing_concepticon_ids.append((line, concepticon_id))

        __rest()

        if clashing_concepticon_ids:
            clashing_concepticon_ids.insert(0, local)

        return clashing_concepticon_ids


def get_headers(concept_tsv_path):
    try:
        with codecs.open(concept_tsv_path, 'r', 'utf-8-sig') as f:
            return f.readline().rstrip('\r\n').split('\t')
    except (UnicodeDecodeError, UnicodeEncodeError, UnicodeError) as e:
        print(e)
        print("Unicode problem. Is " + concept_tsv_path + " saved as UTF-8?")
        sys.exit(0)


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


input_file_concepts = 'Bangime_mapped_updated.txt'

concepts_from_file = concept_to_concept_row(
    input_file_concepts, get_headers(input_file_concepts)
)

x = 1