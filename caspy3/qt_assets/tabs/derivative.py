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
from caspy3.qt_assets.tabs.tab import CaspyTab
# TODO: Worker
if ty.TYPE_CHECKING:
    from caspy3.qt_assets.app.mainwindow import MainWindow


class DerivativeTab(CaspyTab):

    display_name = "Derivative"
    name = "derivative"

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window, self.name)
        loadUi(self.main_window.get_resource("qt_assets/tabs/derivative.ui"), self)

        self.eout = self.textEdit
        self.aout = None
        self.splitter = None

    def close_event(self) -> None:
        print("CLOSING DERIVATIVE")