Dowwner
=======

Very simple wiki program.
Uses [Markdown](http://daringfireball.net/projects/markdown/) for markup.


Feature
-------

* Works without external http server
* Files are stored as plain markdown files


Dependencies
------------

* Python3 (Tested under python3.2)
* [Python Markdown](http://pythonhosted.org/Markdown/)


Installation
------------

Run:

    ./setup.py install

or just create simlink of bin/dowwner and put it into your prefered directory
like "$HOME/bin" or "$HOME/.local/bin".


Usage
-----

Run:

    $ bin/dowwner

and access to `localhost:2505`. `bin/dowwner -h` for additional help.


TODO:
-----

* Stylesheet support
* Menu
* Works as cgi
* More usable access control (currently accesses only from 127.0.0.1 are
allowed)
* Use cache (both http cache and local cache)


License
-------

All code licensed under PSF License: <http://docs.python.org/2/license.html>
