#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   live-magic - GUI frontend to create Debian LiveCDs, etc.
#   Copyright (C) 2007-2008 Chris Lamb <chris@chris-lamb.co.uk>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
