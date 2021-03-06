VortSerĉilo
===========

VortSerĉilo is an [Esperanto][]-to-English dictionary program.  Its
name literally means ‘word-searching tool’.  The program uses Paul
Denisowski’s [ESPDIC][] as its dictionary file.  VortSerĉilo will
automatically download this dictionary for you, which is the program’s
most useful property: you can use it without an Internet connection.
There are online Esperanto-English dictionary sites that are better
than VortSerĉilo; but I do not always have an Internet connection and
so it was vital to me that VortSerĉilo worked without one.  The
program only needs to connect to the Internet the first time it runs
so that it may grab a copy of the dictionary to use in the future.

A side-effect of this design is that you can force VortSerĉilo to
fetch the latest copy of the ESPDIC by simply deleting the
`ESPDIC.txt` file from the program’s directory.


Usage
-----

```sh
$ ./vortsercxilo.py fakto
fakto : fact
faktoreca : factorial
faktorgrupo : factor group, quotient group
faktorialo : factorial
faktorio : (trading) agency
faktoro : agent, factor, steward
faktoro de eventualo : contingency factor

$ ./vortsercxilo.py --match=exact kriegi fajfi kanti
kriegi : to bawl, roar, scream, shout, shriek, yell
fajfi : to whistle
kanti : to sing
```

You may provide multiple words to search for.  Using the `--help`
option will show the available command-line options.  The most useful
is `--match`, which accepts the following values:

1. `start`: Search for the given input only at the start of words and
   phrases.  *This is the default behavior.*

2. `end`: Search for the given input only at the end of words and
   phrases.

3. `anywhere`: Search for the given input anywhere it appears in words
   and phrases.

4. `exact`: Search for the given input exactly as provided.  This is
   the strictest form of searching.

If you use the option `--roots-only` then VortSerĉilo will remove all
affixes from each word and search the dictionary for the remaining
root words.  For example:

```sh
$ ./vortsercxilo.py --roots-only verkilo
verkado : work, opus
verkaĵo : writing
verkanto : author, creator
verkanto de retotaglibroj : blogger
verkaro : works (collected)
verketo : small work, small creation
verki : to compose, create, write
verkilo : authoring tool, word processor
verkinto : (completed) work; author
verkista : of an artist
verkistino : authoress
verkisto : author, writer, composer
verkita : authored, written, composed, created
verko : work (literary or artistic)
verkoŝtelisto : plagiarist
```

In other words, the results are the same as if you searched for simply
‘verk’ instead of ‘verkilo’.  Using the `--roots-only` option will not
break down compound words such as ‘birdkanto’.  VortSerĉilo only
attempts to remove affixes listed in authoritative sources, even
though most affixes are independent words themselves.


Graphical User Interface
------------------------

Version 2.0.0 will have a graphical user interface for users who do
not want to use the command-line.


Requirements
------------

* [Python 3.3.1][Python] or later.

This is the version of Python used to develop the program.  It may
function with older versions.  However, VortSerĉilo does not support
Python 2 at all.


Installation
------------

To install VortSerĉilo you can either clone [the repository](./) or
simply download the [Python script](./vortsercxilo.py).  The first
time you run the program it will download the Esperanto-English
dictionary in the same directory as the program.


Esperanto Resources
-------------------

* [Universala Esperanto-Asocio](http://www.uea.org/ "The UAE")
* [Lernu](http://en.lernu.net/ "Learn Esperanto")
* [Esperanto.net](http://esperanto.net/ "Esperanto.net")
* [Esperanto Chat](http://babilejo.org/ "Chat in Esperanto")
* [Esperanto 101 at Reddit](http://www.reddit.com/r/Esperanto101 "Esperanto 101")
* [English-Esperanto Courses at Memrise](http://www.memrise.com/courses/english/?q=esperanto "English Esperanto Courses")
* [Books at Project Gutenberg](http://www.gutenberg.org/wiki/Esperanto_%28Bookshelf%29 "Esperanto Bookshelf") 


Licenses
--------

### ESPDIC ###

[Creative Commons Attribution 3.0 Unported License][cc]

Copyright Paul Denisowski

### VortSerĉilo ###

[GNU General Public License][gpl]

Copyright 2013–2014 Eric James Michael Ritz


Miscellaneous
-------------

VortSerĉilo follows [Semantic Versioning 2.0.0][semver].



[gpl]: http://www.gnu.org/copyleft/gpl.html
[Python]: http://python.org/
[Esperanto]: http://www.uea.org/
[ESPDIC]: http://www.denisowski.org/Esperanto/ESPDIC/espdic_readme.htm
[cc]: http://creativecommons.org/licenses/by/3.0/
[semver]: http://semver.org/spec/v2.0.0.html
