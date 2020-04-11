#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Outputs HTML word cloud d3.js code from text file.

usage: wordcloud.py [-h] [-o OUTPUT] [-w MAX_WORDS] [-x EXCLUDE_WORDS] input

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

Based on the Python code from twarc:
* https://github.com/DocNow/twarc/

Original d3.js wordcloud code by Jason Davies:
* http://github.com/jasondavies/d3-cloud
"""

import json

from argparse import ArgumentParser
from collections import defaultdict
from os.path import dirname, isfile, realpath
from string import punctuation
from urllib.request import urlopen

from stopwords import CUSTOM_STOPWORDS

URL = 'https://raw.githubusercontent.com/jasondavies/d3-cloud/master/build/d3.layout.cloud.js'

def wordcloud(input_name, output_name=None,
    max_words=100, exclude_words=[]):
    '''
    Generate cloud from word count dictionary.
    '''
    words = []

    dict_int_words = defaultdict(int)
    dict_str_words = defaultdict(str)

    if isinstance(exclude_words, str):
        exclude_words = exclude_words.replace(', ',',').split(',')

    with open(input_name, 'rt', errors='ignore') as f:
        for line in f.readlines():
            for word in line.split():
                for punct in punctuation:
                    word = word.replace(punct,'')
                if len(word)>1:
                    w = word.lower()
                    if w not in CUSTOM_STOPWORDS:
                        dict_int_words[w] += 1   # count word occurrences
                        dict_str_words[w] = word # preserve case letters

    sorted_words = list(dict_int_words.keys())
    sorted_words.sort(key = lambda x: dict_int_words[x], reverse=True)

    top_words   = sorted_words[:max_words]
    count_range = dict_int_words[top_words[0]] - dict_int_words[top_words[-1]] + 1
    size_ratio  = 100.0 / count_range

    for word in top_words:
        size = int(dict_int_words[word] * size_ratio) + 15
        words.append({
            "text": dict_str_words[word],
            "size": size})

    path = dirname(realpath(__file__))
    layout = path+'/d3.layout.cloud.js'

    if isfile(layout):
        wordcloud_js = open(layout).read()
    else:
        wordcloud_js = urlopen(URL).read().decode('utf8')
        with open(layout, 'w') as f:
            f.write(wordcloud_js)

    output = """<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title></title>
    <script src="http://d3js.org/d3.v3.min.js"></script>
    </head>
    <body>
    <script>
        // embed Jason Davies' d3-cloud
        %s
        var fill = d3.scale.category20();
        var words = %s
        d3.layout.cloud().size([800, 800])
            .words(words)
            .rotate(function() { return ~~(Math.random() * 2) * 90; })
            .font("Impact")
            .fontSize(function(d) { return d.size; })
            .on("end", draw)
            .start();
        function draw(words) {
            d3.select("body").append("svg")
                    .attr("width", 1000)
                    .attr("height", 1000)
                .append("g")
                    .attr("transform", "translate(400,400)")
                .selectAll("text")
                    .data(words)
                .enter().append("text")
                    .style("font-size", function(d) { return d.size + "px"; })
                    .style("font-family", "Impact")
                    .style("fill", function(d, i) { return fill(i); })
                    .attr("text-anchor", "middle")
                    .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text; });
        }
    </script>
    </body>
    </html>
    """ % (wordcloud_js, json.dumps(words, indent=2))

    if output_name:
        with open(output_name, 'w') as f:
          f.write(output)

    return output

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument('input', action='store', help='input file name')
    parser.add_argument('-o', '--output', action='store', default='wordcloud.html', help='output file name')
    parser.add_argument('-w', '--max-words', action='store', type=int, help='maximum number of words (default: 100)', default=100)
    parser.add_argument('-x', '--exclude-words', action='store', help='list of words to ignore (comma separated)')

    args = parser.parse_args()

    wordcloud(args.input,
              args.output,
              args.max_words,
              args.exclude_words)
