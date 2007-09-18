import gtk
import gobject

class MainView(object):
    def __init__(self):
        self.controller.view = self

        # Hide tabs
        self['notebook'].set_show_tabs(False)

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

    # Application-specific calls
    def do_show_main_window(self):
        self['window_main'].show()

    def do_set_window_main_sensitive(self, sensitivity):
        self['window_build'].set_sensitive(sensitivity)

    def do_select_section(self, button):
        # Move to new section tab
        _, _, name = button.get_name().split('_')
        tab = self.sections.index(name)
        self['notebook'].set_current_page(tab)

        # Set section buttons
        for section in self.sections:
            self['button_section_%s' % section].set_relief(gtk.RELIEF_NONE)
        button.set_relief(gtk.RELIEF_NORMAL)

    def setup_sections(self, sections):
        # Save sections
        self.sections = sections

        section_model = gtk.ListStore(gobject.TYPE_PYOBJECT, gobject.TYPE_STRING)
        for s in sections:
            section_model.append((None, s))

        col = gtk.TreeViewColumn("Section", gtk.CellRendererText(), text=1)

        #self['treeview_sections'].set_model(section_model)
        #self['treeview_sections'].append_column(col)

    def set_save_enabled(self, status):
        self['btn_save'].set_sensitive(status)
        self['menu_save'].set_sensitive(status)
        self['menu_save_as'].set_sensitive(status)

    def set_status_bar(self, msg):
        self['label_status'].set_text(msg)

    def do_confirm_save(self, quit_dialog=None):
        # Show a quit button if we are quitting, and a close
        # button if we are closing
        btn = quit_dialog and gtk.STOCK_QUIT or gtk.STOCK_CLOSE

        dialog = gtk.Dialog("",
            self['window_main'],
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (
                gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT,
                btn, gtk.RESPONSE_REJECT,
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            ))
        label = gtk.Label()
        label.set_markup("""<big><b>Save the changes to your configuration\nbefore continuing?</b></big>\n\nIf you don't save, changes will be permanently lost.""")
        dialog.vbox.pack_start(label, True, True, 25)
        label.show()
        dialog.set_size_request(400, 200)
        res = dialog.run()
        dialog.destroy()
        return res

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

    def do_show_loading_error(self):
        dialog = gtk.MessageDialog(
            self['window_main'],
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_ERROR,
            gtk.BUTTONS_CLOSE,
            "There was an error loading the configuration.")

        dialog.format_secondary_markup("Please ensure that you selected a directory containing a Debian Live configuration.")
        dialog.run()
        dialog.destroy()

    def do_show_about_dialog(self):
        about = gtk.AboutDialog()
        about.set_name("Debian Live Magic")
        about.set_comments("GUI configuration tool to build Debian Live systems.")
        about.set_copyright("Copyright (C) 2007 Chris Lamb <chris@chris-lamb.co.uk>")

        about.set_website("http://debian-live.alioth.debian.org/")
        about.set_website_label("Debian Live homepage")
        about.set_license(file('/usr/share/common-licenses/GPL-2').read())

        logo = gtk.gdk.pixbuf_new_from_file('/usr/share/live-magic/debian_openlogo-nd-100.png')
        about.set_logo(logo)

        about.run()
        about.destroy()

    def do_set_key_var(self, namespace, key, value):
        try:
            widget = self['%s/%s' % (namespace, key)]
            if type(widget) is gtk.Entry:
                widget.set_text(value)
            elif type(widget) is gtk.ComboBox:
                pass
            elif type(widget) is gtk.ComboBoxEntry:
                pass
            else:
                widget.get_buffer().set_text(value)
        except KeyError:
            # We either haven't got around to making a widget for this
            # key, or it is new.
            pass
