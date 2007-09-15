import gtk
import gobject
import pango
import mimetypes

class HooksView(object):
    def __init__(self):
        # Configure the hook combo box
        hbox = self['hbox_hooks']
        self.cb = gtk.combo_box_new_text()
        self.cb.show()
        self.cb.connect("changed", self.controller.on_hook_select)
        hbox.pack_start(self.cb)
        hbox.reorder_child(self.cb, 0)

        # Configure editor
        try:
            from gtksourceview import SourceBuffer, SourceView
            buffer = SourceBuffer()
            self.hook_editor = SourceView(buffer)
            self.hook_editor.set_show_line_numbers(True)
            buffer.set_highlight(True)
        except ImportError:
            self.hook_editor = gtk.TextView()

        font_desc = pango.FontDescription('Monospace 8')
        if font_desc:
            self.hook_editor.modify_font(font_desc)

        self.hook_editor.get_buffer().connect("changed", self.controller.on_hook_editor_changed)

        self['scroll_hook_edit'].add_with_viewport(self.hook_editor)
        self.do_enable_edit_hook(False)
        self.hook_editor.show()

    def do_show_new_hook_window(self):
        dialog = gtk.Dialog(
            "Choose filename",
            self['window_main'],
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (   gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        entry = gtk.Entry(256)
        entry.connect("activate", lambda _: dialog.action_area.get_children()[1].clicked())

        dialog.vbox.pack_start(entry, padding=10)
        dialog.vbox.show_all()
        res = dialog.run()
        dialog.destroy()

        if res == gtk.RESPONSE_ACCEPT:
            return entry.get_text().strip()
        else:
            return None

    def do_show_rename_hook_window(self, old_hook_name):
        dialog = gtk.Dialog(
            "Choose new name for %s" % old_hook_name,
            self['window_main'],
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (   gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        entry = gtk.Entry(256)
        entry.connect("activate", lambda _: dialog.action_area.get_children()[1].clicked())

        dialog.vbox.pack_start(entry, padding=10)
        dialog.vbox.show_all()
        res = dialog.run()
        dialog.destroy()

        if res == gtk.RESPONSE_ACCEPT:
            return entry.get_text().strip()
        else:
            return None

    def do_show_hook_import_dialog(self):
        dialog = gtk.FileChooserDialog(
            "Choose hook to import",
            self['window_main'],
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (
                gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

        dialog.set_current_folder("/usr/share/live-helper/examples/hooks")

        res = dialog.run()
        filename = dialog.get_filename()
        dialog.destroy()

        if res == gtk.RESPONSE_ACCEPT:
            return filename
        else:
            return None

    def do_show_error(self, title):
        dialog = gtk.MessageDialog(
            self['window_main'],
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_ERROR,
            gtk.BUTTONS_CLOSE,
            title,
            )
        dialog.run()
        dialog.destroy()

    def do_show_hook_delete_confirm_window(self):
        dialog = gtk.Dialog(
            "Are you sure?",
            self['window_main'],
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (   gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        res = dialog.run()
        dialog.destroy()
        return (res == gtk.RESPONSE_ACCEPT)

    def do_hook_add(self, filename):
        self.cb.append_text(filename)

    def get_selected_hook(self):
        filename = self.cb.get_active_text()
        return filename

    def do_hooks_clear(self):
        self.hook_editor.set_sensitive(False)
        for _ in xrange(len(self.cb.get_model())):
            self.cb.remove_text(0)

    def get_hook_editor_contents(self):
        buf = self.hook_editor.get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter())

    def do_enable_edit_hook(self, enabled):
        self.cb.set_sensitive(enabled)
        self.hook_editor.set_sensitive(enabled)
        self['button_hook_rename'].set_sensitive(enabled)
        self['button_hook_delete'].set_sensitive(enabled)

    def do_set_selected_hook(self, hook_name):
        # Update combo box to reflect selection
        m = self.cb.get_model()
        iter = m.get_iter_first()

        while iter is not None:
            if hook_name == m.get_value(iter, 0):
                self.cb.set_active_iter(iter)
                return
            iter = m.iter_next(iter)

    def do_clear_hook_contents(self):
        buffer = self.hook_editor.get_buffer()
        buffer.begin_not_undoable_action()
        buffer.set_text("")
        buffer.end_not_undoable_action()

    def do_set_selected_hook_contents(self, contents):
        buffer = self.hook_editor.get_buffer()
        buffer.begin_not_undoable_action()

        # Set hook editor contents and allow editing
        buffer.set_text(contents)
        self.do_enable_edit_hook(True)
        self.hook_editor.grab_focus()

        buffer.end_not_undoable_action()

        # Set highlighting
        try:
            import gnomevfs
            from gtksourceview import SourceLanguagesManager

            mime_type = gnomevfs.get_mime_type_for_data(contents)
            lang = SourceLanguagesManager().get_language_from_mime_type(mime_type)
            buffer.set_language(lang)
        except ImportError:
            pass
