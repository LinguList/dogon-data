import C_check_clts_conformity
import codecs

profile_as_segments =\
    C_check_clts_conformity.profile_to_segment_list('D_profile.tsv')
aggregated =\
    C_check_clts_conformity.aggregate_segments(profile_as_segments)
t =\
    C_check_clts_conformity.make_table(aggregated)

with codecs.open('CLTS_out.txt', 'w', encoding='utf-8') as text_file:
    s = C_check_clts_conformity.tabulate_print_table(t)
    text_file.write(s)