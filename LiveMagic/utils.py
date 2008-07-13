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

def find_resource(resource):
    dirs = (
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'misc'),
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        '/usr/bin',
        '/usr/local/bin',
        '/usr/share/live-magic',
        '/usr/local/share/live-magic',
        '/usr/share/common-licenses',
    )

    tried = []
    for base in dirs:
        path = os.path.join(base, resource)
        if os.path.isfile(path):
            return path
        tried.append(path)

    raise ValueError, 'Cannot find %s resource. Tried: %s' % (resource, tried)
