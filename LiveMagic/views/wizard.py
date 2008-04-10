import gtk

class WizardView(object):
    def __init__(self):
        self.asst = gtk.Assistant()
        self.asst.set_title('Debian Live Magic')
        self.asst.set_default_size(640, 480)

        self.asst.connect('apply', self.controller.on_wizard_apply)
        self.asst.connect('cancel', self.controller.on_wizard_cancel)

        def add_expert_mode():
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

            self.asst.add_action_widget(btn)

        # Load paages from Glade resource file.
        notebook = self['notebook_wizard']
        page_types = [gtk.ASSISTANT_PAGE_INTRO] + \
            [gtk.ASSISTANT_PAGE_CONTENT] * (notebook.get_n_pages() - 2) + \
            [gtk.ASSISTANT_PAGE_CONFIRM]

        for i in range(notebook.get_n_pages()):
            # Only show architecture page if using amd64
            if notebook.get_n_pages() - 2 == i and \
                self.controller.get_host_architecture() != 'amd64':
                continue

            page = notebook.get_nth_page(i)
            page.unparent()
            self.asst.append_page(page)
            self.asst.set_page_complete(page, True)
            self.asst.set_page_type(page, page_types[i])

            self.asst.set_page_title(page, notebook.get_tab_label_text(page))

        c = self['combobox_mirror']
        c.prepend_text(self.controller.get_suggested_mirror())
        c.set_active(0)

    def do_show_wizard(self):
        self.asst.show()

    def do_dim_wizard(self):
        self.asst.set_sensitive(False)

    def do_hide_wizard(self):
        self.asst.hide()

    def get_wizard_completed_details(self):
        def get_active(name):
            for button in self[name].get_group():
                if button.get_active() == True:
                    return button.get_name().split('_')[2]

        data = {
            'packages_lists' : get_active('radio_desktop_gnome'),
            'binary_images' : get_active('radio_media_iso'),
            'distribution' : get_active('radio_distribution_stable'),
            'mirror' : self['combobox_mirror'].get_active_text()
        }

        if self.controller.get_host_architecture() == 'amd64':
            data['architecture'] = get_active('radio_architecture_i386')

        return data

    def do_show_wizard_cancel_confirm_window(self):
        dialog = gtk.MessageDialog(
            parent=self.asst,
            flags=gtk.DIALOG_MODAL,
            type=gtk.MESSAGE_QUESTION,
            buttons=gtk.BUTTONS_YES_NO,
            message_format="Are you sure you wish to cancel?");

        res = dialog.run()
        dialog.destroy()
        return res == gtk.RESPONSE_YES
