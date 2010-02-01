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

from DebianLive import utils

import os
import commands

class Config(object):
    def __init__(self, dir, spec=None, **kwargs):
        self.dir = dir

        if spec is None:
            # Load default field specification
            from spec import spec

        from spec import constructor_args
        for option in kwargs:
            option = option.replace('_', '-')
            if option not in constructor_args:
                raise TypeError, 'Unexpected keyword argument "%s"' % option

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        options = ["--%s='%s'" % (k.replace('_', '-'), v)
            for k, v in kwargs.iteritems()]
        cmd = 'cd "%s"; lh config --ignore-system-defaults %s' % (os.path.abspath(self.dir),
            ' '.join(options))

        result, out = commands.getstatusoutput(cmd)
        if result != 0:
            raise IOError, out

        self.children = {}
        for name, details in spec.iteritems():
            elem_type = details[0]
            elem = elem_type(self.dir, name, *details[1:])
            self.children[name] = elem
            setattr(self, name, elem)

    def __str__(self):
        from pprint import pformat
        return '<DebianLive.Config dir="%s" %s>' % (self.dir, pformat(self.children))

    def __repr__(self):
        return self.__str__()

    def save(self):
        for elem in self.children.values():
            elem.save()
