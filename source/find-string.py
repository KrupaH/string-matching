import argparse
import os
import unicodedata
import operator

from nltk.stem import *
from nltk.tokenize import RegexpTokenizer
from timeit import default_timer as timer


#TODO: Mandatory arguments
parser = argparse.ArgumentParser(description='Keyword search')
parser.add_argument("-s","--source",help="source file/directory to search for keyword(s)")
parser.add_argument("-k","--keyword",help="keyword to be found in the file(s)")
args = parser.parse_args()
filedict = {}

time_wordmatch = 0
time_KMP = 0

#Function matching stemmed keyword to stemmed words in the file and storing number of occurrences
def findWordOccurrences(words,keyword):
    numOccurrences = 0
    for word in words:
        if word == keyword:
            numOccurrences += 1
    return numOccurrences

#Function to search for the keyword for each line of a source file
def keywordSearch(source, keyword, filename):
    global time_wordmatch, time_KMP
    numIterations = 0

    stemmer = SnowballStemmer("english")
    tokenizer = RegexpTokenizer(r'\w+')
    numOccurrences = 0
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
        numOccurrences += findWordOccurrences(words,keyword)
        end = timer()
        time_wordmatch += (end-start)
        numIterations += 1

        filedict[filename] = numOccurrences

#TODO: Check if path is valid

#stem the keyword
stemmer = LancasterStemmer()

#Perform search for each file in the directory and store results
if os.path.isfile(os.path.abspath(args.source)):
    keywordSearch(args.source,args.keyword)
else:
    for root, dirs, filenames in os.walk(args.source):
        for f in filenames:
            log = open(os.path.join(root,f), 'r')
            keywordSearch(log,args.keyword,f)
print("Direct word-comparison search: " + str(time_wordmatch) + " s")


#sort list of files based on occurrences
sortedList = sorted(filedict.items(), key=operator.itemgetter(1), reverse=True)
opfilename = "../output/op_"+args.keyword+".txt"
opfile = open(opfilename,"w")

#Store ordered ranking of files based on number of occurrences of keyword
opfile.write("Occurrences\tFiles\n")
for item in sortedList:
    opfile.write(str(item[1]) + '\t' + item[0] + '\n')
