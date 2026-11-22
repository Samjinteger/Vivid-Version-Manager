# Vivid Version Manager (VVM)

A small version manager for **vivid/stasis** (a rhythm game with a visual novel and ARG elements), built with Python and Tkinter.

VVM lets you manage multiple installations of vivid/stasis, launch different game versions, and keep their save data separate.

Download the game here (it's free!): https://store.steampowered.com/app/2093940/vividstasis/ 

## Features

- **Version management** – Register and manage multiple vivid/stasis installations.
- **Launch different versions** – Select an installation and launch it directly from VVM.
- **Separate save profiles** – Keep save data independent between game versions.
- **Automatic save switching** – VVM backs up the current save and switches to the selected version's profile before launching.
- **Save backups** – Create backups of your active save data.

## Requirements

- Windows*
- Python 3.14 or later*
- A valid vivid/stasis installation

*Note: Only tested on Windows 11 Pro. Issues may occur on other versions.

**Note: Only tested on Python 3.14. Issues may occur on other versions.

## Dependencies

VVM uses the following external Python packages:

Pillow (https://pypi.org/project/pillow/) – Image processing and icon display.

icoextract (https://pypi.org/project/icoextract/) – Extracting icons from Windows executables.

## Getting started

1. Clone this repository:
   ```bash
   git clone https://github.com/Samjinteger/VividVersionManager.git
   ```
2. Navigate into the project directory:
   ```bash
   cd VividVersionManager
   ```
3. Create and activate your .venv (not needed but recommended):
   ```bash
   py -3.14 -m venv .venv
   .venv/Scripts/activate
4. Install depedencies:
   ```bash
   python -m pip install Pillow icoextract
5. Run the application:
   ```bash
   python main.py
   ```

## Known issues

- Steam Cloud needs to be set OFF for vivid/stasis for the app to work correctly.
- The 'Add version' window opens behind other windows if not opened through the 'Add version' button in the main window.
- The data/ folder is excluded from the source code, since it contains local settings, save profiles and backups, which are user data.

## To-do list

to-do

## Project status

VVM is currently a work in progress. Features and the interface are still being developed, and breaking changes may occur.

VVM is a hobby project. No kind of profit is being made out of this, and I am not seeking any monetary value either.

## Disclaimer

Vivid Version Manager is an independent, community-made project and is not affiliated with or endorsed by the developers of vivid/stasis.

I am not responsible for any problems that may occur as a result of this software; it has been designed with only my usage in mind.

Use at your own risk. Always keep backups of your save data. I am not responsible for any data loss.

## License

This project is licensed under the MIT License.
See the (LICENSE) file for details.
