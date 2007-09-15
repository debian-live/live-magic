import vte

class BuildView(object):
    def __init__(self):
        # Init custom widgets
        self.vte_terminal = None

    def do_show_window_build(self, build_close_callback):
        self.build_close_callback = build_close_callback
        self['window_main'].set_sensitive(False)

        # Configure VteTerminal component if necessary
        if self.vte_terminal is None:
            t = vte.Terminal()
            t.set_font_from_string('Monospace 8')
            self['vte_scrollbar'].set_adjustment(t.get_adjustment())
            self['hbox_vte'].pack_end(t)
            self['hbox_vte'].show_all()

            # Connect signals from VteTerminal
            t.connect('child-exited', self.controller.on_vte_child_exited)
            t.connect('contents-changed', self.controller.on_vte_contents_changed)

            self.vte_terminal = t

        self.vte_terminal.reset(True, True)
        self['window_build'].show()

    def do_hide_window_build(self):
        self['window_build'].hide()
        self.build_close_callback()

    def set_build_titles(self, title, heading, subheading):
        self['window_build'].set_title(title)
        self['label_build_titles'].set_label('<big><b>%s</b></big>\n\n%s' % (heading, subheading))

    def set_build_status(self, msg):
        self['label_build_status'].set_label('<i>%s</i>' % msg)

    def do_build_pulse(self):
        self['progress_build'].pulse()

    def set_build_status_change(self, initial=True):
        """
        If initial is True, the GUI is adjusted to its initial conditions, otherwise
        it is adjusted to that it the build window can be closed.
        """
        self['button_build_cancel'].set_sensitive(initial)
        self['button_build_close'].set_sensitive(not initial)
        self['checkbutton_build_auto_close'].set_sensitive(initial)
        self['progress_build'].set_fraction({True: 0, False: 1}[initial])

    def get_build_auto_close(self):
        """
        Returns True if the build window should automatically close after a successful
        build, and False otherwise.
        """
        return self['checkbutton_build_auto_close'].get_active()
