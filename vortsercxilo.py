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



def download_dictionary():
    """Download a local copy of the Esperanto-English dictionary."""
    with urllib.request.urlopen(DICTIONARY_URI) as remote:
        with open(DICTIONARY_FILENAME, mode="w", encoding="utf-8") as local:
            local.write(remote.read().decode("utf-8"))

def collect_matches(word, match):
    """Accepts a word and a match type, both as strings, and returns a
    list of all entries which match that word.  The value of the match
    parameter must be a string that is an acceptable value to
    '--match' command-line argument.

    The return value will either be a list of strings, or an empty
    list if the function finds no matching dictionary entries.

    """
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
    parser.add_argument("--match", default="start",
                        choices=["start", "end", "anywhere", "exact"],
                        help="searchs for the word at the beginning, end, or anywhere in words")
    parser.add_argument("--version", action="version", version="%(prog)s {0}".format(__version__))
    arguments = parser.parse_args()

    if os.path.exists(DICTIONARY_FILENAME) is False:
        download_dictionary()

    for word in arguments.word:
        for match in collect_matches(word, arguments.match):
            print(match, end="")
