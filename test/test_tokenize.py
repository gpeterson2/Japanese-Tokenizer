#!/usr/bin/python

import unittest

from tokenizer import tokenize

class TestTokenize(unittest.TestCase):
    def test_tokenize(self):
        # Ore no Imouto ga Konna ni Kawaii Wake ga Nai
        text = u'\u4ffa\u306e\u59b9\u304c\u3053\u3093\u306a\u306b\u53ef\u611b\u3044\u308f\u3051\u304c\u306a\u3044'
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

if __name__ == '__main__':
    unittest.main()
