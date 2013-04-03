Dowwner
=======

Very simple wiki clone.
Uses Markdown for markup and pages are stored as plain markdown files.
Works both as a cgi program and as a server.

Dowwner is developed at <https://github.com/10sr/dowwner>.


Dependencies
------------

* Python3 (Tested under python3.2)
* [Python Markdown](http://pythonhosted.org/Markdown/)


Installation
------------

Run:

    ./setup.py install

and command `dowwner` is installed. Or you can just create simlink of
`bin/dowwner` and put it into your prefered directory like `$HOME/bin` or
`$HOME/.local/bin`. When you just want a try, running `bin/dowwner`
directly also works.


Quick Start
-----------

Run:

    $ dowwner

and access to `localhost:2505`.


Wiki Usage
----------

### Syntax

[Markdown](http://daringfireball.net/projects/markdown/) is used for wiki
syntax with one extension: wiki link.
This extension converts `[[newpage]]` into `<a href="newpage">newpage</a>`.
It works with spaces and/or slashes so you can use links like `[[dir/page]]`.

### Creating and Removing Pages

There is no special step for creating new pages. When you access pages that do
not exist yet, edit pages appear and you can write newly. That all.

To remove pages, access edit pages and submit empty contents.

### Page Name

You cannot create directories or pages that start with `.`. These names are all
reserved for special porpose. For example, if a page name is prefixed by
`.edit.`, dowwner shows the edit page. Additionally, all pages with suffix
`.css` are treated as stylesheet files, and you cannot create directories with
suffix `.css`.

### Page Hierarchy

Wiki pages are not flat. When creating pages like `dir/page`, directory named
`dir` is created automatically and `page` is placed under `dir`, and directories
are hidden when no pages exist in that directories.

### Index Page

If the page named `index` exists in a directory, dowwner use that when only the
directory name is specified.
Otherwise, dowwner shows the list of pages in the directory. This list can be
accessed explicitly with `.list`.

### Page History

When modifying or removing pages, old contents are backed up. It is possible to
revert to these backups.

### StyleSheet

You can create and edit `style.css` from `.list` page. Additionally, you can
create `common.css` in the root directory. `common.css` is same for all
directories, whereas `style.css`s are different for each directory. You cannot
create or edit `common.css` from the web interface.


Commandline Options
-------------------

Without `-d` or `-c` option, dowwner run in "server" mode and you can
terminate dowwner with `C-c`. With `-d start` option, dowwner run in "daemon"
mode. With `-c` option, dowwner run in "cgi" mode.

### `-h`, `--help`

Show help message.

### `-r|--root-dir <path>`

Change root directory. If omitted current directory is used.

### `-d|--daemon start|status|stop|restart`

Fork to background and make server run as daemon when `-d start` is given.
This means that dowwner does not stick to your tty and you can safely exit after
starting dowwner program.
When this option is used, only one instance of dowwner can be run per root
directory.

### `-p|--port <num>`

Wnen running dowwner as a server, this num is used for port. When omitted `2505`
is used by default.

### `-c`, `--cgi`

Run dowwner as a cgi program. When this option is used, options `-d` and `-p`
are ignored. Normally using `tools/cgi.py` is more recommended (see below).


Run as CGI
----------

Copy `tools/cgi.py` to where you want to access as a cgi,
modify the file so that `rootdir` points to your wiki directory, and configure
http server to run the file as a cgi. You can set auth for `POST` method to make
wiki read-only for anonymous access.


TODOs
-----

* Search support
* Menu
* More usable access control for server mode (currently accesses only from
127.0.0.1 are allowed)
* Fix http headers if needed
* Handle errors properly and return correct http status
* Use logger when -d option used


License
-------

All code licensed under PSF License: <http://docs.python.org/3/license.html>
