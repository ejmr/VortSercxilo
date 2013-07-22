#!/usr/bin/env python3

import argparse
import os.path
import re
import sys
import urllib.request

__version__ = "0.3.0"

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
    parser.add_argument("--download-dictionary", help="download the latest dictionary", action="store_true")
    parser.add_argument("--version", action="version", version="%(prog)s {0}".format(__version__))
    arguments = parser.parse_args()

    if arguments.download_dictionary is True:
        download_dictionary()

    if os.path.exists(DICTIONARY_FILENAME) is False:
        download_dictionary()

    with open(DICTIONARY_FILENAME, mode="r", encoding="utf-8") as espdic:
        word = re.compile(arguments.word, re.IGNORECASE)
        for entry in espdic.readlines():
            match = re.match(word, entry)
            if match: print(match.string)
