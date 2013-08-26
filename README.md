VortSerĉilo
===========

VortSerĉilo is an [Esperanto][]-to-English dictionary program.  Its
name literally means ‘word-searching tool’.  The program uses Paul
Denisowski’s [ESPDIC][] as its dictionary file.  VortSerĉilo will
automatically download this dictionary for you.


Usage
-----

```sh
$ ./vortsercxilo.py dormi
dormi : to be asleep, sleep
dormi la tutan nokton : to sleep all night long
dormi sur : to sleep on
dormi surkrure : to sleep standing up
dormiga : soporific, sleep-inducing
dormigi : to put to sleep
dormigilo : soporific
dormilo : sleeping device
dorminklina : drowsy, sleepy
dormiranto : sleep-walker
```

You may provide multiple words to search for.  Using the `--help`
option will show the available command-line options.  The most useful
is `--match`, which accepts one of three values:

1. `start`: Search for the given input only at the start of words and
   phrases.  *This is the default behavior.*

2. `end`: Search for the given input only at the end of words and
   phrases.

3. `anywhere`: Search for the given input anywhere it appears in words
   and phrases.

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
* [Books at Project Gutenberg](http://www.gutenberg.org/wiki/Esperanto_%28Bookshelf%29 "Esperanto Bookshelf") 


Licenses
--------

### ESPDIC ###

[Creative Commons Attribution 3.0 Unported License][cc]

Copyright Paul Denisowski

### Code ###

[GNU General Public License][gpl]

Copyright 2013 Eric James Michael Ritz


Miscellaneous
-------------

VortSerĉilo follows [Semantic Versioning 2.0.0][semver].



[gpl]: http://www.gnu.org/copyleft/gpl.html
[Python]: http://python.org/
[Esperanto]: http://www.uea.org/
[ESPDIC]: http://www.denisowski.org/Esperanto/ESPDIC/espdic_readme.htm
[cc]: http://creativecommons.org/licenses/by/3.0/
[semver]: http://semver.org/spec/v2.0.0.html
