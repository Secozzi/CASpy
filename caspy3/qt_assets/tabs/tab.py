#
#    CASPy - A program that provides both a GUI and a CLI to SymPy.
#    Copyright (C) 2021 Folke Ishii
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

# Standard library
import typing as ty

# PyQt5
from PyQt5.QtWidgets import QWidget

# Relative
if ty.TYPE_CHECKING:
    from caspy3.qt_assets.app.mainwindow import MainWindow


class CaspyTab(QWidget):
    def __init__(self, main_window: "MainWindow", name: str) -> None:
        super().__init__()
        self.main_window = main_window
        self.main_window.qapp.aboutToQuit.connect(self.close_event)
        self.setFont(self.main_window.tabs_font)

    def update_ui(self, input_dict) -> None: ...
    def stop_thread(self) -> None: ...
    def set_splitters(self) -> None:
        if self.splitter:
            ...