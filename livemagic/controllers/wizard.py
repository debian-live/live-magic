import gtk

class WizardController(object):

    def on_wizard_apply(self, _):

        # Fill in data from model
        data = self.view.get_wizard_completed_details()
        self.model.binary.LIVE_BINARY_IMAGES = [data['media']]
        self.model.bootstrap.LIVE_MIRROR_BOOTSTRAP = data['mirror']
        self.model.chroot.LIVE_PACKAGES_LISTS = data['desktop']
        self.model.bootstrap.LIVE_ARCHITECTURE = data['arch']
        self.model.save()

        self.view.do_dim_wizard()
        self.do_show_build_window(self.on_wizard_build_completed)

    def on_wizard_expert_mode_selected(self, _):
        self.view.do_hide_wizard()
        self.view.do_show_main_window()

    def on_wizard_build_completed(self):
        gtk.main_quit()
