# saved from: http://pastie.org/private/bclbdgxzbkb1gs2jfqzehg

import sublime
import sublime_plugin
import subprocess

class RunExternalCommand(sublime_plugin.TextCommand):
    """
    Runs an external command with the selected text,
    which will then be replaced by the command output.

    If you open the console (cmd-` or ctrl-`) and enter
    >>> view.run_command('run_external', dict(args="sort"))
    the selected text (or whole file if no selection)
    will be sorted using the "sort" command.
    """

    def run(self, edit, args):
        if self.view.sel()[0].empty():
            # nothing selected: process the entire file
            region = sublime.Region(0L, self.view.size())
        else:
            # process only selected region
            region = self.view.line(self.view.sel()[0])

        p = subprocess.Popen(
            args,
            shell=True,
            bufsize=-1,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

        output, error = p.communicate(self.view.substr(region).encode('utf-8'))
        
        if error:
            # sublime.error_message(error.decode('utf-8'))
            # I prefer seeing the error message in the status bar instead of a popup
            sublime.status_message(error.decode('utf-8'))
        else:
            self.view.replace(edit, region, output.decode('utf-8'))
            # Comment the above and uncomment the following line
            # if you want to insert the output at the start of the file
            # self.view.insert(edit, 0, output.decode('utf-8'))
