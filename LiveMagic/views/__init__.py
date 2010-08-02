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

from build import BuildView as Build
from main import MainView as Main
from wizard import WizardView as Wizard

from LiveMagic.utils import find_resource

import gtk.glade

class View(Main, Build, Wizard):
    def __init__(self, controller):
        self.controller = controller

        self.xml = gtk.glade.XML(find_resource('live-magic.glade'))
        self.xml.signal_autoconnect(self.controller)

        Main.__init__(self)
        Build.__init__(self)
        Wizard.__init__(self)
