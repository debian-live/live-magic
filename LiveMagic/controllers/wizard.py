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
import gtk
import time
import shutil
import gobject
import threading
import subprocess

from LiveMagic import utils
from DebianLive import Config

class WizardController(object):
    def on_wizard_apply(self, asst):
        data, build_dir = self.view.get_wizard_completed_details()

        if build_dir in (self.get_homedir(), os.path.expanduser('~/DebianLive')):
            build_dir = os.path.expanduser('~/DebianLive/build-%s' % time.strftime('%Y-%m-%d-%H%M-%S'))
        elif len(os.listdir(build_dir)) != 0:
            build_dir = os.path.join(build_dir, 'DebianLive')

        existed_before = os.path.exists(build_dir)

        # Use cdebootstrap in some situations
        if os.path.exists('/usr/bin/cdebootstrap') and \
                                data['distribution'] in ('lenny',):
            data['bootstrap'] = 'cdebootstrap'

        # Disabling caching
        data['cache_stages'] = 'none'
        data['cache_packages'] = False

        self.model = Config(build_dir, **data)

        self.view.do_dim_wizard()

        os.chdir(build_dir)

        def gain_superuser():
            global _
            title = _("Enter your password to continue")
            text = _("Debian Live Magic requires superuser capabilities to build your Debian Live system.")

            for num in range(3):
                cmd = ['gksu', '--disable-grab', '--preserve-env',
                    '--message', '<big><b>%s</b></big>\n\n%s' % (title, text), '--',
                    utils.find_resource('live-magic'),
                    '--build-for', '%d:%d' % (os.geteuid(), os.getegid()),
                ]
                p = subprocess.Popen(cmd)

                os.waitpid(p.pid, 0)

                # If build-log.txt exists, we had a successful build
                if os.path.exists(os.path.join(self.model.dir, 'build-log.txt')):
                    gobject.timeout_add(0, lambda: gtk.main_quit())
                    return

                # If the build directory does not exist, we cancelled the build
                if not os.path.exists(self.model.dir):
                    break

            self.view.do_undim_wizard()
            os.chdir('..')

            try:
                if not existed_before:
                    shutil.rmtree(self.model.dir)
            except:
                # Tree may not exist if we cancelled build
                pass

        threading.Thread(target=gain_superuser).start()

    def on_wizard_cancel(self, *args):
        if self.view.do_show_wizard_cancel_confirm_window():
            gtk.main_quit()

    def on_radio_media_net_group_changed(self, button):
        self.view.toggle_netboot_settings(button)
