#!/usr/bin/env python3

# from http://code.activestate.com/recipes/66012/

import os
import sys

def start(pidfile, logfile, func):
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    if status(pidfile, logfile, func):
        print("Exit.")
        sys.exit(0)

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

    print("Starting server...", end="")
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

    # start the daemon main loop

    # Redirect standard file descriptors
    sys.stdin = open('/dev/null', 'r')
    sys.stdout = open('/dev/null', 'w')
    sys.stderr = open('/dev/null', 'w')
    func()
    return

def stop(pidfile, logfile, func):
    pid = status(pidfile, logfile, func)
    if pid:
        print("Stopping server...", end="")
        # this may be dengerous, i think process name must be ensured
        os.kill(pid, 15)
        print("done")
        os.remove(pidfile)
    return

def status(pidfile, logfile, func):
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
    stop(pidfile, logfile, func)
    return start(pidfile, logfile, func)

cmds = {"start" : start,
        "stop" : stop,
        "status" : status,
        "restart" : restart}

def daemon(cmd, pidfile, logfile, func):
    cmds[cmd](pidfile, logfile, func)
    return
