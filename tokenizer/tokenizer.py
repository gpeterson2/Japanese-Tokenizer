import unicodedata

__all__ = ['get_char_type', 'is_char_type_change', 'is_japanese',
     'get_jp_text', 'tokenize']

def get_char_type(char):
    ''' Returns KANJI, KANA, or NONE. '''

    # TODO - this is a less than ideal way of dealing with character
    # types. For the most part it works, but I'm sure there are better
    # ways to do it.

    if not char.strip():
        return 'NONE'

    try:
        char_name = unicodedata.name(char)
    except ValueError:
        print(u'Error finding code name: {0}'.format(char))
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
    chars = []

    for i, char in enumerate(jp_chars):
        
        # TODO don't need the last and current type's anymore
        is_change, l, c = is_char_type_change(last, char)

        # make sure it's not the first
        if i > 0 and is_change:
            yield ''.join(chars)
            chars = [char]
        else:
            chars.append(char)

        last = char

    # get the last value
    yield ''.join(chars)

