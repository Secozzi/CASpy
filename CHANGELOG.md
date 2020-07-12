# Changelog

All changes will be documented in this file

## [2.0] - TBA (Not released yet)

### Added

- Added windows to remove and add websites
- Added splitters in each tab
- Added 'view' to view the exact  or approximate answer in a separate window
- Added CHANGELOG.md
- Added option to type in equation with equals sign in left expression

### Changed

- Massive overhaul of structure. Each tab is defined as a separate class that loads its ui from a .ui file. This makes it much easier to add, remove or change individual tabs. The class of each tab handles everything from adding special menu bar actions to eventfilters
- Output type is now located in the menu instead of a group of radiobuttons in each tab
- CAS.py has been removed and is replaced by qt_assets/main.py
- qt_gui.py's only purpose is now to call the launch_app() function imported from qt_assets/main.py
- The textbrowser that holds the approximate answer has been enlarged vertically.
- Prime Factor tab has now two text browsers. One for displaying as a dict and for displaying as a string
- Wordwrap on the text browser that displays the exact answer has been disabled and is instead enabled on view -> view exact answer
- Settings -> Accuracy is no longer checkable and always displays accuracy
- Each tab is now split into a separate .py file. This adds around 11 ms to start but it makes it way easier to manage
- Eventfilters are now installed on the tab, not on the QPlainTextEdit

### Fixed

- Inconsistencies in the ui has been fixed
- Fixed a bug where shell clear wouldn't remove the list of previously executed commands
- Fixed bug where application would detect, but still crash when trying to preview or calculate even though a formulas wasn't selected

## [1.2.1] - 2020-06-12

### Fixed

- Removed unnecessary `print()` statements

## [1.2] - 2020-06-12

### Fixed

- `-c` option for CLI now works

## [1.1] - 2020-06-12

### Added

- Added option `-a` for accuracy both for CLI and GUI
- Added CLI option `-c` for copying the results
- Added logo for GUI

### Changed

- Improved overall structure of project
- Changed license from MIT to GPLv3+

## [1.0.2] - 2020-05-31

### Changed

- Desmos changed from a html file to the official url.

## [1.0.1] - 2020-05-31

### Fixed

- cli.py can now read `formulas.json`