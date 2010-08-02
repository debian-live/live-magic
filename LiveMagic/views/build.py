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

import vte
import gobject

class BuildView(object):
    def __init__(self):
        # Init custom widgets
        self.vte_terminal = None

    def do_show_window_build(self, build_close_callback):
        self.build_close_callback = build_close_callback

        # Configure VteTerminal component if necessary
        if self.vte_terminal is None:
            t = vte.Terminal()
            t.set_font_from_string('Monospace 8')
            self['vte_scrollbar'].set_adjustment(t.get_adjustment())
            self['hbox_vte'].pack_end(t)
            self['hbox_vte'].show_all()
            t.connect('child-exited', self.controller.on_vte_child_exited)
            self.vte_terminal = t

        self.vte_terminal.reset(True, True)
        self['window_build'].show()

    def do_hide_window_build(self):
        self['window_build'].hide()
        gobject.timeout_add(0, self.build_close_callback)

    def set_build_titles(self, heading, subheading):
        self['window_build'].set_title(heading)
        self['label_build_titles'].set_label('<big><b>%s</b></big>\n\n%s' % (heading, subheading))

    def do_build_pulse(self):
        self['progress_build'].pulse()

    def set_build_status_change(self, initial=True):
        """
        If initial is True, the GUI is adjusted to its initial conditions, otherwise
        it is adjusted to that it the build window can be closed.
        """
        self['button_build_cancel'].set_sensitive(initial)
        self['button_build_close'].set_sensitive(not initial)
        self['checkbutton_build_auto_close'].set_sensitive(initial)
        self['progress_build'].set_fraction({True: 0.0, False: 1.0}[initial])

    def set_build_uncancellable(self):
        self['button_build_cancel'].set_sensitive(False)

    def get_build_auto_close(self):
        """
        Returns True if the build window should automatically close after a successful
        build, and False otherwise.
        """
        return self['checkbutton_build_auto_close'].get_active()
