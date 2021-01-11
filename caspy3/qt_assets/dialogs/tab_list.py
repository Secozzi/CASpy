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
from typing import TYPE_CHECKING
import sys

# PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem
from PyQt5.QtGui import QCloseEvent, QIcon

# Relative
if TYPE_CHECKING:
    from caspy3.qt_assets.app.mainwindow import MainWindow


class TabList(QListWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super(TabList, self).__init__()
        self.main_window = main_window

        # Initialize Ui
        self.setFixedHeight(340)
        self.setWindowTitle("CASPy tab list")
        self.setWindowIcon(QIcon(self.main_window.get_resource("images/logo.png")))
        self.setToolTip("Settings take effect after restart")
        self.setWindowModality(Qt.ApplicationModal)

        self.setAlternatingRowColors(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDragDropOverwriteMode(False)

        self.main_window.settings.beginGroup("mainwindow")
        # TODO: Fill tab
        self.tab_list = self.main_window.settings.value("tab_list", [2, 3], list)
        self.main_window.settings.endGroup()

        print(self.tab_list)

        self.show()

    def str_to_class(self, classname: str) -> "sip.wrappertype":
        """Returns tab widget from the tab's class name"""
        return getattr(sys.modules[__name__], classname)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.main_window.settings.beginGroup("mainwindow")
        self.main_window.settings.setValue("tab_list", self.tab_list)
        self.main_window.settings.endGroup()

        event.accept()
