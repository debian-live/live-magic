#!/usr/bin/env python
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

import os
import re

from distutils.core import setup
from distutils.file_util import copy_file
from distutils.command.build_py import build_py
from distutils.command.install_data import install_data

from glob import glob
from subprocess import check_call

class my_install(install_data):
    def run(self):
        # Generating and installing .mo files
        check_call('po/update-mo.sh')
        for langdir in glob('mo/*'):
            lang = os.path.basename(langdir)
            src = os.path.join(langdir, 'LC_MESSAGES', 'live-magic.mo')
            dst = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
            self.data_files.append((dst, [src]))

        try:
            credits = file('misc/translator-credits.txt', 'w')
            for po in glob('po/*.po'):
                f = file(po)
                try:
                    lang = os.path.basename(po).split('.')[0]
                    for line in f:
                        m = re.match(r'"Last-Translator: ([^\\]*)', line)
                        if m:
                            print >>credits, m.group(1), '(%s)' % lang
                            break
                finally:
                    f.close()
        finally:
            credits.close()

        install_data.run(self)

setup(
    name='live-magic',
    version='1.0',
    maintainer = "Chris Lamb",
    maintainer_email = "chris@chris-lamb.co.uk",
    description = "GTK+ frontend for configuring Debian Live systems",
    license = "GNU GPL v3",
    scripts = ['live-magic'],
    cmdclass = {
        'install_data': my_install,
    },
    packages = [
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
            'misc/keyboard-layouts.txt',
            'misc/translator-credits.txt',
            ]),
        ('share/applications', [
            'misc/live-magic.desktop'
        ]),
    ]
)
