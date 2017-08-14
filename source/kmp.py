#Function using enhanced KMP string matching to find number of matches in stemmed word list
def findKMPMatches(string,keyword,shiftTable):
    numMatches = 0

    M = len(keyword)
    N = len(string)

    i = 0 # index for string[]
    j = 0 #index for keyword[]
    while i < N:
        if keyword[j] == string[i]:
            i += 1
            j += 1

        if j == M:
            numMatches += 1
            j = shiftTable[j-1]

        # mismatch after j matches
        elif i < N and keyword[j] != string[i]:
            # Do not match shiftTable[0..shiftTable[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = shiftTable[j-1]
            else:
                i += 1
    return numMatches

#Helper function to compute the shift table for KMP string matching
def computeShiftTable(keyword):
    pos = 1
    nextCandidate = 0
    shiftTable = [0]*(len(keyword))

    shiftTable[0] = 0

    while (pos < len(keyword)):
        if keyword[pos] == keyword[nextCandidate]:
            nextCandidate += 1
            shiftTable[pos] = nextCandidate
            pos += 1
        else:
            if nextCandidate != 0:
                nextCandidate = shiftTable[nextCandidate-1]
            else:
                shiftTable[pos] = 0
                pos += 1

    return shiftTable
