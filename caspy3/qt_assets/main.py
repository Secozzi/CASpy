#
#    CASPy - A program that provides both a GUI and a CLI to SymPy.
#    Copyright (C) 2020 Folke Ishii
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

from pyperclip import copy
import json
import os
import pkg_resources

import typing as ty

from .dialogs.tab_list import TabList

from .tabs import TABS
from PyQt5.QtCore import QCoreApplication, QThreadPool, pyqtSlot
from PyQt5.QtGui import QKeySequence

from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QApplication,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QShortcut,
    QTabWidget,
    QWidget,
)

from PyQt5.QtGui import QCloseEvent
from PyQt5.uic import loadUi


class CASpyGUI(QMainWindow):
    def __init__(self) -> None:
        """
        The main window.

        formulas.json is loaded and every variable + the threadpool is initialized.
        self.TABS includes every tab to be loaded from qt_assets. This list is later iterated through and each tab is added to the tab manager
        Every QAction gets the corresponding function assigned when triggered.
        """
        super().__init__()

        # Load json file, call individual function(s) to reload data
        self.load_jsons()

        # Initialize variables
        self.exact_ans = ""
        self.approx_ans = ""
        self.latex_text = ""

        # Load settings from settings.json
        self.output_type = self.settings_data["output"]
        self.use_unicode = self.settings_data["unicode"]
        self.line_wrap = self.settings_data["linewrap"]
        self.use_scientific = self.settings_data["scientific"]
        self.accuracy = self.settings_data["accuracy"]
        self.use_latex = self.settings_data["use_latex"]
        self.latex_fs = self.settings_data["latex_fs"]
        self.save_settings_data = {}

        # Start threadppol
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)

        # Define tabs used
        self.TABS: ty.List[QWidget] = TABS

        # Initialize ui
        self.init_ui()
        self.init_shortcuts()

    @staticmethod
    def get_resource_path(relative_path: str) -> str:
        return pkg_resources.resource_filename("caspy3", relative_path)

    def load_jsons(self) -> None:
        # Load each json_file
        self.load_settings()
        self.load_websites()
        self.load_formulas()

    def load_settings(self) -> None:
        with open(
            self.get_resource_path("data/settings.json"), "r", encoding="utf8"
        ) as json_f:
            _settings_file = json_f.read()
            self.settings_data = json.loads(_settings_file)

    def load_websites(self) -> None:
        with open(
            self.get_resource_path("data/websites.json"), "r", encoding="utf8"
        ) as json_f:
            _websites_file = json_f.read()
            self.websites_data = json.loads(_websites_file)

    def load_formulas(self) -> None:
        with open(
            self.get_resource_path("data/formulas.json"), "r", encoding="utf8"
        ) as json_f:
            _formulas_file = json_f.read()
            self.formulas_data = json.loads(_formulas_file)

    def init_ui(self) -> None:
        """Load ui file, then initialize menu, and then initalize all tabs"""
        loadUi(self.get_resource_path("qt_assets/main.ui"), self)

        # For displaying icon in taskbar
        try:
            if os.name == "nt":
                import ctypes

                myappid = "secozzi.caspy3.220"
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        self.init_menu()
        self.init_tabs()
        self.show()

    def init_menu(self) -> None:
        """For the QActionGroup Output Type -> Pretty - Latex - Normal.
        This couldn't be done in Qt Designer since AFAIK it doesn't support QActionGroup."""
        self.output_type_group = QActionGroup(self.menuOutput_Type)
        self.output_type_group.addAction(self.actionPretty)
        self.output_type_group.addAction(self.actionLatex)
        self.output_type_group.addAction(self.actionNormal)
        self.output_type_group.setExclusive(True)
        self.output_type_group.triggered.connect(self.change_output_type)

        # QAction and its corresponding function when triggered
        action_bindings = {
            "actionUnicode": self.toggle_unicode,
            "actionLinewrap": self.toggle_line_wrap,
            "actionScientific_Notation": self.toggle_use_scientific,
            "actionAccuracy": self.change_accuracy,
            "actionTab_List": self.open_tab_list,
            "actionCopy_Exact_Answer": self.copy_exact_ans,
            "actionCopy_Approximate_Answer": self.copy_approx_ans,
            "actionNext_Tab": self.next_tab,
            "actionPrevious_Tab": self.previous_tab,
            "actionLatexFs": self.change_latex_fs,
            "actionUseLatex": self.toggle_use_latex,
        }

        checkable_actions = {
            "actionUseLatex": self.use_latex,
            "actionUnicode": self.use_unicode,
            "actionLinewrap": self.line_wrap,
        }

        # Assign function to QAction when triggered
        for action in (
            self.menuSettings.actions()
            + self.menuCopy.actions()
            + self.menuTab.actions()
        ):
            object_name = action.objectName()

            if object_name in action_bindings.keys():
                action.triggered.connect(action_bindings[object_name])

            if object_name in checkable_actions.keys():
                if checkable_actions[object_name]:
                    action.setChecked(True)

        _translate = QCoreApplication.translate
        if self.use_scientific:
            self.actionScientific_Notation.setText(
                _translate("MainWindow", f"Scientific Notation - {self.use_scientific}")
            )

        self.actionAccuracy.setText(
            _translate("MainWindow", f"Accuracy - {self.accuracy}")
        )
        self.actionLatexFs.setText(
            _translate("MainWindow", f"LaTeX font-size - {self.latex_fs}")
        )

        if self.output_type == 1:
            self.actionPretty.setChecked(True)
        elif self.output_type == 2:
            self.actionLatex.setChecked(True)
        else:
            self.actionNormal.setChecked(True)

    def init_tabs(self) -> None:
        """
        Iterate through self.TABS and add the tab to tab_manager and pass self as main_window
        """
        self.tab_manager: QTabWidget
        self.tab_manager.clear()
        for tab in self.TABS:
            tab: "sip.wrappertype"
            self.tab_manager.addTab(tab(main_window=self), tab.display_name)

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

    def change_output_type(self, action: QAction) -> None:
        # Pretty is represented as a 1, Latex 2, and Normal 3
        types = ["Pretty", "Latex", "Normal"]
        self.output_type = types.index(action.text()) + 1

    def get_scientific_notation(self) -> ty.Union[int, None]:
        # Get accuracy of scientific notation with QInputDialog
        number, confirmed = QInputDialog.getInt(
            self,
            "Get Scientific Notation",
            "Enter the accuracy for scientific notation",
            5,
            1,
            999999,
            1,
        )
        if confirmed:
            return number
        else:
            return None

    def get_accuracy(self) -> None:
        # Get accuracy with QInputDialog
        number, confirmed = QInputDialog.getInt(
            self,
            "Get Accuracy",
            "Enter the accuracy for evaluation",
            self.accuracy,
            1,
            999999,
            1,
        )
        if confirmed:
            self.accuracy = number

    def open_tab_list(self) -> None:
        self.tab_list = TabList(self)

    def toggle_unicode(self, state: bool) -> None:
        # Toggles whether or not to use unicode.
        if state:
            self.use_unicode = True
        else:
            self.use_unicode = False

    def toggle_line_wrap(self, state: bool) -> None:
        # Toggles whether or not to wrap lines.
        if state:
            self.line_wrap = True
        else:
            self.line_wrap = False

    def toggle_use_scientific(self, state: bool) -> None:
        # Toggles the use of scientific notation (and accuracy), only works when calculating an approximation
        _translate = QCoreApplication.translate
        if state:
            self.use_scientific = self.get_scientific_notation()
            if self.use_scientific:
                self.actionScientific_Notation.setText(
                    _translate(
                        "MainWindow", f"Scientific Notation - {self.use_scientific}"
                    )
                )
            else:
                self.actionScientific_Notation.setChecked(False)
                self.actionScientific_Notation.setText(
                    _translate("MainWindow", "Scientific Notation")
                )
        else:
            self.use_scientific = False
            self.actionScientific_Notation.setText(
                _translate("MainWindow", "Scientific Notation")
            )

    def toggle_use_latex(self, state: bool) -> None:
        if state:
            self.use_latex = True
        else:
            self.use_latex = False

    def get_latex_fs(self) -> None:
        # Get LaTeX resolution with QInputDialog
        number, confirmed = QInputDialog.getInt(
            self,
            "LaTex Resolution",
            "Enter font-size for LaTeX renderer. Higher font-size equals greater resolution",
            self.latex_fs,
            1,
            999999,
            1,
        )
        if confirmed:
            self.latex_fs = number

    def change_latex_fs(self) -> None:
        _translate = QCoreApplication.translate
        self.get_latex_fs()
        self.actionAccuracy.setText(
            _translate("MainWindow", f"Accuracy - {self.accuracy}")
        )

    def change_accuracy(self) -> None:
        # Changes accuracy of all evaluations
        _translate = QCoreApplication.translate
        self.get_accuracy()
        self.actionAccuracy.setText(
            _translate("MainWindow", f"Accuracy - {self.accuracy}")
        )

    def copy_exact_ans(self) -> None:
        # Copies self.exact_ans to clipboard.
        if type(self.exact_ans) == list:
            if len(self.exact_ans) == 1:
                copy(str(self.exact_ans[0]))
        else:
            copy(str(self.exact_ans))

        if self.tab_manager.currentWidget().eout:
            self.tab_manager.currentWidget().eout.selectAll()

    def copy_approx_ans(self) -> None:
        # Copies self.approx_ans to clipboard.
        if type(self.approx_ans) == list:
            if len(self.approx_ans) == 1:
                copy(str(self.approx_ans[0]))
        else:
            copy(str(self.approx_ans))

        if self.tab_manager.currentWidget().aout:
            self.tab_manager.currentWidget().aout.selectAll()

    def next_tab(self) -> None:
        # Goes to next tab.
        if self.tab_manager.currentIndex() == self.tab_manager.count() - 1:
            self.tab_manager.setCurrentIndex(0)
        else:
            self.tab_manager.setCurrentIndex(self.tab_manager.currentIndex() + 1)

    def previous_tab(self) -> None:
        # Goes to previous tab.
        if self.tab_manager.currentIndex() == 0:
            self.tab_manager.setCurrentIndex(self.tab_manager.count() - 1)
        else:
            self.tab_manager.setCurrentIndex(self.tab_manager.currentIndex() - 1)

    def add_to_save_settings(self, data: dict) -> None:
        """
        Function that a tab calls to add data to be saved when closing the window.
        The tab calls this function on init() and every time the data changes.
        :param data: dict
            Dict that holds data
        """
        for key in data:
            self.save_settings_data[key] = data[key]

    def update_save_settings(self, data: dict) -> None:
        """
        Update the dict the saves all data
        :param data: dict
            entry to update
        """
        self.save_settings_data.update(data)

    def init_shortcuts(self) -> None:
        # I don't like this
        self._s1 = QShortcut(QKeySequence("Alt+1"), self)
        self._s2 = QShortcut(QKeySequence("Alt+2"), self)
        self._s3 = QShortcut(QKeySequence("Alt+3"), self)
        self._s4 = QShortcut(QKeySequence("Alt+4"), self)
        self._s5 = QShortcut(QKeySequence("Alt+5"), self)
        self._s6 = QShortcut(QKeySequence("Alt+6"), self)
        self._s7 = QShortcut(QKeySequence("Alt+7"), self)
        self._s8 = QShortcut(QKeySequence("Alt+8"), self)
        self._s9 = QShortcut(QKeySequence("Alt+9"), self)

        self._s1.activated.connect(lambda: self.goto_tab(1))
        self._s2.activated.connect(lambda: self.goto_tab(2))
        self._s3.activated.connect(lambda: self.goto_tab(3))
        self._s4.activated.connect(lambda: self.goto_tab(4))
        self._s5.activated.connect(lambda: self.goto_tab(5))
        self._s6.activated.connect(lambda: self.goto_tab(6))
        self._s7.activated.connect(lambda: self.goto_tab(7))
        self._s8.activated.connect(lambda: self.goto_tab(8))
        self._s9.activated.connect(lambda: self.goto_tab(9))

    @pyqtSlot()
    def goto_tab(self, tab: int) -> None:
        if tab <= self.tab_manager.count():
            self.tab_manager.setCurrentIndex(tab-1)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Save settings when closing window by writing dict to json file
        """
        settings_json = {
            "tabs": self.settings_data["tabs"],
            "unicode": self.use_unicode,
            "linewrap": self.line_wrap,
            "output": self.output_type,
            "scientific": self.use_scientific,
            "accuracy": self.accuracy,
            "use_latex": self.use_latex,
            "latex_fs": self.latex_fs
        }

        # Going through each tab
        for i in range(self.tab_manager.count()):
            tab: QWidget = self.tab_manager.widget(i)
            if tab.objectName() == "ShellTab":  # Shut down kernal
                tab.jupyter_widget.kernel_client.stop_channels()
                tab.jupyter_widget.kernel_manager.shutdown_kernel()

        # add data called from add_to_save_settings()
        for key in list(self.save_settings_data.keys()):
            settings_json[key] = self.save_settings_data[key]

        with open(
            self.get_resource_path("data/settings.json"), "w", encoding="utf-8"
        ) as json_f:
            json.dump(
                settings_json, json_f, ensure_ascii=False, indent=4, sort_keys=False
            )

        event.accept()


def launch_app() -> None:
    import sys

    app = QApplication(sys.argv)
    caspy = CASpyGUI()
    sys.exit(app.exec_())
