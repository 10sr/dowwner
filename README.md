Dowwner
=======

Very simple wiki program.
Uses [Markdown](http://daringfireball.net/projects/markdown/) for markup.
Works both as a cgi program and as a server.


Features
--------

* Works with and without external http server
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


Use as Server
-------------

Run:

    $ bin/dowwner

and access to `localhost:2505`. `bin/dowwner -h` for additional help.


Use as CGI
----------

Configure to run:

    $ bin/dowwner --cgi


TODO:
-----

* Stylesheet support
* Menu
* More usable access control (currently accesses only from 127.0.0.1 are
allowed)
* Fix header if needed


License
-------

All code licensed under PSF License: <http://docs.python.org/2/license.html>
