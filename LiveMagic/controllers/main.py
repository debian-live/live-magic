import os
import gtk
import pwd
import sys

class MainController(object):

    def ready(self, options, args):
        self.options = options

        if options.build_for:
            self.do_show_build_window(lambda: gtk.main_quit())
        else:
            self.view.do_show_wizard()

    def on_quit_request(self, *_):
        return self._confirm_save(lambda: gtk.main_quit(), quit_dialog=True)

    def on_about_request(self, *_):
        self.view.do_show_about_dialog()

    def get_host_architecture(self):
        import commands
        status, output = commands.getstatusoutput('dpkg --print-architecture')
        assert status == 0
        return output

    def get_homedir(self):
        uid = os.geteuid()
        return pwd.getpwuid(uid)[5]
