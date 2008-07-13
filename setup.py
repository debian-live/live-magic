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

from distutils.core import setup

setup(
    name='live-magic',
    version='0.4',
    maintainer = "Chris Lamb",
    maintainer_email = "chris@chris-lamb.co.uk",
    description = "GTK+ frontend for configuring Debian Live systems",
    license = "GNU GPL v3",
    scripts = ['live-magic'],
    packages= [
        'LiveMagic',
        'LiveMagic.views',
        'LiveMagic.controllers',
        'DebianLive',
        'DebianLive.elements',
        'DebianLive.utils',
    ],
    data_files = [
        ('share/live-magic', [
            'misc/live-magic-builder',
            'misc/live-magic.glade',
            'misc/debian_openlogo-nd-100.png',
            'misc/debian_sm.png',
            'misc/gnome-logo-icon-transparent.png',
            'misc/kde.png',
            'misc/xfce.png',
            ]),
        ('share/applications', [
            'misc/live-magic.desktop'
        ]),
    ]
)
