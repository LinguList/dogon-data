from pyclts.clts import CLTS
from lingpy.read.csv import csv2list
from collections import defaultdict
from tabulate import tabulate

BIPA = CLTS('bipa')


class SegmentsInProfile:
    """
    Map a segment or a list of segments to their
    respective line in an orthography profile.
    """

    def __init__(self, segment_list, profile_line):
        self.segment_list = segment_list
        self.profile_line = profile_line

        self.segment_info = {
            profile_line: segment_list
        }


def profile_to_segment_list(profile_tsv_path):
    row_number = 1
    segments = []

    for row in csv2list(profile_tsv_path)[1:]:
        row_number += 1
        segments.append(
            SegmentsInProfile(
                row[1].split('/')[1]
                if '/' in row[1] else
                row[1].split(' '), row_number
            )
        )

    return segments


def check_conformity(segment_dict):
    conformity_dict = {}

    def check_bipa(segment_bipa_check):
        is_in_bipa = segment_bipa_check in BIPA

        return [segment_bipa_check, is_in_bipa]

    for line, segment_list in segment_dict.items():
        local_segments = []

        for segment in segment_list:
            local_segments.append(check_bipa(segment))

        conformity_dict = {
            line: local_segments
        }

    return conformity_dict


def aggregate_segments(segment_dicts):
    aggregated_segments = defaultdict(list)

    for segment_dict in segment_dicts:
        for line, segments in segment_dict.segment_info.items():
            for segment in segments:
                aggregated_segments[segment].append(line)

    return aggregated_segments


def in_bipa(char):
    bchar = BIPA[char]

    if bchar.type == 'unknownsound':
        return char, '?', 'unknown'
    if bchar.generated:
        return char, str(bchar), 'generated'
    if str(bchar) != char:
        return char, str(bchar), 'normalized'

    return char, str(bchar), ''


def make_table(aggregated_items):
    table_data = []

    def is_normalized(f):
        if f == 'normalized':
            return True
        else:
            return False

    def is_alias(f):
        if f == 'alias':
            return True
        else:
            return False

    def is_generated(f):
        if f == 'generated':
            return True
        else:
            return False

    for k, v in aggregated_items.items():
        _, bipa_sugg, feature = in_bipa(k)

        tmp = [
            k,
            bipa_sugg,
            v,
            is_normalized(feature),
            is_alias(feature),
            is_generated(feature),
        ]

        table_data.append(tmp)

    return table_data


def tabulate_print_table(table_data):
    headers = [
        'Sound Source',
        'BIPA Suggestion',
        'Lines in Profile',
        'Normalized',
        'Alias',
        'Generated',
    ]

    return str(tabulate(table_data, headers=headers, tablefmt='grid'))
