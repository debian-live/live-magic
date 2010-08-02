# -*- coding: utf-8 -*-
#
#   live-magic - GUI frontend to create Debian LiveCDs, etc.
#   Copyright (C) 2007-2010 Chris Lamb <chris@chris-lamb.co.uk>
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

import re
import os

from DebianLive.utils import ListObserver

SHELL_ESCAPES = (
    (r'\ '[:-1], r'\\ '[:-1]),
    (r'"',  r'\"'),
    (r'`', r'\`'),
    (r'$', r'\$'),
    (r"'", r'\''),
)

REGEX = re.compile(r"""^\s*(\w+)=(?:(["\'])(([^\\\2]|\\.)*|)\2|((\w|\\["'])*))\s*(?:#.*)?$""")

class KeyVar(dict):
    '''
    Represents a POSIX shell KEY="VAR" configuration file.
    '''

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, dir, name, spec, filename=None):
        self.line_numbers = {}
        self.stale = set()

        if filename is None:
            self.filename = os.path.join(dir, 'config', name)
        else:
            self.filename = filename

        f = open(self.filename, 'r')
        try:
            line_no = 0
            for line in f:
                line_no += 1

                # Check and parse key=value lines
                match = REGEX.match(line)
                if not match:
                    continue

                key = match.groups()[0]

                # Find the correct match group
                for m in match.groups()[2:]:
                    if m is not None:
                        val = m
                        break

                # Unescape value
                for to, from_ in SHELL_ESCAPES:
                    val = val.replace(from_, to)

                # Save line number
                self.line_numbers[key] = line_no

                # Mutate to file type
                val_type = spec.get(key, str)
                typed_val = {
                    int: lambda k, v: {'': None}.get(v, None),
                    list: lambda k, v: ListObserver(v.split(), lambda: self.stale.add(k)),
                    str: lambda k, v: v,
                    bool: lambda k, v: {'true' : True, 'false' : False, \
                        'yes' : True, 'no' : False}.get(v, None),
                }[val_type](key, val)

                # Save value
                dict.__setitem__(self, key, typed_val)

        finally:
            f.close()

    def __setitem__(self, key, value):
        self.stale.add(key)
        if type(value) is list:
            value = ListObserver(value, lambda: self.stale.add(key))
        dict.__setitem__(self, key, value)

    def save(self):
        """
        Update all updated entries in the file.
        """
        if len(self.stale) == 0:
            return

        f = open(self.filename, 'r+')
        lines = f.readlines()

        for k in self.stale:
            val = self[k]

            # Escape value
            if type(val) in (list, ListObserver):
                for from_, to in SHELL_ESCAPES:
                    val = map(lambda x: x.replace(from_, to), val)
                val = map(str.strip, val)
            elif type(val) is str:
                for from_, to in SHELL_ESCAPES:
                    val = val.replace(from_, to)

            # Format value depending on its type
            line_value = {
                list : lambda v: " ".join(val),
                bool : lambda v: {True: 'true', False: 'false'}.get(val, None),
                str : lambda v: v,
                type(None) : lambda v: "",
            }[type(val)](val)

            line = '%s="%s"\n' % (k, line_value)

            try:
                # Overwrite original line in file
                lines[self.line_numbers[k] - 1] = line
            except KeyError:
                # Append line to end of file
                lines.append("\n# The following option was added by live-magic\n")
                lines.append(line)
        f.close()

        f = open(self.filename, 'w')
        f.writelines(lines)
        f.close()

        self.stale = set()
