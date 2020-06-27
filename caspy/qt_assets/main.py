from pyperclip import copy
import json

from Worker import CASWorker

from qt_assets.tabs import (
    DerivativeTab,
    IntegralTab,
    LimitTab,
    SimplifyTab,
    ExpandTab,
    EvaluateTab,
    PfTab,
    WebTab,
    ShellTab
)

from PyQt5.QtCore import (
    QCoreApplication,
    QThreadPool,
)

from PyQt5.QtWidgets import (
    QApplication,
    QInputDialog,
    QMainWindow,
    QMessageBox
)

from PyQt5.uic import loadUi

class CASpyGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        with open("assets/formulas.json", "r", encoding="utf8") as json_f:
            self.json_data = json_f.read()
            self.json_file = json.loads(self.json_data)

        self.exact_ans = ""
        self.approx_ans = ""

        self.use_unicode = False
        self.line_wrap = False
        self.use_scientific = False
        self.accuracy = 10

        self.threadpool = QThreadPool()

        self.TABS = [DerivativeTab, IntegralTab, LimitTab, SimplifyTab, ExpandTab, EvaluateTab, PfTab, WebTab, ShellTab]

        self.init_ui()

    def init_ui(self):
        loadUi('qt_assets/main.ui', self)
        self.init_menu()
        self.init_tabs()
        self.show()

    def init_menu(self):
        action_bindings = {
            'actionUnicode': self.toggle_unicode,
            'actionLinewrap': self.toggle_line_wrap,
            'actionScientific_Notation': self.toggle_use_scientific,
            'actionAccuracy': self.change_accuracy,
            'actionCopy_Exact_Answer': self.copy_exact_ans,
            'actionCopy_Approximate_Answer': self.copy_approx_ans,
            'actionNext_Tab': self.next_tab,
            'actionPrevious_Tab': self.previous_tab
        }

        for action in self.menuSettings.actions() + self.menuCopy.actions() + self.menuTab.actions():
            if action.objectName() in action_bindings.keys():
                action.triggered.connect(action_bindings[action.objectName()])

    def init_tabs(self):
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

    def get_scientific_notation(self):
        number, confirmed = QInputDialog.getInt(self, "Get Scientific Notation", "Enter the accuracy for scientific notation", 5, 1, 999999, 1)
        if confirmed:
            self.use_scientific = number

    def get_accuracy(self):
        number, confirmed = QInputDialog.getInt(self, "Get Accuracy", "Enter the accuracy for evaluation", self.accuracy, 1, 999999, 1)
        if confirmed:
            self.accuracy = number

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
        # Toggles scientific notation, only works when calculating an approximation
        _translate = QCoreApplication.translate
        if state:
            self.get_scientific_notation()
            self.actionScientific_Notation.setText(_translate("MainWindow", f"Scientific Notation - {self.use_scientific}"))
        else:
            self.use_scientific = False
            self.actionScientific_Notation.setText(_translate("MainWindow", "Scientific Notation"))

    def change_accuracy(self, state):
        _translate = QCoreApplication.translate
        if state:
            self.get_accuracy()
            self.actionAccuracy.setText(_translate("MainWindow", f"Accuracy - {self.accuracy}"))
        else:
            self.actionAccuracy.setText(_translate("MainWindow", "Accuracy"))

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

def launch_app():
    import sys
    app = QApplication(sys.argv)
    caspy = CASpyGUI()
    sys.exit(app.exec_())