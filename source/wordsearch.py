#Function matching stemmed keyword to stemmed words in the file and returning number of occurrences
def findWordOccurrences(words,keyword):
    numOccurrences = 0
    for word in words:
        if word == keyword:
            numOccurrences += 1
    return numOccurrences
