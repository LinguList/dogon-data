# Get the raw data from the Dogon-data repository
wget -O data/Dogon.comp.vocab.UNICODE-2017.xls https://github.com/clld/dogonlanguages-data/raw/master/beta/Dogon.comp.vocab.UNICODE-2017.xls

# Convert it to csv and keep the relevant data for analysis
in2csv data/Dogon.comp.vocab.UNICODE-2017.xls | csvcut -c 1,2,3,4,5,6,7,8,9,10,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43 > D_dogon-wordlist.csv
