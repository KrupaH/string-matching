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

#Function matching stemmed keyword to stemmed words in the file and storing number of occurrences
def findWordOccurrences(words,keyword):
    numOccurrences = 0
    for word in words:
        if word == keyword:
            numOccurrences += 1
    return numOccurrences

#Function to search for the keyword for each line of a source file
def keywordSearch(source, keyword, filename):
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

        numOccurrences += findWordOccurrences(words,keyword)
        filedict[filename] = numOccurrences

#TODO: Check if path is valid

#stem the keyword
stemmer = LancasterStemmer()

start = timer()
#Perform search for each file in the directory and store results
if os.path.isfile(os.path.abspath(args.source)):
    keywordSearch(args.source,args.keyword)
else:
    for root, dirs, filenames in os.walk(args.source):
        for f in filenames:
            log = open(os.path.join(root,f), 'r')
            keywordSearch(log,args.keyword,f)
end = timer()
print("Direct word-comparison search: " + str(end-start) + " s")

#sort list of files based on occurrences
sortedList = sorted(filedict.items(), key=operator.itemgetter(1), reverse=True)
opfilename = "../output/op_"+args.keyword+".txt"
opfile = open(opfilename,"w")

#Store ordered ranking of files based on number of occurrences of keyword
opfile.write("Occurrences\tFiles\n")
for item in sortedList:
    opfile.write(str(item[1]) + '\t' + item[0] + '\n')
