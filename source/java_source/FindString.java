package java_source;

import java.util.*;
import java.lang.*;
import java.io.*;
import java.nio.file.*;

import org.tartarus.snowball.*;

public class FindString{
    public static Hashtable<String, String> filedict = new Hashtable<>();
    public static Double CONVERSION_FACTOR = 1000000.0;

    public static void main(String[] args) throws Throwable{
        Double[] times = new Double[5]; //time_wordmatch, time_RK_stem, time_RK_nostem, time_KMP_stem, time_KMP_nostem,
        for(int i=0 ; i<5 ; i++) times[i] = 0.0;

        String path = args[1];
        String keyword = args[0];

        File file = new File(path);

        if(file.isFile()){
            times = keywordSearch(path,keyword,file);
        }
        else if(file.isDirectory()){
            File[] files = new File(path).listFiles();
            for(File src: files){
                if(!Files.isHidden(src.toPath())){
                    System.out.println("Processing "+src+"...");
                    Double[] temp = new Double[5];
                    temp = keywordSearch(src.getName(),keyword,src);

                    for(int i=0 ; i<5 ; i++) times[i] += temp[i];
                }
            }
        }
        else{
            System.out.println("Invalid file/path name");
            System.exit(1);
        }

        System.out.println("------------------------------------------");
        System.out.println("Direct word-comparison search time: " + times[0] + " ms");
        System.out.println ("RK string-matching with stemming search time: " + times[1] + " ms");
        System.out.println ("RK string-matching without stemming search time: " + times[2] + " ms");
        System.out.println("KMP string-matching with stemming search time: "+ times[3] +" ms");
        System.out.println("KMP string-matching without stemming search time: "+ times[4] +" ms");

        ArrayList<Map.Entry<String, String>> sortedList = new ArrayList(filedict.entrySet());
        Collections.sort(sortedList, new Comparator<Map.Entry<?, String>>(){
            public int compare(Map.Entry<?, String> o1, Map.Entry<?, String> o2) {
                return o2.getValue().compareTo(o1.getValue());
        }});

        String opfilename = "../output/op_java_"+keyword+".txt";
        Writer writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(opfilename), "utf-8"));
        writer.write("Occurrences\tFiles\n");
        for(Map.Entry item : sortedList){
            writer.write(item.getValue() + "\t" + item.getKey() + "\n");
        }
        writer.close();
    }

    private static Double[] keywordSearch(String filename, String keyword, File file) throws Throwable{
        Double[] times = new Double[5];
        for(int i=0 ; i<5 ; i++) times[i] = 0.0;

        Class stemClass = Class.forName("org.tartarus.snowball.ext.englishStemmer");
        SnowballStemmer stemmer = (SnowballStemmer) stemClass.newInstance();

        Integer numOccurrences = 0,
            numMatches_KMP_stem = 0,
            numMatches_KMP_nostem = 0,
            numMatches_RK_stem = 0,
            numMatches_RK_nostem = 0;

        //Stem the keyword
        stemmer.setCurrent(keyword);
        stemmer.stem();
        String keyword_stem = stemmer.getCurrent();

        //Compute shift tables
        Integer[] shiftTable_stem = kmp.computeShiftTable(keyword_stem);
        Integer[] shiftTable_nostem = kmp.computeShiftTable(keyword);

        //Read contents from file
        List<String> lines = Files.readAllLines(file.toPath());
        String text = new String();
        String stemmed_text = new String();

        //Create "text" containing all lines of file and "stemmed_text" containing all stemmed words of file
        for(String line : lines){
            text = text + " " + line;
            for (String word : line.split("\\W")){
                //Stem word and add to stemmed_text
                stemmer.setCurrent(word);
                stemmer.stem();
                word = stemmer.getCurrent();
                stemmed_text += " " + word;
            }
        }
        int pos = 0;
        double start = 0.0;
        double end = 0.0;

        //Time finding number of word occurences with simple word match
        start = System.nanoTime();
        numOccurrences += wordsearch.findWordOccurrences(stemmed_text,keyword_stem);
        end = System.nanoTime();
        times[0] += (end-start)/CONVERSION_FACTOR;

        //Time finding number of word matches using Rabin-Karp algorithm with stemming
        start = System.nanoTime();
        numMatches_RK_stem += rk.findRKMatches(stemmed_text,keyword_stem);
        end = System.nanoTime();
        times[1] += (end-start)/CONVERSION_FACTOR;

        //Time finding number of word matches using Rabin-Karp algorithm without stemming
        start = System.nanoTime();
        numMatches_RK_nostem += rk.findRKMatches(text,keyword);
        end = System.nanoTime();
        times[2] += (end-start)/CONVERSION_FACTOR;

        //Time finding number of word matches using KMP string matching with stemming
        start = System.nanoTime();
        numMatches_KMP_stem += kmp.findKMPMatches(stemmed_text,keyword_stem,shiftTable_stem);
        end = System.nanoTime();
        times[3] += (end-start)/CONVERSION_FACTOR;

        //Time finding number of word matches using KMP string matching without stemming
        start = System.nanoTime();
        numMatches_KMP_nostem += kmp.findKMPMatches(text, keyword, shiftTable_nostem);
        end = System.nanoTime();
        times[4] += (end-start)/CONVERSION_FACTOR;

        String list = Integer.toString(numOccurrences) + " " + Integer.toString(numMatches_RK_stem) + " " + Integer.toString(numMatches_RK_nostem) + " " + Integer.toString(numMatches_KMP_stem) + " " + Integer.toString(numMatches_KMP_nostem);

        filedict.put(filename,list);

        return times;
    }
}
