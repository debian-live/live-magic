import gtk
import os.path

from DebianLive import Config, utils

class WizardController(object):

    def on_wizard_apply(self, _):
        build_dir = utils.get_build_dir()
        data = self.view.get_wizard_completed_details()

        # Use cdebootstrap in some situations
        if os.path.exists('/usr/bin/cdebootstrap') and \
                            data['distribution' in ('etch', 'lenny'):
            data['bootstrap'] = 'cdebootstrap'

        # Disabling caching
        data['cache_stages'] = 'none'
        data['cache_packages'] = False

        self.model = Config(build_dir, **data)

        self.view.do_dim_wizard()
        self.do_show_build_window(lambda: gtk.main_quit())

    def on_wizard_expert_mode_selected(self, _):
        self.view.do_hide_wizard()
        self.view.do_show_main_window()

    def get_suggested_mirror(self):
        s = utils.SourcesList()
        return s.get_mirror()

    def on_wizard_cancel(self, *args):
        if self.view.do_show_wizard_cancel_confirm_window():
