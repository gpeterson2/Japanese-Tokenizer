import unicodedata

# TODO - everything in here is very "functional" which fits the overall
# goal of the code perfectly fine. Currently the code wouldn't necessarily
# benefit from moving it into classes, but doing so would at least make it
# easier to provide alternate functionality through subclassing.

__all__ = ['get_char_type', 'is_char_type_change', 'tokenize']

def get_char_type(char):
    ''' Returns KANJI, HIRAGANA, KATAKA, BOTH or NONE. 
        
        NONE is somehwat misnamed for representing non-Japanese
        characters.

        BOTH appears (so far) one instance for the "prolonged sound mark"
        which can be used with both hiragana and katakana.
    '''

    # TODO - This seems too simple... It works, but relying on strings
    # in the unicode data seems wrong somehow.

    # TODO - This should not be using string constants

    # TODO - there are probably better ways of dealing with the "both"
    # character, although likely not here.

    if not char.strip():
        return 'NONE'

    try:
        char_name = unicodedata.name(char)
    except ValueError:
        print(u'Error finding code name: {0}'.format(char))
        return 'NONE'

    if 'CJK UNIFIED IDEOGRAPH' in char_name:
        return 'KANJI'

    #'KATAKANA-HIRAGANA PROLONGED SOUND MARK' counts as both
    # throwing off the otherwise fairly simple proces. Although
    # it makes sense as this character is included inside words,
    # and wouldn't make sense to split on.

    elif char_name == 'KATAKANA-HIRAGANA PROLONGED SOUND MARK':
        return 'BOTH' 
    elif 'KATAKANA' in char_name:
        return 'KATAKANA'
    elif 'HIRAGANA' in char_name:
        return 'HIRAGANA'
    else:
        return 'NONE'

def is_char_type_change(last, current):
    ''' Returns (is_change, last type, current type) '''

    last_type = get_char_type(last)
    current_type = get_char_type(current)

    if (
        (last_type == 'BOTH' and current_type in ['HIRAGANA', 'KATAKANA']) or
        (last_type in ['HIRAGANA', 'KATAKANA'] and current_type == 'BOTH')
    ):
        return False
        

    return last_type != current_type

def is_japanese(char):
    ''' Checks if the given character is Japanese.'''

    return get_char_type(char) != 'NONE'

def tokenize(text):
    ''' Split Japanese text. '''

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

