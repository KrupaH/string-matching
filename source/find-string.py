import argparse
import os
import unicodedata
import operator

from nltk.stem import *
from nltk.tokenize import RegexpTokenizer
from timeit import default_timer as timer

import kmp
import wordsearch


#TODO: Mandatory arguments
parser = argparse.ArgumentParser(description='Keyword search')
parser.add_argument("-s","--source",help="source file/directory to search for keyword(s)")
parser.add_argument("-k","--keyword",help="keyword to be found in the file(s)")
args = parser.parse_args()
filedict = {}

time_wordmatch = 0
time_KMP = 0
time_KMP_nostem = 0

#Function to search for the keyword for each line of a source file
def keywordSearch(source, keyword, filename):
    global time_wordmatch, time_KMP, time_KMP_nostem

    stemmer = SnowballStemmer("english")
    tokenizer = RegexpTokenizer(r'\w+')
    numOccurrences = 0
    numMatches_KMP_stem = 0
    numMatches_KMP_nostem = 0

    keyword_stem = stemmer.stem(keyword)

    shiftTable_stem = kmp.computeShiftTable(keyword_stem)
    shiftTable_nostem = kmp.computeShiftTable(keyword)

    while True:
        line = source.readline()
        if not line:
            break
        #get words from line
        wordlist = tokenizer.tokenize(line)
        #stem words
        wordlist = [stemmer.stem(word) for word in wordlist]

        #normalize unicode strings
        words = []
        for word in wordlist:
            if isinstance(word, unicode):
                words = words + [unicodedata.normalize('NFKD', word).encode('ascii','ignore')]
            else:
                words = words + [word]

        #Time finding number of word occurences with simple word match
        start = timer()
        numOccurrences += wordsearch.findWordOccurrences(words,keyword_stem)
        end = timer()
        time_wordmatch += (end-start)

        filedict[filename] = numOccurrences

        #Time finding number of word matches using KMP string matching with stemming
        start = timer()
        numMatches_KMP_stem += kmp.findKMPMatches(words,keyword_stem,shiftTable_stem)
        end = timer()
        time_KMP += (end-start)

        #Time finding number of word matches using KMP string matching without stemming
        start = timer()
        numMatches_KMP_nostem += kmp.findKMPMatches(line, keyword, shiftTable_nostem)
        end = timer()
        time_KMP_nostem += (end-start)

#TODO: Check if path is valid

#Perform search for each file in the directory and store results
if os.path.isfile(os.path.abspath(args.source)):
    keywordSearch(args.source,args.keyword)
else:
    for root, dirs, filenames in os.walk(args.source):
        for f in filenames:
            log = open(os.path.join(root,f), 'r')
            keywordSearch(log,args.keyword,f)


print("Direct word-comparison search time: " + str(time_wordmatch) + " s")
print("KMP string-matching with stemming search time: "+str(time_KMP)+" s")
print("KMP string-matching without stemming search time: "+str(time_KMP_nostem)+" s")

#sort list of files based on occurrences
sortedList = sorted(filedict.items(), key=operator.itemgetter(1), reverse=True)
opfilename = "../output/op_"+args.keyword+".txt"
opfile = open(opfilename,"w")

#Store ordered ranking of files based on number of occurrences of keyword
opfile.write("Occurrences\tFiles\n")
for item in sortedList:
    opfile.write(str(item[1]) + '\t' + item[0] + '\n')
