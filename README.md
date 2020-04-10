## Notes

Plugin for [fman.io](https://fman.io) to give the ability to add notes to files and 
directories.

You can install this plugin by pressing `<shift+cmd+p>` to open the command pallet. 
Then type `install plugin`. Look for the `Notes` plugin and select it.

### Usage

Select a file or directory and press **`<shift>+n`**. The associated note will be 
displayed for reading or editing. All notes are in the current directory in a new 
`.notes` subdirectory. The name for the note file associated with a directory or 
file is that directory or file name with the `.md` extension.

If you have the [Open With Editor](https://github.com/raguay/OpenWithEditor) plugin installed and configured, then this 
plugin will use the editor your select with that plugin to edit the notes file.
Otherwise, it will use the fman edit command to edit the file.

### Features

 - Attach notes to files and directories.
