Dowwner
=======

Very simple wiki program.
Uses [Markdown](http://daringfireball.net/projects/markdown/) for markup and
pages are stored as plain markdown files.
Works both as a cgi program and as a server.


Dependencies
------------

* Python3 (Tested under python3.2)
* [Python Markdown](http://pythonhosted.org/Markdown/)


Installation
------------

Run:

    ./setup.py install

and command `dowwner` is installed. Or you can also just create simlink of
`bin/dowwner` and put it into your prefered directory like `$HOME/bin` or
`$HOME/.local/bin`. When you want to just try dowwner, running `bin/dowwner`
directly also works.


Basic Usage
-----------

### Use as Server

Run:

    $ dowwner

and access to `localhost:2505`.


### Use as CGI

Configure to run:

    $ dowwner --cgi


Commandline Options
-------------------

### `-h`, `--help`

Show help message.

### `-r|--root-dir <path>`

Change root directory. If omitted current directory is used.

### `-d|--daemon start|status|stop|restart`

Fork to background and make server run as daemon. When this option is used, only
one instance of dowwner can be run per root directory.

### `-p|--port <num>`

Wnen running dowwner as a server, this num is used for port. When omitted `2505`
is used by default.

### `-c`, `--cgi`

Run dowwner as a cgi program. When this option is used options `-d` and `-p` are
ignored.


TODOs
-----

* Stylesheet support
* Menu
* More usable access control for server mode (currently accesses only from
127.0.0.1 are allowed)
* Fix header if needed


License
-------

All code licensed under PSF License: <http://docs.python.org/2/license.html>
