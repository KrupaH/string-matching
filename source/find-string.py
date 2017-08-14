import argparse
import os
import unicodedata
import operator

from nltk.stem import *
from nltk.tokenize import RegexpTokenizer
from timeit import default_timer as timer

import kmp
import rk
import wordsearch
import re


#TODO: Mandatory arguments
parser = argparse.ArgumentParser(description='Keyword search')
parser.add_argument("-s","--source",help="source file/directory to search for keyword(s)")
parser.add_argument("-k","--keyword",help="keyword to be found in the file(s)")
args = parser.parse_args()
filedict = {}

time_wordmatch = 0
time_KMP_stem = 0
time_KMP_nostem = 0
time_RK_stem = 0
time_RK_nostem = 0

#Function to search for the keyword in the source file
def keywordSearch(source, keyword, filename):
    global time_wordmatch, time_KMP_stem, time_KMP_nostem, time_RK_nostem, time_RK_stem

    stemmer = SnowballStemmer("english")
    tokenizer = RegexpTokenizer(r'\w+')
    numOccurrences = 0
    numMatches_KMP_stem = 0
    numMatches_KMP_nostem = 0
    numMatches_RK_stem = 0
    numMatches_RK_nostem = 0

    keyword_stem = stemmer.stem(keyword)

    shiftTable_stem = kmp.computeShiftTable(keyword_stem)
    shiftTable_nostem = kmp.computeShiftTable(keyword)

    text = source.read()
    pos = 0

    #get words from text
    wordlist = tokenizer.tokenize(text)
    #stem words
    wordlist = [stemmer.stem(word) for word in wordlist]

    #normalize unicode strings
    words = ""
    for word in wordlist:
        if isinstance(word, unicode):
            words = words + " " + str(unicodedata.normalize('NFKD', word).encode('ascii','ignore'))
        else:
            words = words + " " + word

    #Time finding number of word occurences with simple word match
    start = timer()
    numOccurrences += wordsearch.findWordOccurrences(words,keyword_stem)
    end = timer()
    time_wordmatch += (end-start)

    #Time finding number of word matches using Rabin-Karp algorithm with stemming
    start = timer()
    numMatches_RK_stem += rk.findRKMatches(words,keyword_stem)
    end = timer()
    time_RK_stem += (end-start)

    #Time finding number of word matches using Rabin-Karp algorithm without stemming
    start = timer()
    numMatches_RK_nostem += rk.findRKMatches(text,keyword)
    end = timer()
    time_RK_nostem += (end-start)

    #Time finding number of word matches using KMP string matching with stemming
    start = timer()
    numMatches_KMP_stem += kmp.findKMPMatches(words,keyword_stem,shiftTable_stem)
    end = timer()
    time_KMP_stem += (end-start)

    #Time finding number of word matches using KMP string matching without stemming
    start = timer()
    numMatches_KMP_nostem += kmp.findKMPMatches(text, keyword, shiftTable_nostem)
    end = timer()
    time_KMP_nostem += (end-start)

    filedict[filename] = [numOccurrences,numMatches_RK_stem,numMatches_RK_nostem,numMatches_KMP_stem,numMatches_KMP_nostem]

#TODO: Check if path is valid

#Perform search for each file in the directory and store results
if os.path.isfile(os.path.abspath(args.source)):
    keywordSearch(args.source,args.keyword)
else:
    for root, dirs, filenames in os.walk(args.source):
        for f in filenames:
            if os.path.splitext(f)[1] == '.txt':
                print "Processing " + f + "..."
                log = open(os.path.join(root,f), 'r')
                keywordSearch(log,args.keyword,f)

print("------------------------------------------")
print("Direct word-comparison search time: " + str(time_wordmatch) + " s")
print ("RK string-matching with stemming search time: " + str(time_RK_stem) + " s")
print ("RK string-matching without stemming search time: " + str(time_RK_nostem) + " s")
print("KMP string-matching with stemming search time: "+str(time_KMP_stem)+" s")
print("KMP string-matching without stemming search time: "+str(time_KMP_nostem)+" s")


#sort list of files based on occurrences
sortedList = sorted(filedict.items(), key=operator.itemgetter(1), reverse=True)
opfilename = "../output/op_"+args.keyword+".txt"
opfile = open(opfilename,"w")

#Store ordered ranking of files based on number of occurrences of keyword
opfile.write("Occurrences\tFiles\n")
for item in sortedList:
    opfile.write(str(item[1]) + '\t' + item[0] + '\n')
