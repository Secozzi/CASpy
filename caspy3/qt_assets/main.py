from pyperclip import copy
import json, os

from qt_assets.dialogs.dialog_view import View
from qt_assets.dialogs.dialog_view_text import View_Text
from qt_assets.dialogs.tab_list import TabList

from qt_assets.tabs import TABS
from PyQt5.QtCore import (
    QCoreApplication,
    QSize,
    QThreadPool
)

from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QApplication,
    QDialog,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QTextBrowser
)

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont, QIcon
from PyQt5.uic import loadUi

class CASpyGUI(QMainWindow):
    def __init__(self):
        """"""

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
        self.save_settings_data = {}

        # Start threadppol
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)

        # Define tabs used
        self.TABS = TABS

        # Initialize ui
        self.init_ui()

    def load_jsons(self):
        # Load each json_file
        self.load_settings()
        self.load_websites()
        self.load_formulas()

    def load_settings(self):
        # Loads settings
        with open("data/settings.json", "r", encoding="utf8") as json_f:
            self.settings_file = json_f.read()
            self.settings_data = json.loads(self.settings_file)

    def load_websites(self):
        with open("data/websites.json", "r", encoding="utf8") as json_f:
            self.websites_file = json_f.read()
            self.websites_data = json.loads(self.websites_file)

    def load_formulas(self):
        with open("data/formulas.json", "r", encoding="utf8") as json_f:
            self.formulas_file = json_f.read()
            self.formulas_data = json.loads(self.formulas_file)

    def init_ui(self):
        """Load ui file, then initialize menu, and then initalize all tabs"""
        loadUi('qt_assets/main.ui', self)

        # For displaying icon in taskbar
        try:
            if os.name == "nt":
                import ctypes
                myappid = u'secozzi.caspy3.200'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        self.init_menu()
        self.init_tabs()
        self.show()

    def init_menu(self):
        """For the QActionGroup Output Type -> Pretty - Latex - Normal.
        This couldn't be done in Qt Designer since it doesn't support QActionGroup."""
        self.output_type_group = QActionGroup(self.menuOutput_Type)
        self.output_type_group.addAction(self.actionPretty)
        self.output_type_group.addAction(self.actionLatex)
        self.output_type_group.addAction(self.actionNormal)
        self.output_type_group.setExclusive(True)
        self.output_type_group.triggered.connect(self.change_output_type)

        # QAction and its corresponding function when triggered
        action_bindings = {
            'actionUnicode': self.toggle_unicode,
            'actionLinewrap': self.toggle_line_wrap,
            'actionScientific_Notation': self.toggle_use_scientific,
            'actionAccuracy': self.change_accuracy,
            'actionTab_List': self.open_tab_list,
            'actionCopy_Exact_Answer': self.copy_exact_ans,
            'actionCopy_Approximate_Answer': self.copy_approx_ans,
            'actionNext_Tab': self.next_tab,
            'actionPrevious_Tab': self.previous_tab,
            'actionExact_Answer': self.view_exact_ans,
            'actionApproximate_Answer': self.view_approx_ans
        }

        checkable_actions = {
            'actionUnicode': self.use_unicode,
            'actionLinewrap': self.line_wrap
        }

        # Assign function to QAction when triggered
        for action in self.menuSettings.actions() + self.menuCopy.actions() + self.menuTab.actions() + self.menuView.actions():
            object_name = action.objectName()

            if object_name in action_bindings.keys():
                action.triggered.connect(action_bindings[object_name])

            if object_name in checkable_actions.keys():
                if checkable_actions[object_name]:
                    action.setChecked(True)

        _translate = QCoreApplication.translate
        if self.use_scientific:
            self.actionScientific_Notation.setText(_translate("MainWindow", f"Scientific Notation - {self.use_scientific}"))

        self.actionAccuracy.setText(_translate("MainWindow", f"Accuracy - {self.accuracy}"))

        if self.output_type == 1:
            self.actionPretty.setChecked(True)
        elif self.output_type == 2:
            self.actionLatex.setChecked(True)
        else:
            self.actionNormal.setChecked(True)

    def init_tabs(self):
        """
        Iterate through self.TABS and add the tab to tab_manager and pass self as main_window
        """
        self.tab_manager.clear()
        for tab in self.TABS:
            self.tab_manager.addTab(tab(main_window=self), tab.display_name)

    def show_error_box(self, message):
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

    def change_output_type(self, action):
        # Pretty is represented as a 1, Latex 2, and Normal 3
        types = ["Pretty", "Latex", "Normal"]
        self.output_type = types.index(action.text()) + 1

    def get_scientific_notation(self):
        # Get accuracy of scientific notation with QInputDialog
        number, confirmed = QInputDialog.getInt(self, "Get Scientific Notation", "Enter the accuracy for scientific notation", 5, 1, 999999, 1)
        if confirmed:
            return number
        else:
            return False

    def get_accuracy(self):
        # Get accuracy with QInputDialog
        number, confirmed = QInputDialog.getInt(self, "Get Accuracy", "Enter the accuracy for evaluation", self.accuracy, 1, 999999, 1)
        if confirmed:
            self.accuracy = number

    def open_tab_list(self):
        self.tab_list = TabList(self)

    def toggle_unicode(self, state):
        # Toggles whether or not to use unicode.
        if state:
            self.use_unicode = True
        else:
            self.use_unicode = False

    def toggle_line_wrap(self, state):
        # Toggles whether or not to wrap lines.
        if state:
            self.line_wrap = True
        else:
            self.line_wrap = False

    def toggle_use_scientific(self, state):
        # Toggles the use of scientific notation (and accuracy), only works when calculating an approximation
        _translate = QCoreApplication.translate
        if state:
            self.use_scientific = self.get_scientific_notation()
            if self.use_scientific:
                self.actionScientific_Notation.setText(_translate("MainWindow", f"Scientific Notation - {self.use_scientific}"))
            else:
                self.actionScientific_Notation.setChecked(False)
                self.actionScientific_Notation.setText(_translate("MainWindow", "Scientific Notation"))
        else:
            self.use_scientific = False
            self.actionScientific_Notation.setText(_translate("MainWindow", "Scientific Notation"))

    def change_accuracy(self):
        # Changes accuracy of all evaluations
        _translate = QCoreApplication.translate
        self.get_accuracy()
        self.actionAccuracy.setText(_translate("MainWindow", f"Accuracy - {self.accuracy}"))

    def copy_exact_ans(self):
        # Copies self.exact_ans to clipboard.
        if type(self.exact_ans) == list:
            if len(self.exact_ans) == 1:
                copy(str(self.exact_ans[0]))
        else:
            copy(str(self.exact_ans))

    def copy_approx_ans(self):
        # Copies self.approx_ans to clipboard.
        if type(self.approx_ans) == list:
            if len(self.approx_ans) == 1:
                copy(str(self.approx_ans[0]))
        else:
            copy(str(self.approx_ans))

    def next_tab(self):
        # Goes to next tab.
        if self.tab_manager.currentIndex() == 10:
            self.tab_manager.setCurrentIndex(0)
        else:
            self.tab_manager.setCurrentIndex(self.tab_manager.currentIndex() + 1)

    def previous_tab(self):
        # Goes to previous tab.
        if self.tab_manager.currentIndex() == 0:
            self.tab_manager.setCurrentIndex(10)
        else:
            self.tab_manager.setCurrentIndex(self.tab_manager.currentIndex() - 1)

    def view_exact_ans(self):
        # Open QDialog with exact answer
        self.v = View(str(self.exact_ans), self.latex_text)

    def view_approx_ans(self):
        # Open QDialog with approximate answer
        self.v = View_Text(str(self.approx_ans))

    def add_to_save_settings(self, data):
        """
        Function that a tab calls to add data to be saved when closing the window.
        The tab calls this function on init() and every time the data changes.
        :param data: dict
            Dict that holds data
        """
        for key in list(data.keys()):
            self.save_settings_data[key] = data[key]

    def update_save_settings(self, data):
        """
        Update the dict the saves all data
        :param data: dict
            entry to update
        """
        self.save_settings_data.update(data)

    def closeEvent(self, event):
        """
        Save settings when closing window by writing dict to json file
        """
        settings_json = {
            "tabs": self.settings_data["tabs"],
            "unicode": self.use_unicode,
            "linewrap": self.line_wrap,
            "output": self.output_type,
            "scientific": self.use_scientific,
            "accuracy": self.accuracy
        }

        # add data called from add_to_save_settings()
        for key in list(self.save_settings_data.keys()):
            settings_json[key] = self.save_settings_data[key]

        with open("data/settings.json", "w", encoding="utf-8") as json_f:
            json.dump(settings_json, json_f, ensure_ascii=False, indent=4, sort_keys=False)

        event.accept()

def launch_app():
    import sys
    app = QApplication(sys.argv)
    caspy = CASpyGUI()
    sys.exit(app.exec_())