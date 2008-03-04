#!/usr/bin/env python

import os
import sys
import commands

def coverage(cmd, show=False):
    status, output = commands.getstatusoutput('python-coverage %s ' % cmd)
    if status != 0:
        print >>sys.stderr, output
        sys.exit(-1)
    elif show:
        print output

def module_files():
    for dir, _, files in os.walk('DebianLive'):
        for filename in files:
            if filename.endswith('.py'):
                yield os.path.join(dir, filename)

def purge():
    try:
        os.unlink('.coverage')
    except OSError:
        pass

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    purge()
    coverage('-x %s' % 'tests/test_all.py')
    coverage(' -r -m %s' % " ".join([x for x in module_files()]), show=True)
    purge()
