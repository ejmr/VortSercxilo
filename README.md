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


Requirements
------------

* [Python 3.3.1][] or later.

This is the version of Python used to develop the program.  It may
function with older versions.  However, VortSerĉilo does not support
Python 2 at all.


Installation
------------

To install VortSerĉilo you can either clone [the repository][./] or
simply download the [Python script][./vortsercxilo.py].  The first
time you run the program it will download the Esperanto-English
dictionary in the same directory as the program.


Licenses
--------

### ESPDIC ###

[Creative Commons Attribution 3.0 Unported License][cc]

Copyright Paul Denisowski

### Code ###

[GNU General Public License][gpl]

Copyright 2013 Eric James Michael Ritz



[gpl]: http://www.gnu.org/copyleft/gpl.html
[Python 3]: http://python.org/
[Esperanto]: http://www.uea.org/
[ESPDIC]: http://www.denisowski.org/Esperanto/ESPDIC/espdic_readme.htm
[cc]: http://creativecommons.org/licenses/by/3.0/
