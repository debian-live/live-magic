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
import pwd
import sys
import gobject
import subprocess

BUILDING, CANCELLED, CANCELLED_CLEAN, FAILED, \
    FAILED_CLEAN, OK, OK_CLEAN, DONE = range(8)

from LiveMagic.utils import find_resource

LOG_FILE = 'build-log.txt'
STATUS_FILE = '.status'

class BuildController(object):

    def do_show_build_window(self, build_close_callback):
        self.state = BUILDING
        self.build_successful = False

        self.uid, self.gid = [int(x) for x in self.options.build_for.split(':', 2)]

        f = open(os.path.join(LOG_FILE), 'w')
        print >>f, "I: live-magic respawned as root"
        f.close()

        # Set initial titles and state
        self.view.set_build_status_change(initial=True)

        # Show window
        self.view.do_show_window_build(build_close_callback)

        # Start pulsing
        gobject.timeout_add(80, self.do_pulse_cb)

        # Fork command
        cmd = [find_resource('live-magic-builder')]
        self.pid = self.view.vte_terminal.fork_command(cmd[0], cmd, None, os.getcwd())

        if self.pid < 0:
            self.view.set_build_titles(_("Error creating Debian Live system!"), \
                "Could not fork the build process!")
            self.view.set_build_status_change(initial=False)

    def on_window_build_delete_event(self, *args):
        # If no command is running, close the window
        if self.pid < 0:
            self.view.do_hide_window_build()
        return True

    def on_vte_child_exited(self, *args):
        def _exec(*cmds):
            glue = ' | tee -a %s ;' % LOG_FILE
            args = ['/bin/sh', '-c', glue.join(cmds)]
            self.view.vte_terminal.fork_command(args[0], args, None, os.getcwd())

        def set_cleaning_status():
            try:
                os.remove(STATUS_FILE)
            except:
                # This may fail as we removed the build directory
                pass
            self.view.set_build_uncancellable()
            self.view.set_build_titles(_("Cleaning build system"),
                _("Purging unnecessary parts of the build system..."))

        def ok():
            self.view.set_build_titles(_("Build process finished"),
                _("Your Debian Live system has been created successfully."))

            if self.options.kde_full_session != '-':
                os.environ['KDE_FULL_SESSION'] = self.options.kde_full_session
            if self.options.gnome_desktop_session_id != '-':
                os.environ['GNOME_DESKTOP_SESSION_ID'] = self.options.gnome_desktop_session_id

            # Try some file managers.
            for manager in ('/usr/bin/xdg-open', '/usr/bin/pcmanfm'):
                if not os.path.exists(manager):
                    continue

                cmd = ['su', pwd.getpwuid(self.uid)[0], '-c', '%s .' % manager]
                if not subprocess.call(cmd):
                    continue

            return DONE

        def ok_clean():
            set_cleaning_status()
            _exec('lh_clean --chroot --stage --source --cache',
                'rm -rf config/ binary/ tftpboot/',
                'chown -R %d:%d .' % (self.uid, self.gid))
            return OK

        def failed():
            self.view.set_build_titles(_("Error when building Debian Live system"),
                _("There was an error when building your Debian Live system."))
            return DONE

        def failed_clean():
            set_cleaning_status()
            _exec('lh_clean --purge', 'rm -rvf config/',
                'chown -R %d:%d .' % (self.uid, self.gid))
            return FAILED

        def cancelled():
            self.view.set_build_titles(_("Build process cancelled"),
                _("The creation of your Debian Live system was cancelled."))
            return DONE

        def cancelled_clean():
            set_cleaning_status()
            _exec('lh_clean --purge', 'rm -rvf $(pwd)')
            return CANCELLED

        if self.state == BUILDING:
            self.state = FAILED_CLEAN
            try:
                f = open(STATUS_FILE)
                try:
                    if f.read().strip() == 'ok':
                        self.state = OK_CLEAN
                        self.build_successful = True
                finally:
                    f.close()
            except:
                pass

        self.state = {
            CANCELLED: cancelled,
            CANCELLED_CLEAN: cancelled_clean,
            FAILED: failed,
            FAILED_CLEAN: failed_clean,
            OK: ok,
            OK_CLEAN: ok_clean,
        }[self.state]()

        if self.state == DONE:
            self.view.set_build_status_change(initial=False)
            self.pid = -1

        # Auto-close if requested
        if self.view.get_build_auto_close() and self.build_successful:
            self.view.do_hide_window_build()

    def do_pulse_cb(self, *args):
        if self.state != DONE:
            self.view.do_build_pulse()
            return True

    def on_button_build_close_clicked(self, *args):
        self.view.do_hide_window_build()

    def on_button_build_cancel_clicked(self, *args):
        self.state = CANCELLED_CLEAN
        subprocess.call(['/bin/kill', '-s', 'KILL', '-%d' % self.pid])
