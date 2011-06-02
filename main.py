#! /usr/bin/env python3

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

    for word, count in sorted(unique_words.items(), key= lambda x: -x[1]):
        # might want to remove single kana values, as they should just be word breaks...
        #if not remove_single_kana and len(word) > 1 or get_char_type(word) == 'KANJI':    

        # TODO really should eliminate things prior to this point
        if word:
            yield (count, word)

def main():
    # get the arg file name
    args = sys.argv

    # TODO - add an arg parser

    if len(args) == 1:
        print('Need to specify a file encoding')
        sys.exit(1)

    path = args[1]
    outpath = 'output.txt'

    encoding = ''
    if len(args) > 2:
        encoding = args[2]

    if not encoding:
        encoding = 'utf-8'

    # open file (as utf-8?)
    # the test file wasn't utf-8. It may just be how I saved it, but it didn't
    # work, so yeah, this needs some work.

    #encoding = 'UTF-8'
    #encoding = 'EUC-JP'

    paths = []
    if os.path.isfile(path):
        paths.append(path)

    else:
        for path, dirs, files in os.walk(path):
            paths += [os.path.join(path, f) for f in files]
        
    words = []
    for path in paths:
        with codecs.open(path, 'r', encoding=encoding, errors='ignore') as f:
            print(u'Reading file: {0}'.format(path))
            text = f.read()

            words += list(tokenize(text))
            print(u'Finished file: {0}'.format(path))

    output = codecs.open(outpath, 'w', encoding='utf-8')
    for (count, word) in get_word_count(words):
        try:
            encoded = word.encode('utf-8')
            output.write(u'{0}:\t{1}\n'.format(count, word))
            print(u'{0}:\t{1}'.format(count, word))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
