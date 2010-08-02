# -*- coding: utf-8 -*-
#
#   live-magic - GUI frontend to create Debian LiveCDs, etc.
#   Copyright (C) 2007-2010 Chris Lamb <lamby@debian.org>
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
import gtk
import pwd

from LiveMagic.utils import find_resource

class MainController(object):

    def ready(self, options, args):
        self.options = options

        if options.build_for:
            self.do_show_build_window(lambda: gtk.main_quit())
        else:
            self.view.do_show_wizard()

    def on_quit_request(self, *args):
        return self._confirm_save(lambda: gtk.main_quit(), quit_dialog=True)

    def on_about_request(self, *args):
        self.view.do_show_about_dialog()

    def get_host_architecture(self):
        import commands
        status, output = commands.getstatusoutput('dpkg --print-architecture')
        assert status == 0
        return output

    def get_homedir(self):
        uid = os.geteuid()
        return pwd.getpwuid(uid)[5]

    def get_keyboard_layouts(self):
        for line in open(find_resource('keyboard-layouts.txt')):
            yield line.strip().split('\t', 2)

    def get_locales(self):
        locales = []
        try:
            for line in open('/usr/share/i18n/SUPPORTED'):
                locale, codepage = line.strip().split(' ', 2)
                locales.append(locale)
        except:
            locales = ['en_US.UTF-8']

        locales.sort()
        return locales
