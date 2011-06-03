import unicodedata

# TODO - everything in here is very "functional" which does fit the overall
# goal of the code. Nothing would really benefit from being made into a class
# but perhaps that would improve the code?

__all__ = ['get_char_type', 'is_char_type_change', 'tokenize']

def get_char_type(char):
    ''' Returns KANJI, KANA, or NONE. '''

    # TODO - This seems too simple... It works, but relying on strings
    # in the unicode data seems wrong somehow.

    # TODO - This should not be using string constants

    if not char.strip():
        return 'NONE'

    try:
        char_name = unicodedata.name(char)
    except ValueError:
        print(u'Error finding code name: {0}'.format(char))
        return 'NONE'

    if 'CJK UNIFIED IDEOGRAPH' in char_name:
        return 'KANJI'

    # Originally wanted to differentiate between the two, but 
    #'KATAKANA-HIRAGANA PROLONGED SOUND MARK' counts as both
    # throwing it off.
 
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

    return last_type != current_type

def is_japanese(char):
    ''' Checks if the given character is Japanese.'''

    return get_char_type(char) != 'NONE'

def tokenize(text):
    ''' Split up Japanese text. '''

    # break up text
    last = ''
    words = []
    chars = []

    for i, char in enumerate(text):

        if not is_japanese(char):
            continue
        
        is_change = is_char_type_change(last, char)

        # make sure it's not the first
        if i > 0 and is_change:
            yield ''.join(chars)
            chars = [char]
        else:
            chars.append(char)

        last = char

    # get the last value
    yield ''.join(chars)

