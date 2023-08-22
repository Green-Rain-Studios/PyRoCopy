# PyRoCopy

PyRoCopy is a Python-based GUI frontend for the Robocopy command-line utility. It provides an easy-to-use interface for performing file copy operations with various options.

## Features

- Easy-to-use graphical interface for Robocopy.
- Supports all major Robocopy options like mirroring directories, copying all file info, moving files, and copying in restartable mode.
- Allows you to choose the number of CPU threads to use for the copy operation.
- Provides a text area to display the output of the Robocopy operation.

## Usage

1. Download or clone this repository.
2. Run `run.bat` to run the tool. It will automatically install any relevant modules if python is installed.
3. In the PyRoCopy window, enter the source and destination directories for the copy operation.
4. Choose the desired Robocopy option from the dropdown menu.
5. Choose the number of CPU threads to use from the dropdown menu.
6. Click the "Run Robocopy" button to start the copy operation.

## Requirements

- Python 3.6 or later
- tkinter
- subprocess
- threading

## Contributing

Contributions to PyRoCopy are welcome!

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.
