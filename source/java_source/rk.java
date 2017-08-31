package java_source;

import java.lang.Math;
//Module to find matches using enhanced Rabin-Karp algorithm
/*
Parameters:
S = String
P = Pattern
q = a prime number
*/
public class rk{
    public static int findRKMatches(String S,String P){
        int n = S.length();
        int m = P.length();
        int q = 3;

        char[] string = S.toCharArray();
        char[] keyword = P.toCharArray();

        //If word is smaller than keyword
        if (n<m)
            return 0;
        else if (n==m && P.equalsIgnoreCase(S))
            return 1;

        int d = 256; //Number of characters in input alphabet

        double h = Math.pow(d,m-1) % q;
        double p = 0.0; //Hash value for pattern P
        double s = 0.0; //Hash value for string S

        int numMatched = 0;
        int pos = 0;

        //Compute hash values
        for (int i=0 ; i<m ; i++){
            p = (d*p + (int)(keyword[i]))%q;
            s = (d*s + (int)(string[i]))%q;
        }
        //Compare substring of String only if hash value matches
        for (int i=0 ; i<n-m+1 ; i++){
            if (p==s)
                if (P.equalsIgnoreCase(S.substring(i,i+m))){
                    pos = i+1;
                    numMatched += 1;
                }

            //Recompute hash value for next substring
            if (i<n-m){
                s = ((d*(s-(int)(string[i])*h)) + (int)(string[i+m]))%q;
                if (s<0)
                    s += q;
            }
        }
        return numMatched;
    }
}
