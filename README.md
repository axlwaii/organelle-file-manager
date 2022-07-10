# Organelle File Manager

A simple file manager to directly browse, copy/paste or delete files on the Critter & Guitari Organelle.

## Install

1. Create the folder inside `System` on the Organelles SD card with the name `File manager`.
2. Copy the files `main.py` and `og.py` into the `File manager` folder.
3. In the Organelle menu go to `System` -> `File manager` to start.

## Actions

To open the available options press the main knob on the file you would like to perfom an action.

### Browse

Turning the main knob let you select files or folders. Pressing the knob on a folder will enter the folder.
Selecting `../` will bring you to the previous folder.

### Delete

**Caution**: Files are deleted permanentely and can not be restored. Only files can be deleted.

1. Browse to the file you would like to delete.
2. Press the main knob and select `Delete`.
3. Confirm the file to be permanentely deleted.

### Copy & Paste

**Copy**

1. Browse to the file you would like to copy.
2. Press the main knob and select `Copy`.
3. The file has been copied and you'll see the folder structure again

**Paste file to folder**

1. Each folder will now have a `/` menu entry which represents the folders root.
2. Choose `/` with the main knob and then select paste
3. Confirm the file to be copied to the selected folder.

**Overwrite an existing file**

1. Browse to the file you would like to replace.
2. Press the main know and select `Paste`.
3. Confirm the copied file to overwrite the selected file

**Rename**

Only `wav` files can be renamed for now.

1. Browse to the audio file you would like to rename.
2. Press the main knob and select `Rename`.
3. Select the new file name (1.wav - 24.wav) and confirm your selection

## Version History:

1.1 - Added rename function
1.0 – Initial Release. April 17 2022

## License

The MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
