#!/usr/bin/env python3

"""This script is the implementation of VortSerĉilo.  If there are no
errors the program exits with the system code zero.  But if something
goes wrong, e.g. downloading the dictionary, then Python itself will
halt due to uncaught exceptions.

The only third-party package we use is 'click', available here:

    http://click.pocoo.org/5/

"""

import click
import os.path
import re
import sys
import urllib.request

__version__ = "1.2.0"

# These two global variables provide the URI to the 'ESPDIC.txt' file,
# i.e. the Esperanto-English dictionary, and the filename we want to
# use for our local copy of the dictionary.
DICTIONARY_URI = "http://www.denisowski.org/Esperanto/ESPDIC/espdic.txt"
DICTIONARY_FILENAME = os.path.dirname(
    os.path.realpath(sys.argv[0])) + "/ESPDIC.txt"

# This global list contains all of the 'match types' which the
# program recognizes.  These are the only acceptable values to the
# 'match' parameter of collect_matches() and to the '--match'
# command-line argument.
VALID_MATCH_TYPES = ["start", "end", "anywhere", "exact"]

# This list contains all of the suffixes which the program considers
# 'official', in the sense that they appear in respected Esperanto
# dictionaries and grammars.  The suffixes never end with a vowel
# because we assume any vowel may follow them.  That is not
# necessarily grammatically correct, but it simplifies the code.
SUFFIXES = [
    "ad",   # The action or process of the root
    "an",   # Member or participant of the root
    "ant",  # Present active participle
    "ar",   # Collection of the root
    "as",   # Present tense
    "at",   # Present passive participle
    "aĉ",   # Disparaging or detestation of the root
    "aĵ",   # Manifestation of the root
    "ebl",  # Possibility or suitability of the root
    "ec",   # Quality or characteristic of the root
    "eg",   # Augments the root
    "ej",   # Place characterized by the root
    "em",   # Inclination towards the root
    "end",  # Requirement characterized by the root
    "er",   # Smallest tangible unit of the root
    "est",  # Leader or person in charge of the root
    "et",   # Diminishes the root
    "id",   # Offspring of the root
    "ig",   # To cause the state described by the root
    "il",   # Tool or instrument defined by the root
    "in",   # Female version of the root
    "ind",  # Worthy of the characteristic of the root
    "ing",  # Holder for objects of the root
    "int",  # Past active participle
    "is",   # Past tense
    "ism",  # System or doctrine defined by the root
    "ist",  # Person who is a professional concerning the root
    "it",   # Past passive participle
    "iĝ",   # To become the state described by the root
    "nj",   # Friendly, personal female name
    "ont",  # Future active participle
    "os",   # Future tense
    "ot",   # Future passive participle
    "u",    # Imperative
    "uj",   # Container of objects of the root
    "ul",   # Person characterized by the root
    "um",   # Idiomatically creates a new word from the root
    "us",   # Subjunctive
    "ĉj",   # Friendly, personal male name
]

# This list contains all of the prefixes that we consider 'official'
# under the same pretense as the SUFFIXES list.
PREFIXES = [
    "bo",   # Related through marriage
    "dis",  # Separation of the root object or action
    "ek",   # Start of the action defined by the root
    "eks",  # Former, cf. English 'ex-'
    "ge",   # Indicates both sexes of the root
    "mal",  # Creates the opposite meaning of the root
    "pra",  # Distant in time or relationship
    "re",   # To return or do again, cf. English 're-'
]

# This is the list of regular expressions we use to match affixes,
# compiled from the other lists of affixes so that we are not building
# the same regular expressions over and over.  See the function
# compile_affixes(), which populates this list.
AFFIXES = []


class InvalidMatchType(Exception):
    """Exception raised whenever we expect a 'match type' and receive
    something that is not in VALID_MATCH_TYPES.

    """
    pass


def compile_affixes():
    """Populate the global AFFIXES list with compiled regular expressions
    matching all prefixes and suffixes.

    """
    global AFFIXES

    AFFIXES.extend([re.compile("^({0})".format(prefix), re.IGNORECASE)
                    for prefix in PREFIXES])

    AFFIXES.extend([re.compile("({0}[aeiouŭj]{{0,2}})$".format(suffix), re.IGNORECASE)
                    for suffix in SUFFIXES])


def remove_affixes(word):
    """Accepts a word and removes all affixes, returning that version of
    the word.  The returned word will not end in any grammatically
    significant vowel under the assumption that we are removing all
    affixes in order to get the root word.

    """
    while True:
        matched_something = False

        for affix in AFFIXES:
            (new_word, matches) = re.subn(affix, "", word)

            if matches > 0:
                matched_something = True

            if len(new_word) == 0:
                return word
            else:
                word = new_word

        if matched_something == False:
            break

    # When the loop is finished purging all of the affixes the word
    # may still end in a vowel which we need to remove.
    return re.sub("[aioe]j?$", "", word)


def download_dictionary():
    """Download a local copy of the Esperanto-English dictionary."""
    print("Downloading the ESPDIC Esperanto-English dictionary...")
    with urllib.request.urlopen(DICTIONARY_URI) as remote:
        with open(DICTIONARY_FILENAME, mode="w", encoding="utf-8") as local:
            local.write(remote.read().decode("utf-8"))


def collect_entries(word, match):
    """Accepts a word and a match type, both as strings, and returns a
    list of all entries which match that word.  The value of the match
    parameter must be a string that is in VALID_MATCH_TYPES or else
    the function will raise an InvalidMatchType exception.

    The return value will either be a list of strings, or an empty
    list if the function finds no matching dictionary entries.

    """
    if match not in VALID_MATCH_TYPES:
        raise InvalidMatchType(match)

    entries = []

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
            if match:
                entries.append(match.string)

        return entries


@click.command()
@click.argument("words", nargs=-1)
@click.option("-m", "--match", type=click.Choice(VALID_MATCH_TYPES),
              default="start",
              help="Search entries at their start, end, anywhere, or exactly")
@click.option("-r", "--roots-only", is_flag=True,
              help="Remove all affixes and search only word roots")
@click.version_option(__version__, prog_name="VortSerĉilo",
              message="%(prog)s %(version)s")
def search(words, match, roots_only):
    """Search an Esperanto-English dictionary for given words.

    The first time you run VortSerĉilo it will download the dictionary
    file: "ESPDIC.txt" by Paul Denisowski.  If you ever want to update
    the dictionary, e.g. if there are new entries, then simply delete
    "ESPDIC.txt" and run VortSerĉilo again.

    """

    if os.path.exists(DICTIONARY_FILENAME) is False:
        download_dictionary()

    if roots_only:
        compile_affixes()
        words = [remove_affixes(word) for word in words]

    for word in words:
        for entry in collect_entries(word, match):
            print(entry, end="")


if __name__ == "__main__":
    search()
