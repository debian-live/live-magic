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
import re

from DebianLive.elements import KeyVar

__all__ = ['get_mirror']

COMMENTS = re.compile(r'\s*#')
PATTERNS = (
    re.compile(r'http://ftp.?\..{2}\.debian\.org[^\s]*'),
    re.compile(r'http://(localhost|127\.0\.0\.1)[^\s]*'),
    re.compile(r'http://[^\s]*'),
)
REJECT_PATTERNS = (
    re.compile(r'backports\.'),
    re.compile(r'security\.'),
)

def get_mirror(fallback='http://www.us.debian.org/', sources_list='/etc/apt/sources.list', defaults='/etc/default/live-helper'):
    result = fallback

    def filter_mirror(line):
        if COMMENTS.match(line):
            return False

        for pat in REJECT_PATTERNS:
            m = pat.search(line)
            if m:
                return False

        for pat in PATTERNS:
            m = pat.search(line)
            if m:
                return m.group(0)

        return False

    try:
        f = open(sources_list, 'r')
        try:
            for line in f.readlines():
                mirror = filter_mirror(line)
                if mirror:
                    result = mirror
                    break
        finally:
            f.close()
    except IOError:
        pass

    if defaults:
        try:
            kv = KeyVar('/etc/default', 'live-helper', {}, filename=defaults)
            kv_mirror = filter_mirror(kv['LH_MIRROR_BOOTSTRAP'])
            if kv_mirror:
                return kv_mirror
        except:
            pass

    return result
