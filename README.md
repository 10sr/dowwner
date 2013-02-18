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

Usage
-----

Run:

    $ bin/dowwner

and access to `localhost:2505`.

TODO:
-----

* Confirm when deleting pages
* Manage history (view, revert, diff, ...)
* More valuable access control (currently accesses only from 127.0.0.1 are
allowed)
