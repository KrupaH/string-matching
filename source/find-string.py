import argparse
import os
from nltk.stem import *
from nltk.tokenize import RegexpTokenizer
import unicodedata

parser = argparse.ArgumentParser(description='Keyword search')
parser.add_argument("-s","--source",help="source file/directory to search for keyword(s)")
parser.add_argument("-k","--keyword",help="keyword to be found in the file(s)")
args = parser.parse_args()

#Function implementing Knuth-Morris-Pratt string matching to find keyword in source file
def findWordOccurrences(words,keyword):
    numOccurrences = 0
    for word in words:
        if word == keyword:
            numOccurrences += 1
    return numOccurrences

#Function to implement KMP algorithm for each line of source file
def keywordSearch(source, keyword, outputfile):
    stemmer = LancasterStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    numOccurrences = 0
    with open(outputfile,"w") as opfile:
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
                    words = words + unicodedata.normalize('NFKD', word).encode('ascii','ignore')
                else:
                    words = words + [word]

            numOccurrences += findWordOccurrences(words,keyword)
        opfile.write(str(numOccurrences))

        opfile.close()

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
            opfile = "../output/op_"+f
            keywordSearch(log,args.keyword,opfile)
