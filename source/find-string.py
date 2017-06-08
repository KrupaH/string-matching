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

#Function matching stemmed keyword to stemmed words in the file and returning number of occurrences
def findWordOccurrences(words,keyword):
    numOccurrences = 0
    for word in words:
        if word == keyword:
            numOccurrences += 1
    return numOccurrences

#Helper function to compute the shift table for KMP string matching
def computeShiftTable(keyword):
    pos = 1
    nextCandidate = 0
    shiftTable = [None for x in range(len(keyword)+1)]

    shiftTable[0] = -1

    while (pos < len(keyword)):
        if keyword[pos] == keyword[nextCandidate]:
            shiftTable[pos] = shiftTable[nextCandidate]
            pos += 1
            nextCandidate += 1
        else:
            shiftTable[pos] = nextCandidate
            nextCandidate = shiftTable[nextCandidate]

            while (nextCandidate >= 0 and keyword[pos] != keyword[nextCandidate]):
                nextCandidate = shiftTable[nextCandidate]

            pos += 1
            nextCandidate += 1

        shiftTable[pos] = nextCandidate

    return shiftTable


#Function using enhanced KMP string matching to find number of matches in stemmed word list
def findKMPMatches(words,keyword, shiftTable):
    numMatches = 0

    for word in words:
        #TODO: Convert KMP to enhanced KMP
        curMatch = 0
        curChar = 0

        while ((curMatch + curChar) < len(word)):
            if keyword[curChar] == word[curMatch+curChar]:
                curChar += 1
                if curChar == len(keyword):
                    numMatches += 1
                    break
            else:
                if shiftTable[curChar] > -1:
                    curMatch += curChar - shiftTable[curChar]
                    curChar = shiftTable[curChar]
                else:
                    curMatch += curChar + 1
                    curChar = 0

    return numMatches

#Function to search for the keyword for each line of a source file
def keywordSearch(source, keyword, filename):
    global time_wordmatch, time_KMP

    stemmer = SnowballStemmer("english")
    tokenizer = RegexpTokenizer(r'\w+')
    numOccurrences = 0
    numMatches = 0

    shiftTable = computeShiftTable(keyword)

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

        filedict[filename] = numOccurrences

        #Time finding number of word matches using KMP string matching
        start = timer()
        numMatches += findKMPMatches(words,keyword,shiftTable)
        end = timer()
        time_KMP += (end-start)

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
print("Direct word-comparison search time: " + str(time_wordmatch) + " s")
print("KMP string-matching search time: "+str(time_KMP)+" s")


#sort list of files based on occurrences
sortedList = sorted(filedict.items(), key=operator.itemgetter(1), reverse=True)
opfilename = "../output/op_"+args.keyword+".txt"
opfile = open(opfilename,"w")

#Store ordered ranking of files based on number of occurrences of keyword
opfile.write("Occurrences\tFiles\n")
for item in sortedList:
    opfile.write(str(item[1]) + '\t' + item[0] + '\n')
