import gtk

class WizardView(object):
    def __init__(self):
        self.asst = self.construct_assistant()

    def do_show_wizard(self):
        self.asst.show()

    def do_dim_wizard(self):
        self.asst.set_sensitive(False)

    def do_hide_wizard(self):
        self.asst.hide()

    def construct_assistant(self):
        asst = gtk.Assistant()
        asst.set_title('Debian Live Magic')
        asst.set_default_size(640, 480)

        asst.connect('apply', self.controller.on_wizard_apply)
        asst.connect('cancel', lambda _: gtk.main_quit())

        label = gtk.Label('Expert mode')
        label.show()

        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_EDIT, gtk.ICON_SIZE_BUTTON)
        image.show()

        vbox = gtk.HBox(spacing=4)
        vbox.add(label)
        vbox.add(image)
        vbox.show()

        btn = gtk.Button()
        btn.add(vbox)
        btn.connect('clicked', self.controller.on_wizard_expert_mode_selected)
        btn.show()

        asst.add_action_widget(btn)

        # Don't construct to pages of the gtk.Assistant manually, load
        # them from the Glade resource file.
        notebook = self['notebook_wizard']
        page_types = [gtk.ASSISTANT_PAGE_INTRO] + \
            [gtk.ASSISTANT_PAGE_CONTENT] * (notebook.get_n_pages() - 2) + \
            [gtk.ASSISTANT_PAGE_CONFIRM]

        for i in range(notebook.get_n_pages()):
            page = notebook.get_nth_page(i)
            page.unparent()
            asst.append_page(page)
            asst.set_page_complete(page, True)
            asst.set_page_type(page, page_types[i])

            asst.set_page_title(page, notebook.get_tab_label_text(page))

        return asst

    def get_wizard_completed_details(self):
        data = {}

        def get_active(name):
            for button in self[name].get_group():
                if button.get_active() == True:
                    return button.get_name().split('_')[2]

        return {
            'desktop' : get_active('radio_desktop_gnome'),
            'media' : get_active('radio_media_usb'),
            'arch' : get_active('radio_architecture_i386'),
            'mirror' : self['combobox_mirror'].get_active_text()
        }
