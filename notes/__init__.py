from fman import DirectoryPaneCommand, show_alert, load_json, save_json, show_prompt, show_quicksearch, QuicksearchItem, show_status_message, clear_status_message
from core.quicksearch_matchers import contains_chars
from core.commands import _get_thirdparty_plugins, _THIRDPARTY_PLUGINS_DIR
from fman.url import basename, dirname
from fman.fs import exists, mkdir, touch

NOTESDIR = None
NOTESDIRNAME = 'notesdir'
#
# Class:        Notes
#
# Description:  This class is a subclass of DirectoryPaneCommand. It is 
#               used to open a note file in the `.notes` subdirectory 
#               in the user's defined editor. It will create the directory 
#               if it doesn't already exist. It will also save the new 
#               directory in the list of note directories.
#
class Notes (DirectoryPaneCommand):
    def __call__(self, url=None):
        #
        # Make sure the `.notes` directory exists. If not, create it.
        #
        notePath = self.pane.get_path() + "/.notes/"
        if not exists(notePath):
            mkdir(notePath)
            saveNotesDir(notePath)

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

 def getNotesDir():
    global NOTESDIR, NOTESDIRNAME
    if NOTESDIR == None:
        NOTESDIR = load_json(NOTESDIRNAME,default=[])
    return(NOTESDIR)

def saveNotesDir(newDir):
    global NOTESDIR
    notes = getNotesDir()
    if not newDir in notes:
        NOTESDIR = notes.append(newDir)
        saveNotesDirDisk()

def saveNotesDirDisk();
    global NOTESDIR, NOTESDIRNAME
    save_json(NOTESDIRNAME, NOTESDIR)

#
# Class:        GoToNoteDir
#
# Description:  A Pane command to jump to a notes directory.
#
class GoToNoteDir(DirectoryPaneCommand):
    #
    # This directory command is for selecting a note directory 
    # and going to that directory.
    #
    def __call__(self):
        show_status_message('Select Note Directory')
        result = show_quicksearch(self._suggest_directory)
        if result:
            query, dirName = result
            self.pane.set_path(dirName)
        clear_status_message()

    def _suggest_directory(self, query):
        directories = getNotesDir()
        for dirName in directories:
            match = contains_chars(dirName.lower(), query.lower())
            if match or not query:
                yield QuicksearchItem(dirName, highlight=match)

