#!/usr/bin/env python3

"""This script is the implementation of VortSerĉilo.  If there are no
errors the program exits with the system code zero.  But if something
goes wrong, e.g. download the dictionary, then Python itself will halt
due to uncaught exceptions.

"""

import argparse
import os.path
import re
import urllib.request

__version__ = "1.0.0"

# These two global variables provide the URI to the 'ESPDIC.txt' file,
# i.e. the Esperanto-English dictionary, and the filename we want to
# use for our local copy of the dictionary.
DICTIONARY_URI = "http://www.denisowski.org/Esperanto/ESPDIC/espdic.txt"
DICTIONARY_FILENAME = "ESPDIC.txt"



def download_dictionary():
    """Download a local copy of the Esperanto-English dictionary."""
    with urllib.request.urlopen(DICTIONARY_URI) as remote:
        with open(DICTIONARY_FILENAME, mode="w", encoding="utf-8") as local:
            local.write(remote.read().decode("utf-8"))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("word", help="Esperanto word to search for in the dictionary")
    parser.add_argument("--match", default="start",
                        choices=["start", "end", "anywhere"],
                        help="searchs for the word at the beginning, end, or anywhere in words")
    parser.add_argument("--version", action="version", version="%(prog)s {0}".format(__version__))
    arguments = parser.parse_args()

    if os.path.exists(DICTIONARY_FILENAME) is False:
        download_dictionary()

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
        if arguments.match == "start":
            word = re.compile(arguments.word + r"(?:\B.+)?\s+:", re.IGNORECASE)
            search_function = re.match
        elif arguments.match == "end":
            word = re.compile(".+" + arguments.word + r"\b\s+:", re.IGNORECASE)
            search_function = re.search
        elif arguments.match == "anywhere":
            word = re.compile(arguments.word + r"\s+:", re.IGNORECASE)
            search_function = re.search

        for entry in espdic.readlines():
            match = search_function(word, entry)
            if match: print(match.string, end="")
