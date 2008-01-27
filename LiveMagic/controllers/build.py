import os
import sys
import signal
import gobject
import tempfile
import threading

class BuildController(object):

    # GTK callbacks

    def on_build_activate(self, *_):
        # Save model if necessary
        if self.model.altered():
            self.model.save()

        self.do_show_build_window(self.set_window_main_sensitive)

    def do_show_build_window(self, build_close_callback):
        self.cancelled = False
        self.fifo = None

        # Set initial titles and state
        self.view.set_build_titles("Generating Debian Live system...", \
            "Generating Debian Live system.", \
            "Please wait while your Live system is generated for you.")
        self.view.set_build_status("Forking build process..")
        self.view.set_build_status_change(initial=True)

        # Show window
        self.view.do_show_window_build(build_close_callback)

        # Start pulsing
        gobject.timeout_add(100, self.do_pulse_cb)

        # Create log FIFO
        fd, self.fifo = tempfile.mkstemp()
        os.close(fd)
        os.unlink(self.fifo)
        os.mkfifo(self.fifo)

        class BuildLogWatcher(threading.Thread):
            def run(self):
                f = None
                try:
                    f = open(self.controller.fifo, 'r')
                    while not self.controller.cancelled:
                        data = f.readline()

                        for prefix in ("I: ", "P: "):
                            if data.startswith(prefix) and not self.controller.cancelled:
                                msg = data[len(prefix):]
                                gobject.timeout_add(0, lambda: self.controller.view.set_build_status(msg))
                finally:
                    if f:
                        f.close()

        b = BuildLogWatcher()
        b.controller = self
        b.start()

        # Fork command
        cmd = ['/usr/bin/gksu', '-k', "/bin/sh -c '{ echo I: lh_build starting in `pwd`; lh_build 2>&1; echo I: lh_build returned with error code $?; } | tee build-log.txt %s; '" % self.fifo]
        self.pid = self.view.vte_terminal.fork_command(cmd[0], cmd, None, self.model.dir)

        if self.pid >= 0:
            self.view.set_build_status("Build process forked (pid %d)..." % self.pid)
        else:
            self.view.set_build_titles("Error", "Error creating Debian Live system!", \
                "Could not fork the build process!")
            # Allow user to close window
            self.view.set_build_status_change(initial=False)

        self.view.do_build_completed()

    def on_window_build_delete_event(self, *_):
        # If no command is running, close the window
        if self.pid < 0:
            self.view.do_hide_window_build()
        return True

    def on_vte_child_exited(self, *_):
        self.pid = -1

        # Remove fifo
        if self.fifo:
            os.unlink(self.fifo)

        if self.view.get_build_auto_close():
            self.view.do_hide_window_build()
        else:
            # Set UI state to finished
            self.view.set_build_status_change(initial=False)

            # Display a different message if build process was cancelled
            if self.cancelled is True:
                self.view.set_build_titles("Build process cancelled", "Cancelled", \
                    "The creation of your Debian Live system was cancelled.")
                self.view.set_build_status("Build process cancelled.")
            else:
                self.view.set_build_titles("Build process finished", "Finished", \
                    "Your Debian Live system has been created successfully.")
                self.view.set_build_status("Build process complete.")

    def do_pulse_cb(self, *_):
        self.view.do_build_pulse()
        return self.pid > 0

    def on_button_build_close_clicked(self, *_):
        # The build button is only sensitive when it is safe to close, so
        # no check required.
        self.view.do_hide_window_build()

    def on_button_build_cancel_clicked(self, *_):
        self.cancelled = True
        os.kill(self.pid, signal.SIGTERM)
