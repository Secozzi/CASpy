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
from pkg_resources import resource_filename

# PyQt5
from PyQt5.QtCore import QSettings, QThreadPool
from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QApplication,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QWidget,
)
from PyQt5.uic import loadUi

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

        self.init_ui()

    @staticmethod
    def get_resource(relative_path: str) -> str:
        """
        Returns path to a file relative to source directory (CASPy/caspy3)
        """
        return resource_filename("caspy3", relative_path)

    @staticmethod
    def show_error_box(message: str) -> None:
        """
        Show a message box containing an error

        :param message: str
            The message that is to be displayed by the message box
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def init_ui(self) -> None:
        # Load ui
        loadUi(self.get_resource("qt_assets/app/mainwindow.ui"), self)

        # Displaying icon in taskbar
        try:
            from PyQt5.QtWinExtras import QtWin
            from caspy3 import version

            my_app_id = f"secozzi.caspy3.{''.join(map(str, version))}"
            QtWin.setCurrentProcessExplicitAppUserModelID(my_app_id)
        except ImportError:
            pass

        self.init_menu()
        self.init_tabs()

    def init_menu(self) -> None:
        """
        Initialize menu and add bindings to actions
        """
        # For the QActionGroup Output Type -> Pretty - Latex - Normal
        self.output_type_group = QActionGroup(self.menuOutput_Type)
        self.output_type_group.addAction(self.actionPretty)
        self.output_type_group.addAction(self.actionLatex)
        self.output_type_group.addAction(self.actionNormal)
        self.output_type_group.setExclusive(True)
        self.output_type_group.triggered.connect(self.change_output_type)

        # Object name of QAction and function to call when triggered
        action_bindings = {}

        # Actions that are also checkable
        checkable_actions = {}

    def change_output_type(self, action: QAction) -> None:
        ...

    def init_tabs(self) -> None:
        ...
