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
import os

# PyQt5
from PyQt5.QtCore import QSettings, QThreadPool
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

# Relative
from caspy3.qt_assets.tabs import get_tabs


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # Initalize variables
        self.approx_ans = ""
        self.exact_ans = ""
        self.latex_ans = ""

        # Qt specific variables
        self.settings = QSettings("Secozzi", "CASPy")
        self.qapp = QApplication.instance()
        self.threadpool = QThreadPool()
        self.tab_list: ty.List[QWidget]
