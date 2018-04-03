@Mattis/@Chris - which one of these is the final for concept sanity checks?

C_check_clts_conformity.py
C_check_concepts_out.py
C_check_concepts.py

check orthography profile:

check_profile.py

convert wordlists for reading into Edictor:
C_convert.py
C_download.sh

run output of my pass with Edictor through SCA/LexStat which I then go through again comparing differences:
compare.py

map wordlist glosses to concepticon concepts:
concept_mapping.sh

determine coverage statistics and extract best coverage concepts/doculects:
coveragestats-blacklist.pyc
coveragestats-noblacklist.py
extract.py

converting data to a wordlist:
make-wordlist

merging different wordlists:
merge.py

making a html map:
plot_map