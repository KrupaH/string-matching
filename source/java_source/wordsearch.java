package java_source;

public class wordsearch{
    public static int findWordOccurrences(String text, String keyword){
        int numOccurrences = 0;
        String[] words = text.split("\\P{Alpha}+");
        for (String word : words)
            if (word.equalsIgnoreCase(keyword))
                numOccurrences += 1;
        return numOccurrences;
    }
}
