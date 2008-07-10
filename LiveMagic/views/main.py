import gtk
import gobject

from LiveMagic.utils import find_resource

class MainView(object):
    def __init__(self):
        self.controller.view = self

    def __getitem__(self, key):
        widget = self.xml.get_widget(key)
        if widget is None:
            raise KeyError, "Widget not found: %s" % key
        return widget

    def __contains__(self, key):
        try:
            _ = self[key]
        except KeyError:
            return False
        return True

    def do_folder_open(self):
        dialog = gtk.FileChooserDialog("Open Configuration",
            self['window_main'],
            gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
            (
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                gtk.STOCK_OPEN, gtk.RESPONSE_ACCEPT,
            ))

        res = dialog.run()
        filename = dialog.get_filename()
        dialog.destroy()
        return res, filename

    def do_show_about_dialog(self):
        about = gtk.AboutDialog()
        about.set_name("Debian Live Magic")
        about.set_comments("GUI tool to build Debian Live systems.")
        about.set_copyright("Copyright (C) 2007-2008 Chris Lamb <chris@chris-lamb.co.uk>")

        about.set_website("http://debian-live.alioth.debian.org/")
        about.set_website_label("Debian Live homepage")
        about.set_license(file(find_resource('GPL-3')).read())

        logo = gtk.gdk.pixbuf_new_from_file(find_resource('debian_openlogo-nd-100.png'))
        about.set_logo(logo)

        about.run()
        about.destroy()
