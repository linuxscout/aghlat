#/usr/bin/sh
# Build arabic misspelling corpus
DATA=abdnormal.txt
default: all
# Clean build files
clean:
	
backup: 
	
#create all files 
all: 

build:DATA=abdnormal
build:
	python scripts/analyze_doc.py -f output/${DATA}.unq -o output/${DATA}.csv

# Publish to github
publish:
	git push origin master 
spellcheck:
	# generate suggestion for unkown words
#~ 	hunspell -d ar_DZ -a samples/${DATA}  > output/${DATA}.1.tmp
suggest:
	# select mispelled words with suggestion only
	grep "^& " output/${DATA}.1.tmp > output/${DATA}.tmp
	sed "s/: /\t/g" -i output/${DATA}.tmp
	# extract word input in colums to separate it
	cut -f1 output/${DATA}.tmp > output/${DATA}.input.tmp 
	sed "s/&//g" -i output/${DATA}.input.tmp  
	sed "s/ /\t/g" -i output/${DATA}.input.tmp  

	# extract word suggestion in colums to separate it
	cut -f2 output/${DATA}.tmp  > output/${DATA}.suggest.tmp 
	sed "s/, /;/g" -i output/${DATA}.suggest.tmp 
	# join files
	echo "word\tn1\tn2\tsuggest"| cat >output/${DATA}.csv
	paste output/${DATA}.input.tmp output/${DATA}.suggest.tmp >> output/${DATA}.csv
	rm output/*.tmp
	
join:
	python scripts/join.py -c join -f samples/${DATA}  -f2 output/${DATA}.csv -o output/${DATA}.corpus.csv 
	
suggest2:
	#tokenize
#~ 	scripts/tokenize.sh  tests/samples/abdnormal.txt  >  tests/output/abdnormal.tok 

	# generate suggestion for unkown words
#~ 	cd tests; hunspell -d ar_DZ -a output/abdnormal.tok  > output/abd.1.tmp
	# select mispelled words with suggestion only
#~ 	cd tests; grep "^& " output/abd.1.tmp > output/abd.tmp
	cp tests/output/abd.1.tmp tests/output/abd.tmp 
#~ 	sed "s/\*/\*\t/g" -i tests/output/abd.tmp
	# remove first line
	sed 1d -i tests/output/abd.tmp 
	# remove empty lines
	sed -e '/^$$/d' -i tests/output/abd.tmp 
	sed "s/: /\t/g" -i tests/output/abd.tmp 
	# extract word input in colums to separate it
	cut -f1 tests/output/abd.tmp >tests/output/input.tmp 
#~ 	sed "s/&//g" -i tests/output/input.tmp 
	sed "s/ /\t/g" -i tests/output/input.tmp 

	# extract word suggestion in colums to separate it
	cut -f2 tests/output/abd.tmp >tests/output/suggest.tmp 
	sed "s/, /;/g" -i tests/output/suggest.tmp 
	# join files
	#paste tests/output/abdnormal.tok tests/output/input.tmp tests/output/suggest.tmp > tests/output/abdo.csv
	
	

