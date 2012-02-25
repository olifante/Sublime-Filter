# based on http://pastie.org/private/bclbdgxzbkb1gs2jfqzehg

import sublime
import sublime_plugin
import subprocess

class RunExternalCommand(sublime_plugin.TextCommand):
    """
    Runs an external command with the selected text, which will then be
    replaced by the command output.

    For example, to sort the selected text with the Unix "sort" command,
    open the console (cmd-` or ctrl-`), input the following and press enter:

    view.run_command('run_external', dict(command="sort"))

    You could add a "filter through sort" shortcut by inserting something like
    this in your user's keymap file:

    {
        "keys": ["alt+super+s"],
        "command": "run_external",
        "args": {"command": "sort"}
    }
    """

    def run(self, edit, command):
        if self.view.sel()[0].empty():
            ## if nothing selected, process the entire file:
            region = sublime.Region(0L, self.view.size())
        else:
            ## process only selected region:
            region = self.view.line(self.view.sel()[0])

        p = subprocess.Popen(
            command,
            shell=True,
            bufsize=-1,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

        output, error = p.communicate(self.view.substr(region).encode('utf-8'))

        if error:
            # sublime.error_message(error.decode('utf-8'))
            ## I prefer seeing the error message in the status bar
            ## instead of inside a popup window.
            sublime.status_message(error.decode('utf-8'))
        else:
            self.view.replace(edit, region, output.decode('utf-8'))
            ## Comment the above and uncomment the following line
            ## if you want to insert the output at the start of the file:
            # self.view.insert(edit, 0, output.decode('utf-8'))
