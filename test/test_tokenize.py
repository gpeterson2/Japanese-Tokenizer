#!/usr/bin/python

import unittest

from tokenizer import *

class TestTokenize(unittest.TestCase):
    def test_tokenize(self):
        # Ore no Imouto ga Konna ni Kawaii Wake ga Nai
        text = (u'\u4ffa\u306e\u59b9\u304c\u3053\u3093\u306a\u306b\u53ef'
            u'\u611b\u3044\u308f\u3051\u304c\u306a\u3044')

        # Note that Wake ga nai should  be split up as well
        # Hopefully in a later version.

        expected = [
            u'\u4ffa',
            u'\u306e',
            u'\u59b9',
            u'\u304c\u3053\u3093\u306a\u306b',
            u'\u53ef\u611b',
            u'\u3044\u308f\u3051\u304c\u306a\u3044',
        ]

        result = list(tokenize(text))

        self.assertEqual(expected, result)

    # Hardly exhaustive
    def test_is_japanese_false(self):
        self.assertFalse(is_japanese(u'q'))

    def test_is_japanese_true(self):
        self.assertTrue(is_japanese(u'\u4ffa'))

    def test_get_char_type_kanji(self):
        text = u'\u4ffa'
        expected = 'KANJI'

        result = get_char_type(text)

        self.assertEqual(expected, result)

    def test_get_char_type_kana(self):
        text = u'\u306e'
        expected = 'KANA'

        result = get_char_type(text)

        self.assertEqual(expected, result)

    def test_get_char_type_none(self):
        text = u'q'
        expected = 'NONE'

        result = get_char_type(text)

        self.assertEqual(expected, result)

    def test_get_char_type_hiragana_katakana_prolonged_sound_mark(self):
        ''' Can be either hiragana or katakana. 

            Which make more sense when I was differentiating the two.
        '''

        text = u'\u30fc'
        expected = 'KANA'

        result = get_char_type(text)

        self.assertEqual(expected, result)

    def test_is_char_type_change_true(self):
        last = u'\u30fc'
        current = u'q'

        self.assertTrue(is_char_type_change(last, current))  

    def test_is_char_type_change_false(self):
        last = u'\u30fc'
        current = u'\u30fc'

        self.assertFalse(is_char_type_change(last, current))  

if __name__ == '__main__':
    unittest.main()
