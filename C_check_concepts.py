from lingpy.read.csv import csv2list
from typing import List

Glosses=List[str]
IDs=List[int]

class ProposedConcept:
    """Description."""

    def __init__(self, concept_id, line):
        self.concept_id = concept_id
        self.line = line

        self.concept_dict = {
            line: id
        }


class UniquenessError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def concept_to_proposed(concept_tsv_path):
    row_number = 1
    concepts = []

    def is_id(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    # Is there a better way to ignore comments completely, i.e. read the file
    # 'raw'? If not, suggest/issue 'None' as argument.
    for row in csv2list(concept_tsv_path, comment=None)[1:]:
        row_number += 1

        if is_id(row[0]):
            concepts.append(
                ProposedConcept(row[0], row_number)
            )

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
    pass

# Find glosses with ! as proposed new glosses

# Check ID column for uniqueness
# Check concepticon API for proper gloss

# ------------------
# ID ENG
# 1
# 1
# ------------------


concepts_w = concept_to_proposed('D_dogon-concepts.tsv')
# print(concepts_w[3].concept_id)
# print(concepts_w[3].line)

check_uniqueness(concepts_w)