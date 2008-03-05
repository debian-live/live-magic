
class HooksController(object):
    def __init__(self):
        #self.model.attach_load_observer(self.notify_load_hooks)
        self.hook_select_triggers_change = True

    def on_hook_select(self, *_):
        self.hook_select_triggers_change = False
        hook_name = self.view.get_selected_hook()
        contents = self.model.hooks[hook_name]
        self.view.do_set_selected_hook_contents(contents)
        self.hook_select_triggers_change = True

    def notify_load_hooks(self):
        self.view.do_hooks_clear()
        for filename in sorted(self.model.hooks.files.iterkeys()):
            self.view.do_hook_add(filename)

    def _new_hook_template(self, hook_name):
        # Try and guess the interpreter for the specified filename
        try:
            interpreter = {
                "rb" : "#!/usr/bin/env ruby",
                "pl" : "#!/usr/bin/perl",
                "py" : "#!/usr/bin/env python",
            }[hook_name.rsplit(".")[1]]
        except:
            # Can't guess: assume it's a shell script.
            interpreter = "#!/bin/sh"

        return "%s\n\n# %s -- description_of_hook\n\n" % (interpreter, hook_name)

    def on_button_hook_new_clicked(self, *_):
        hook_name = self.view.do_show_new_hook_window()
        if hook_name is not None:
            if len(hook_name) > 0 and hook_name not in self.model.hooks:
                self.model.hooks[hook_name] = self._new_hook_template(hook_name)
                self.view.set_save_enabled(True)
                self.notify_load_hooks()
                self.view.do_set_selected_hook(hook_name)
                self.view.do_set_selected_hook_contents(self.model.hooks[hook_name])
            else:
                self.view.do_show_error("The name you specified is invalid")

    def on_button_hook_import_clicked(self, *_):
        filename = self.view.do_show_hook_import_dialog()
        if filename is not None:
            hook_name = self.model.hooks.import_file(filename)
            self.notify_load_hooks()
            self.view.do_set_selected_hook(hook_name)
            self.view.set_save_enabled(True)

    def on_button_hook_rename_clicked(self, *_):
        hook_name = self.view.get_selected_hook()
        new_hook_name = self.view.do_show_rename_hook_window(hook_name)

        if new_hook_name is None:
            return

        try:
            self.model.hooks.rename(hook_name, new_hook_name)
            self.notify_load_hooks()
            self.view.do_set_selected_hook(new_hook_name)
            self.view.set_save_enabled(True)
        except ValueError:
            self.view.do_show_error("The name already exists")

    def on_button_hook_delete_clicked(self, *_):
        ret = self.view.do_show_hook_delete_confirm_window()
        if not ret:
            return

        hook_name = self.view.get_selected_hook()
        self.model.hooks.delete(hook_name)
        self.notify_load_hooks()
        self.view.do_clear_hook_contents()
        self.view.do_enable_edit_hook(False)
        self.view.set_save_enabled(True)

    def on_hook_editor_changed(self, *_):
        if self.hook_select_triggers_change:
            self.view.set_save_enabled(True)
        hook = self.view.get_selected_hook()
        if hook is not None:
            self.model.hooks[hook] = self.view.get_hook_editor_contents()
