import os
import gtk
import time
import popen2
import shutil
import threading
import subprocess

from LiveMagic import utils
from DebianLive import Config
from DebianLive.utils import SourcesList, get_build_dir

class WizardController(object):
    def on_wizard_apply(self, _):
        build_dir = get_build_dir()
        data = self.view.get_wizard_completed_details()

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
        build_for = '%d:%d' % (os.geteuid(), os.getegid())

        def gain_superuser():
            title = "Enter your password to continue"
            text = "Live-magic requires superuser capabilities to build your Debian Live system."

            for _ in range(3):
                cmd = ['gksu', '--disable-grab', '--preserve-env',
                    '--message', '<big><b>%s</b></big>\n\n%s' % (title, text), '--',
                    utils.find_resource('live-magic'), '--build-for', build_for,
                    '--kde-full-session', os.environ.get('KDE_FULL_SESSION', '-'),
                    '--gnome-desktop-session-id', os.environ.get('GNOME_DESKTOP_SESSION_ID', '-')]
                p = subprocess.Popen(cmd)

                os.waitpid(p.pid, 0)
                try:
                    os.stat(os.path.join(self.model.dir, 'build-log.txt'))
                    gtk.main_quit()
                    return
                except:
                    pass

            self.view.do_undim_wizard()
            os.chdir('..')
            shutil.rmtree(self.model.dir)

        threading.Thread(target=gain_superuser).start()

    def get_suggested_mirror(self):
        return SourcesList().get_mirror()

    def on_wizard_cancel(self, *args):
        if self.view.do_show_wizard_cancel_confirm_window():
            gtk.main_quit()
