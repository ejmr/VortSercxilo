#!/usr/bin/env python3

"""This script is the implementation of VortSerĉilo.  If there are no
errors the program exits with the system code zero.  But if something
goes wrong, e.g. download the dictionary, then Python itself will halt
due to uncaught exceptions.

"""

import argparse
import os.path
import re
import sys
import urllib.request

__version__ = "1.2.0-dev"

# These two global variables provide the URI to the 'ESPDIC.txt' file,
# i.e. the Esperanto-English dictionary, and the filename we want to
# use for our local copy of the dictionary.
DICTIONARY_URI = "http://www.denisowski.org/Esperanto/ESPDIC/espdic.txt"
DICTIONARY_FILENAME = os.path.dirname(os.path.realpath(sys.argv[0])) + "/ESPDIC.txt"

# This global tuple contains all of the 'match types' which the
# program recognizes.  These are the only acceptable values to the
# 'match' parameter of collect_matches() and to the '--match'
# command-line argument.
VALID_MATCH_TYPES = ("start", "end", "anywhere", "exact")

# This list contains all of the suffixes which the program considers
# 'official', in the sense that they appear in respected Esperanto
# dictionaries and grammars.  The suffixes never end with a vowel
# because we assume any vowel may follow them.  That is not
# necessarily grammatically correct, but it simplifies the code.
SUFFIXES = [
    "ad",  # The action or process of the root
    "an",  # Member or participant of the root
    "ant", # Present active participle
    "ar",  # Collection of the root
    "at",  # Present passive participle
    "aĉ",  # Disparaging or detestation of the root
    "aĵ",  # Manifestation of the root
    "ebl", # Possibility or suitability of the root
    "ec",  # Quality or characteristic of the root
    "eg",  # Augments the root
    "ej",  # Place characterized by the root
    "em",  # Inclination towards the root
    "end", # Requirement characterized by the root
    "er",  # Smallest tangible unit of the root
    "est", # Leader or person in charge of the root
    "et",  # Diminishes the root
    "id",  # Offspring of the root
    "ig",  # To cause the state described by the root
    "il",  # Tool or instrument defined by the root
    "in",  # Female version of the root
    "ind", # Worthy of the characteristic of the root
    "ing", # Holder for objects of the root
    "int", # Past active participle
    "ism", # System or doctrine defined by the root
    "ist", # Person who is a professional concerning the root
    "it",  # Past passive participle
    "iĝ",  # To become the state described by the root
    "nj",  # Friendly, personal female name
    "ont", # Future active participle
    "ot",  # Future passive participle
    "uj",  # Container of objects of the root
    "ul",  # Person characterized by the root
    "um",  # Idiomatically creates a new word from the root
    "ĉj",  # Friendly, personal male name
]



class InvalidMatchType(Exception):
    """Exception raised whenever we expect a 'match type' and receive
    something that is not in VALID_MATCH_TYPES.

    """
    pass

def download_dictionary():
    """Download a local copy of the Esperanto-English dictionary."""
    with urllib.request.urlopen(DICTIONARY_URI) as remote:
        with open(DICTIONARY_FILENAME, mode="w", encoding="utf-8") as local:
            local.write(remote.read().decode("utf-8"))

def collect_matches(word, match):
    """Accepts a word and a match type, both as strings, and returns a
    list of all entries which match that word.  The value of the match
    parameter must be a string that is in VALID_MATCH_TYPES or else
    the function will raise an InvalidMatchType exception.

    The return value will either be a list of strings, or an empty
    list if the function finds no matching dictionary entries.

    """
    if match not in VALID_MATCH_TYPES:
        raise InvalidMatchType(match)

    results = []
    
    with open(DICTIONARY_FILENAME, mode="r", encoding="utf-8") as espdic:
        # ESPDIC uses the format
        #
        #     Esperanto : English, English, English...
        #
        # for all entries.  We add a test for that colon to all
        # regular expressions so that they only match the Esperanto.
        # We also assign a search function so that we do not have to
        # write a similar but redundant if-elif block when reading
        # from ESPDIC.
        if match == "start":
            word_regex = re.compile(word + r"(?:\B.+)?\s+:", re.IGNORECASE)
            search_function = re.match
        elif match == "end":
            word_regex = re.compile(".+" + word + r"\b\s+:", re.IGNORECASE)
            search_function = re.search
        elif match == "anywhere":
            word_regex = re.compile(word + r"\s+:", re.IGNORECASE)
            search_function = re.search
        elif match == "exact":
            word_regex = re.compile("^" + word + "\s+:", re.IGNORECASE)
            search_function = re.search

        for entry in espdic.readlines():
            match = search_function(word_regex, entry)
            if match: results.append(match.string)

        return results



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("word", nargs="+", help="Esperanto word(s) to search for in the dictionary")
    parser.add_argument("--match", default="start", choices=VALID_MATCH_TYPES,
                        help="search for matches at the beginning, end, or anywhere in words")
    parser.add_argument("--roots-only", action="store_true",
                        help="search using only the roots of the words, removing affixes")
    parser.add_argument("--version", action="version", version="%(prog)s {0}".format(__version__))
    arguments = parser.parse_args()

    if os.path.exists(DICTIONARY_FILENAME) is False:
        download_dictionary()

    for word in arguments.word:
        for match in collect_matches(word, arguments.match):
            print(match, end="")
