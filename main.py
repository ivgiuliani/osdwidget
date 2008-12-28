#!/usr/bin/env python
import sys, os
from optparse import OptionParser
from handler import handle

def main():
    parser = OptionParser()
    parser.add_option("-d", "--daemon", dest="daemonize", action="store_true", \
            help="Run this program in background", default=False)
    (options, args) = parser.parse_args()

    try:
        run(options.daemonize)
    except KeyboardInterrupt:
        pass

    return 0

def run(daemon=False):
    if daemon:
        try:
            if os.fork() > 0:
                # parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: (%d) %sn" % (e.errno, e.strerror))
            sys.exit(1)

        # children process
        # setup a safe environment and start a new process in that
        os.chdir("/")
        os.umask(0)
        os.setsid()

        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: (%d) %sn" % (e.errno, e.strerror))
            sys.exit(1)

        # now we're daemonized
        for f in sys.stdout, sys.stderr: f.flush()

    handle()

if __name__ == '__main__':
    sys.exit(main())
