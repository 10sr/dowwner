#!/usr/bin/env python3

# from http://code.activestate.com/recipes/66012/

import os
import sys
import signal

def start(pidfile, logfile, func):
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    if status(pidfile):
        print("Exit.")
        sys.exit(0)

    print("Starting server...", end="")
    sys.stdout.flush()

    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError as e:
        print("fork #1 failed: {} ({})".format(e.errno, e.strerror),
              file=sys.stderr)
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/")   #don't prevent unmounting....
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            #print "Daemon PID %d" % pid
            with open(pidfile, mode='w') as f:
                f.write("{}".format(pid))
            print("done")
            sys.exit(0)
    except OSError as e:
        print("fork #2 failed: {} ({})".format(e.errno, e.strerror),
              file=sys.stderr)
        sys.exit(1)

    def _term_hndlr(signum, frame):
        os.remove(pidfile)
        return

    # start the daemon main loop

    sys.stdout.flush()
    sys.stderr.flush()
    sys.stdin = open(os.devnull, 'r')
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    signal.signal(signal.SIGTERM, _term_hndlr)
    func()
    return

def stop(pidfile):
    pid = status(pidfile)
    if pid:
        print("Stopping server...", end="")
        # this may be dengerous, i think process name must be ensured
        os.kill(pid, signal.SIGTERM)
        print("done")
        # os.remove(pidfile) # done by _term_hndlr() in start()
    return

def status(pidfile):
    """
    Returns:
        pidnum if server running, otherwise 0."""
    try:
        with open(pidfile) as f:
            pid = int(f.read())
    except IOError as e:
        if e.errno == 2:
            print("Server not running on this dir.")
            return 0
        else:
            raise

    try:
        os.getsid(pid)
    except OSError as e:
        if e.errno == 3:        # not such process
            print("Server not running on this dir.")
            return 0
        else:
            raise

    print("Server running on this dir.")
    return pid

def restart(pidfile, logfile, func):
    stop(pidfile)
    return start(pidfile, logfile, func)
