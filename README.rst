=================
Japanes Tokenizer
=================

An incredibly annoying aspect of learning a new language is having to stop
and look up unknown words every few minutes. I started this project so that
I could extract the words from Japanese text, make flashcards out of them,
and then later return to the original text at that point being able to
reasonably understand it.
The ulimate goal is to have this program extract words, normalize verb
congugations, and provide translations.

Currently it only extracts words.

In English this would be a rather simple prospect: read in the file(s), split
on whitespace or punctuation characters and call it a day. Japanese does
not differentiation words using whitespace, making this a bit more challenging.

As a quick explanation:

Modern Japanese is composed of three different alphabets:

- Hiragana - an alphabet of about 50 letters used to represent sounds, to
  conjugate verbs, and cover anything that kanji does not cover.
- Katakana - an alphabet mirroring the hiragana alphabet, it is primary used for
  foreign loan words.
- Kanji - Over 2,000 ideographs representing objects, ideas, etc.

Generally a sentence will contain Kanji for nouns, verbs, and adjectives, with
Hiragana used for conjugation purposes or to provide markers for sentence
sections.

The way most Japanese programs handle this problem is compare a given section
of text to a weighted list of words, often with grammatical analysis.

Until that can be implemented this project will use a simpler method of
analyzing the text of a sentence looking for alphabet changes. In general
this should isolate nouns, verbs, adjectives, etc. and will fail to break
up compound words as well as fail to recognize verb conjugations.

-----
Usage
-----

usage: main.py [-h] -i file [-o file] [-e encoding] [-w] [-v]

