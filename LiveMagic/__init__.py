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

import gtk
import pygtk
pygtk.require('2.0')

import optparse

from LiveMagic import views, controllers

__version__ = '0.4'

class LiveMagic(object):

    def __init__(self, args):
        try:
            gtk.init_check()
        except RuntimeError, e:
            sys.exit('E: %s. Exiting.' % e)

        parser = optparse.OptionParser(version=__version__)
        parser.add_option('--build-for', dest='build_for',
            metavar='owner:group', help="Perform build on behalf of owner:group. "
            "This option is used internally.")
        parser.add_option('--kde-full-session', dest='kde_full_session',
            metavar='', help="Value of KDE_FULL_SESSION. "
            "This option is used internally.")
        parser.add_option('--gnome-desktop-session-id', dest='gnome_desktop_session_id',
            metavar='', help="Value of GNOME_DESKTOP_SESSION_ID. "
            "This option is used internally.")
        options, args = parser.parse_args()

        c = controllers.Controller()
        v = views.View(c)

        c.ready(options, args)

        gtk.gdk.threads_init()
        gtk.main()
