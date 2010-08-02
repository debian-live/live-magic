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

import sys
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

import locale
import gettext
import optparse
import __builtin__

from LiveMagic import views, controllers
from LiveMagic.utils import find_resource

__version__ = '1.0'

def init_gettext():
    try:
        locale_dir = [find_resource('mo')]
    except ValueError:
        # Fall back to /usr/share/locale
        locale_dir = []

    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        pass

    for module in gettext, gtk.glade:
        module.bindtextdomain('live-magic', *locale_dir)
        module.textdomain('live-magic')

    __builtin__._ = gettext.gettext

class LiveMagic(object):

    def __init__(self, args):
        init_gettext()

        try:
            gtk.init_check()
        except RuntimeError, e:
            sys.exit('E: %s. Exiting.' % e)

        parser = optparse.OptionParser(version=__version__)
        parser.add_option('--build-for', dest='build_for',
            metavar='owner:group', help="Perform build on behalf of owner:group. "
            "This option is used internally.")
        options, args = parser.parse_args()

        c = controllers.Controller()
        v = views.View(c)

        c.ready(options, args)

        gtk.gdk.threads_init()
        gtk.main()
