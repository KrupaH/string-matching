# Keyword search using pattern matching algorithms
Comparing running time of naive pattern-matching, Knuth-Morris-Pratt pattern matching, and Rabin-Karp pattern matching algorithms using Python and Java.

Both packages takes a keyword "keyword" and a directory "dir" containing source files to search as command-line arguments.

For Python:
```
$python find-string.py -k keyword -s dir
```

For Java:
```
$javac java_source/FindString.java
$java java_source.FindString keyword dir
```

Note - The snowball package for Java is required to run the Java source, available at snowball.tartarus.org

#### TODO
Fix bugs in accepting single source file rather than directory as argument.
