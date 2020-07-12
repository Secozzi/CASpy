from pyperclip import copy
import json, os

from worker import CASWorker

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

        # Define tabs used
        self.TABS = TABS

        # Initialize ui
        self.init_ui()

    def load_jsons(self):
        self.load_settings()
        self.load_websites()
        self.load_formulas()

    def load_settings(self):
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
        # Load ui file, then initialize menu and then initalize all tabs
        loadUi('qt_assets/main.ui', self)

        # For displaying in taskbar
        if os.name == "nt":
            import ctypes
            myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.init_menu()
        self.init_tabs()
        self.show()

    def init_menu(self):
        # For the QActionGroup Output Type -> Pretty - Latex - Normal. This couldn't be done in Qt Designer since it doesn't support QActionGroup.
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
            self.use_scientific = number

    def get_accuracy(self):
        # Get accuracy with QInputDialog
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
        # Toggles the use of scientific notation (and accuracy), only works when calculating an approximation
        _translate = QCoreApplication.translate
        if state:
            self.get_scientific_notation()
            self.actionScientific_Notation.setText(_translate("MainWindow", f"Scientific Notation - {self.use_scientific}"))
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
        for key in list(data.keys()):
            self.save_settings_data[key] = data[key]

    def closeEvent(self, event):
        """
        Save settings when closing window
        """
        settings_json = {
            "unicode": self.use_unicode,
            "linewrap": self.line_wrap,
            "output": self.output_type,
            "scientific": self.use_scientific,
            "accuracy": self.accuracy
        }

        for key in list(self.save_settings_data.keys()):
            settings_json[key] = self.save_settings_data[key]

        with open("data/settings.json", "w", encoding="utf-8") as json_f:
            json.dump(settings_json, json_f, ensure_ascii=False, indent=4, sort_keys=False)

        event.accept()

class View(QDialog):
    def __init__(self, text, latex_text, parent=None):
        """
        Opens a QDialog and show text and a rendered latex text of exact answer

        :param text: string
            The text that is shown in the QTextBrowser
        :param latex_text: string
            Mathjax will render the LaTeX and show it with QWebEngineView

        The UI file is loaded and set the text to the QTextBrowser. A HTML file using the MathJax API is created and shown with the QWebEngineView
        """
        super(View, self).__init__(parent=None)
        loadUi("qt_assets/main_view_e.ui", self)
        font_size = "2.5em"
        page_source = f"""
             <html><head>
             <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
             <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>                
             </script></head>
             <body>
             <p><mathjax style="font-size:{font_size}">$${latex_text}$$</mathjax></p>
             </body></html>
             """
        self.exact_text.setText(text)
        self.web.setHtml(page_source)
        self.show()

class View_Text(QDialog):
    def __init__(self, text, parent=None):
        """
        Opens a QDialog and show text and a rendered latex text of exact answer

        :param text: string
            The text that is shown in the QTextBrowser

        The UI file is loaded and set the text to the QTextBrowser
        """
        super(View_Text, self).__init__(parent=None)
        loadUi("qt_assets/main_view_a.ui", self)
        self.approx_text.setText(text)
        self.show()

def launch_app():
    import sys
    app = QApplication(sys.argv)
    caspy = CASpyGUI()
    sys.exit(app.exec_())