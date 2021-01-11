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

# Third party
import sympy as sy

# PyQt5
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

# Relative
# TODO: Worker
if ty.TYPE_CHECKING:
    from caspy3.qt_assets.app.mainwindow import MainWindow


class DerivativeTab(QWidget):

    display_name = "Derivative"

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()
        self.main_window = main_window