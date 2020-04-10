from fman import DirectoryPaneCommand, show_alert
from core.commands import _get_thirdparty_plugins, _THIRDPARTY_PLUGINS_DIR
from fman.url import basename, dirname
from fman.fs import exists, mkdir, touch

#
# Class:        Notes
#
# Description:  This class is a subclass of DirectoryPaneCommand. It is 
#               used to open a note file in the `.notes` subdirectory 
#               in the user's defined editor.
#
class Notes (DirectoryPaneCommand):
    def __call__(self, url=None):
        #
        # Make sure the `.notes` directory exists. If not, create it.
        #
        notePath = self.pane.get_path() + "/.notes/"
        if not exists(notePath):
            mkdir(notePath)

        #
        # Get either the current cursor file or the file
        # sent in the url command.
        #
        cursorFile = self.pane.get_file_under_cursor()
        if cursorFile == None and url == None:
            show_alert('Nothing is selected.')
            return

        if not url == None:
            cursorFile = url
            #
            # Change the notes directory to the directory of the file sent.
            #
            notePath = dirname(url) + "/.notes"
            if not exists(notePath):
                mkdir(notePath)
 
        #
        # Open the note file for the file or directory.
        #
        cfName = basename(cursorFile)
        cfNoteFile = notePath + cfName + ".md"

        #
        # If the OpenWithEditor plugin is loaded, use it to edit 
        # the file. Otherwise, use the system edit command. The 
        # touch command will create the file if it doesn't exist.
        #
        touch(cfNoteFile)
        if (_THIRDPARTY_PLUGINS_DIR + "/OpenWithEditor") in _get_thirdparty_plugins():
            self.pane.run_command("my_open_with_editor", args={'url': cfNoteFile})
        else:
            self.pane.run_command("open_with_editor", args={'url': cfNoteFile})

