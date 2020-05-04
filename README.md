py_wordcloud
---

Outputs HTML word cloud d3.js code from text file.

```
usage: wordcloud [-h] [-o OUTPUT] [-w MAX_WORDS]
                 [-x EXCLUDE_WORDS] [-e ENCODING]
                 input

positional arguments:
  input                 input file name

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file name
  -w MAX_WORDS, --max-words MAX_WORDS
                        maximum number of words (default: 100)
  -x EXCLUDE_WORDS, --exclude-words EXCLUDE_WORDS
                        list of words to ignore (comma separated)
  -e ENCODING, --encoding ENCODING
                        file encoding (default: utf-8)
```

Included is a list of stopwords to ignore on read:
* Catalan: 825
* Chinese: 119
* English: 777
* French: 1317
* German: 616
* Italian: 443
* Japanese: 44
* Portuguese: 806
* Russian: 421
* Spanish: 491

Based on the Python code from twarc:
* https://github.com/DocNow/twarc/

Original wordcloud implementation by Jason Davies:
* http://github.com/jasondavies/d3-cloud
