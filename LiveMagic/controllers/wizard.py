import gtk

from LiveMagic import models

class WizardController(object):

    def on_wizard_apply(self, _):

        # Fill in data from model
        data = self.view.get_wizard_completed_details()

        self.model.new()
        self.model.binary.LH_BINARY_IMAGES = [data['media']]
        self.model.bootstrap.LH_MIRROR_BOOTSTRAP = data['mirror']
        self.model.chroot.LH_PACKAGES_LISTS = data['desktop']
        self.model.bootstrap.LH_ARCHITECTURE = data['arch']
        self.model.save()

        self.view.do_dim_wizard()
        self.do_show_build_window(self.on_wizard_build_completed)

    def on_wizard_expert_mode_selected(self, _):
        self.view.do_hide_wizard()
        self.view.do_show_main_window()

    def on_wizard_build_completed(self):
        gtk.main_quit()

    def get_suggested_mirror(self):
        s = models.SourcesList()
        return s.get_mirror()

