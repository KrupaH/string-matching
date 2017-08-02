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
