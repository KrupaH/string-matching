package java_source;

public class kmp{
    public static Integer[] computeShiftTable(String word){
        int pos = 1;
        int nextCandidate = 0;
        Integer[] shiftTable = new Integer[word.length()];
        char[] keyword = word.toCharArray();

        shiftTable[0] = 0;

        while (pos < word.length()){
            if (keyword[pos] == keyword[nextCandidate]){
                nextCandidate += 1;
                shiftTable[pos] = nextCandidate;
                pos += 1;
            }
            else{
                if (nextCandidate != 0){
                    nextCandidate = shiftTable[nextCandidate-1];
                }
                else{
                    shiftTable[pos] = 0;
                    pos += 1;
                }
            }
        }
        return shiftTable;
    }

    public static int findKMPMatches(String str, String k, Integer[] shiftTable){
        int numMatches = 0;

        int M = k.length();
        int N = str.length();

        int i = 0; //index for string[]
        int j = 0; //index for keyword[]

        char[] string = str.toCharArray();
        char[] keyword = k.toCharArray();
        while (i < N){
            if (keyword[j] == string[i]){
                i += 1;
                j += 1;
            }

            if (j == M){
                numMatches += 1;
                j = shiftTable[j-1];
            }

            //mismatch after j matches
            else if (i < N && keyword[j] != string[i]){
                //Do not match shiftTable[0..shiftTable[j-1]] characters,
                //they will match anyway
                if (j != 0)
                    j = shiftTable[j-1];
                else
                    i += 1;
            }
        }
        return numMatches;
    }
}
