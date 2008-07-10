import os
import gtk
import time
import popen2
import shutil
import gobject
import threading
import subprocess

from LiveMagic import utils
from DebianLive import Config

class WizardController(object):
    def on_wizard_apply(self, _):
        data, build_dir = self.view.get_wizard_completed_details()

        if build_dir in (self.get_homedir(), os.path.expanduser('~/DebianLive')):
            build_dir = os.path.expanduser('~/DebianLive/build-%s' % time.strftime('%Y-%m-%d-%H%M-%S'))
        elif len(os.listdir(build_dir)) != 0:
            build_dir = os.path.join(build_dir, 'DebianLive')

        # Use cdebootstrap in some situations
        if os.path.exists('/usr/bin/cdebootstrap') and \
                                data['distribution'] in ('etch', 'lenny'):
            data['bootstrap'] = 'cdebootstrap'

        # Disabling caching
        data['cache_stages'] = 'none'
        data['cache_packages'] = False

        self.model = Config(build_dir, **data)

        self.view.do_dim_wizard()

        os.chdir(build_dir)

        def gain_superuser():
            title = "Enter your password to continue"
            text = "Live-magic requires superuser capabilities to build your Debian Live system."

            for _ in range(3):
                cmd = ['gksu', '--disable-grab', '--preserve-env',
                    '--message', '<big><b>%s</b></big>\n\n%s' % (title, text), '--',
                    utils.find_resource('live-magic'),
                    '--build-for', '%d:%d' % (os.geteuid(), os.getegid()),
                    '--kde-full-session', os.environ.get('KDE_FULL_SESSION', '-'),
                    '--gnome-desktop-session-id', os.environ.get('GNOME_DESKTOP_SESSION_ID', '-')]
                p = subprocess.Popen(cmd)

                os.waitpid(p.pid, 0)

                try:
                    # If build-log.txt exists, we had a successful build
                    os.stat(os.path.join(self.model.dir, 'build-log.txt'))
                    gobject.timeout_add(0, lambda: gtk.main_quit())
                    return
                except:
                    pass

                try:
                    os.stat(self.model.dir)
                except:
                    # If the build directory does not exist, we cancelled the build
                    break

            self.view.do_undim_wizard()
            os.chdir('..')
            try:
                shutil.rmtree(self.model.dir)
            except:
                # Tree may not exist if we cancelled build
                pass

        threading.Thread(target=gain_superuser).start()

    def on_wizard_cancel(self, *args):
        if self.view.do_show_wizard_cancel_confirm_window():
            gtk.main_quit()
