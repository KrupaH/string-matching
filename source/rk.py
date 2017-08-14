#Module to find matches using enhanced Rabin-Karp algorithm
import math

"""
Parameters:
S = String
P = Pattern
q = a prime number
"""
def rabinKarp(S,P,q):
    n = len(S)
    m = len(P)

    #If word is smaller than keyword
    if n<m:
        return 0
    elif n==m and P==S:
        return 1

    d = 256 #Number of characters in input alphabet

    h = math.pow(d,m-1) % q
    p = 0 #Hash value for pattern P
    s = 0 #Hash value for string S

    numMatched = 0

    #Compute hash values
    for i in xrange(m):
        p = (d*p + ord(P[i]))%q
        s = (d*s + ord(S[i]))%q

    #Compare substring of String only if hash value matches
    for i in xrange(n-m+1):
        if p==s:
            if P == S[i:i+m]:
                pos = i+1
                numMatched += 1

        #Recompute hash value for next substring
        if i<n-m:
            s = ((d*(s-ord(S[i])*h)) + ord(S[i+m]))%q
            if s<0:
                s += q

    return numMatched

def findRKMatches(string, keyword):
    string = " ".join(string)
    return rabinKarp(string,keyword,3)
