#! /usr/bin/env python3

import sys
import unicodedata

# Probably not the best way to go about this...
def get_char_type(char):
    ''' Returns KANJI, KANA, or NONE. '''

    if not char.strip():
        return 'NONE'

    try:
        char_name = unicodedata.name(char)
    except ValueError:
        print('Error finding code name: {0}'.format(char))
        return 'NONE'

    if 'CJK UNIFIED IDEOGRAPH' in char_name:
        return 'KANJI'
    # Can't use individuals because there's at least one with
    # HIRAGANA-KATAKANA in it...
    #elif 'KATAKANA' in char_name:
        #return 'KATAKANA'
    #elif 'HIRAGANA' in char_name:
        #return 'HIRAGANA'
    elif 'KATAKANA' in char_name or 'HIRAGANA' in char_name:
        return 'KANA'
    else:
        return 'NONE'

def is_char_type_change(last, current):
    ''' Returns (is_change, last type, current type) '''

    last_type = get_char_type(last)
    current_type = get_char_type(current)

    return (last_type != current_type, last_type, current_type)

def is_japanese(char):
    ''' If the character is japanese. '''

    return get_char_type(char) != 'NONE'
    
def get_jp_text(text):
    ''' Return a list of characters with non-japanese text replaced as empty strings. '''

    # Get rid of non-Japanese text...for now anyway
    # Should keep in newlines/non-japanese breaks...

    # TODO - is there a way to merge multiple instances of empty strings as 
    # a single blank? Better to do it here than pass around a bunch of them.

    for char in text:
        yield char if is_japanese(char) else ''

def tokenize(text):
    ''' Split up Japanese text. '''

    # Eliminate non-japanese text
    jp_chars = get_jp_text(text)
    
    # break up text
    last = ''
    words = []
    word = []

    for i, char in enumerate(jp_chars):
        
        # TODO don't need the last and current type's anymore
        is_change, l, c = is_char_type_change(last, char)

        # make sure it's not the first
        if i > 0 and is_change:
            yield ''.join(word)
            word = [char]
        else:
            word.append(char)

        last = char

    # get the last value
    yield ''.join(word)

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

    if len(args) == 1:
        print('Need to specify a file')
        sys.exit(1)

    filename = args[1]

    # open file (as utf-8?)
    # the test file wasn't utf-8. It may just be how I saved it, but it didn't
    # work, so yeah, this needs some work.

    encoding = 'UTF-8'
    #encoding = 'EUC-JP'
    with open(filename, 'r', encoding=encoding) as f:
        text = f.read()

        words = list(tokenize(text))

    for (count, word) in get_word_count(words):
        print('{0}:\t{1}'.format(count, word))

if __name__ == '__main__':
    main()
