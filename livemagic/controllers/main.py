import gtk
from livemagic.model import KeyVarConfigFile

class MainController(object):
    def __init__(self, args):
        self.model.attach_load_observer(self.notify_load)
        self.args = args

    def notify_load(self):
        for child in self.model.children:
            # Check we are dealing with normal configuration values
            if type(child) is KeyVarConfigFile:
                for key in child:
                    # Set the value in the view
                    self.view.do_set_key_var(child.shortname, key, getattr(child, key))

    def ready(self):
        """
        Called when the view is ready for setup.
        """
        sections = ['common', 'chroot', 'binary', 'bootstrap', 'source', 'hooks']
        self.view.setup_sections(sections)

        # Notify all the observers that depend on the model
        self.model.notify_load_observers()

        if len(self.args) == 0:
            self.view.do_show_wizard()
        else:
            self.view.do_show_main_window()

    # GTK callbacks
    def on_live_helper_value_changed(self, widget):
        namespace, key = widget.name.split("/")
        value = widget.get_text()

        # Call self.model.namespace.key = vaulue
        ns = getattr(self.model, namespace)
        setattr(ns, key, value)

        # Variables have been tainted, allow saving
        self.view.set_save_enabled(True)

    def on_choose_section(self, button):
        self.view.do_select_section(button)

    def on_new(self, *_):
        if self.model.altered():
            print "Not newing as not saved"
        else:
            self.model.new()
        self.view.set_save_enabled(True)

    def on_open(self, *_):
        def open_dialog(self):
            res, filename = self.view.do_folder_open()
            if res == gtk.RESPONSE_ACCEPT:
                try:
                    self.model.open(filename)
                    self.view.set_save_enabled(False)
                except IOError:
                    self.view.do_show_loading_error()
        return self._confirm_save(lambda: open_dialog(self), quit_dialog=False)

    def on_save(self, *_):
        self.view.set_save_enabled(False)
        self.view.set_status_bar("Saving configuration to %s ..." % self.model.dir)
        self.model.save()
        self.view.set_status_bar("Saved configuration to %s" % self.model.dir)

    def on_save_as(self, *_):
        raise NotImplemented

    def _confirm_save(self, fn, **kw):
        if self.model.altered():
            res = self.view.do_confirm_save(**kw)
            if res == gtk.RESPONSE_ACCEPT: # Save
                self.on_save(None)
                fn()
            elif res == gtk.RESPONSE_REJECT: # Don't save
                fn()
            else:
                return True # Cancel
        else:
            # We are up to date
            fn()

    def on_quit_request(self, *_):
        return self._confirm_save(lambda: gtk.main_quit(), quit_dialog=True)

    def on_about_activate(self, *_):
        self.view.do_show_about_dialog()

    def set_window_main_sensitive(self):
        self.view.do_show_main_window(True)
