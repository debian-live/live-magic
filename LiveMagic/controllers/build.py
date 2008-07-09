import os
import sys
import shutil
import gobject
import subprocess

BUILDING, CANCELLED, CANCELLED_CLEAN, GKSU_ERROR, FAILED, \
    FAILED_CLEAN, OK, OK_CLEAN, DONE = range(9)

from LiveMagic.utils import find_resource

class BuildController(object):

    # GTK callbacks

    def on_build_activate(self, *_):
        # Save model if necessary
        if self.model.altered():
            self.model.save()
        self.do_show_build_window(self.set_window_main_sensitive)

    def do_show_build_window(self, build_close_callback):
        self.state = BUILDING
        self.build_successful = False

        # Set initial titles and state
        self.view.set_build_status_change(initial=True)

        # Show window
        self.view.do_show_window_build(build_close_callback)

        # Start pulsing
        gobject.timeout_add(100, self.do_pulse_cb)

        # Fork command
        cmd = ['/usr/bin/gksu', '--', find_resource('live-magic-builder')]
        self.pid = self.view.vte_terminal.fork_command(cmd[0], cmd, None, self.model.dir)

        if self.pid < 0:
            self.view.set_build_titles("Error creating Debian Live system!", \
                "Could not fork the build process!")
            self.view.set_build_status_change(initial=False)

    def on_window_build_delete_event(self, *_):
        # If no command is running, close the window
        if self.pid < 0:
            self.view.do_hide_window_build()
        return True

    def on_vte_child_exited(self, *_):
        self.pid = -1
        status_filename = os.path.join(self.model.dir, '.status')

        def _exec(*cmds):
            args = ['/bin/sh', '-c', '; '.join(cmds)]
            self.view.vte_terminal.fork_command(args[0], args, None, self.model.dir)

        def set_cleaning_status():
            os.remove(status_filename)
            self.view.set_build_uncancellable()
            self.view.set_build_titles("Cleaning build process",
                "Purging unnecessary parts of the build system...")

        def ok():
            self.view.set_build_titles("Build process finished",
                "Your Debian Live system has been created successfully.")
            subprocess.call(['xdg-open', '%s' % self.model.dir])
            return DONE

        def ok_clean():
            set_cleaning_status()
            _exec('lh_clean --chroot --stage --source --cache', 'rm -rf config/ binary/', \
                'gzip build-log.txt')
            return OK

        def failed():
            self.view.set_build_titles("Error when building Debian Live system",
                "There was an error when building your Debian Live system.")
            return DONE

        def failed_clean():
            set_cleaning_status()
            _exec('lh_clean --purge', 'rm -rf config/', 'gzip-build.log.txt')
            return FAILED

        def cancelled():
            self.view.set_build_titles("Build process cancelled",
                "The creation of your Debian Live system was cancelled.")
            return DONE

        def cancelled_clean():
            set_cleaning_status()
            _exec('lh_clean --purge', 'rm -rf $(pwd)')
            return CANCELLED

        def gksu_error():
            self.view.set_build_titles("Error gaining superuser priviledges",
                "There was an error when trying to gain superuser priviledges.")
            shutil.rmtree(self.model.dir)
            return DONE

        if self.state == BUILDING:
            self.state = FAILED_CLEAN
            try:
                f = open(status_filename)
                try:
                    if f.read().strip() == 'ok':
                        self.state = OK_CLEAN
                        self.build_successful = True
                finally:
                    f.close()
            except:
                self.state = GKSU_ERROR

        self.state = {
            CANCELLED: cancelled,
            CANCELLED_CLEAN: cancelled_clean,
            FAILED: failed,
            FAILED_CLEAN: failed_clean,
            GKSU_ERROR: gksu_error,
            OK: ok,
            OK_CLEAN: ok_clean,
        }[self.state]()

        if self.state == DONE:
            self.view.set_build_status_change(initial=False)

        # Auto-close if requested
        if self.view.get_build_auto_close() and self.build_successful:
            self.view.do_hide_window_build()

    def do_pulse_cb(self, *_):
        if self.state != DONE:
            self.view.do_build_pulse()
            return True

    def on_button_build_close_clicked(self, *_):
        self.view.do_hide_window_build()

    def on_button_build_cancel_clicked(self, *_):
        self.state = CANCELLED_CLEAN
        subprocess.call(['gksu', '--', '/bin/kill', '-s', 'KILL', '-%d' % self.pid])
