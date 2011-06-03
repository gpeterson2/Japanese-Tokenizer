#! /usr/bin/env python3

import argparse
import codecs
import os
import sys

from tokenizer import tokenize

def get_word_count(words):
    ''' returns [(count, word)] '''

    unique_words = {}

    for word in words:
        try:
            unique_words[word] += 1
        except KeyError:
            unique_words[word] = 1

    # TODO - probably want to remove non-kanji single character results as
    # they aren't "words"
    key = lambda x: -x[1]
    for word, count in sorted(unique_words.items(), key=key):
        # TODO - empty words should have already been removed at this point,
        #  right?
        if word:
            yield (count, word)

def main():
    parser = argparse.ArgumentParser(description='Tokenize Japanese text.')
    parser.add_argument('-i', '--input', metavar='file', required=True,
         dest='input_path', help='An input file or directory')
    parser.add_argument('-o', '--output', metavar='file', required=False,
         dest='output_path',
         help='An output file. If not supplied will write to standard output.')
    parser.add_argument('-e', '--encoding', metavar='encoding',
         dest='encoding', required=False, help='The file encoding if not utf-8')
    parser.add_argument('-w', '--include-count', required=False,
         action='store_true', dest='include_count',
         help='Include the instance count of each word')
    parser.add_argument('-v', '--verbose', required=False,
         action='store_true', dest='verbose',
         help='Prints verbose output')

    args = parser.parse_args()

    # TODO - most of this code count be moved into functions, and then resused
    # if for example a GUI is added.

    # set encoding if applicable
    encoding = args.encoding

    if not args.encoding:
        encoding = 'utf-8'

    # grab file list
    path = args.input_path

    paths = []
    if os.path.isfile(path):
        paths.append(path)
    else:
        for path, dirs, files in os.walk(path):
            paths += [os.path.join(path, f) for f in files]

    # Read through the file(s)
    words = []
    verbose_output = args.verbose
    for path in paths:
        with codecs.open(path, 'r', encoding=encoding, errors='ignore') as f:
            if verbose_output:
                print(u'Reading file: {0}'.format(path))

            text = f.read()

            words += list(tokenize(text))

            if verbose_output:
                print(u'Finished file: {0}'.format(path))


    # Finally output the words
    include_count = args.include_count
    output_path = args.output_path

    if not output_path:
        # TODO - will fail miserably if console can't handle Unicode
        output = sys.stdout
    else:
        output = codecs.open(output_path, 'w', encoding='utf-8')

    # Grab count anyway, as it will remove duplicates
    for (count, word) in get_word_count(words):
        try:
            encoded = word.encode('utf-8')
            if include_count:
                output.write(u'{0}:\t{1}\n'.format(count, word))
            else:
                output.write(u'{0}\n'.format(word))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
