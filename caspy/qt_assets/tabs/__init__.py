from PyQt5.QtCore import (
    QCoreApplication,
    QEvent,
    QMetaObject,
    QRect,
    QRegExp,
    QSize,
    Qt,
    QThreadPool,
    QUrl
)

from PyQt5.QtGui import (
    QCursor,
    QFont,
    QIcon,
    QRegExpValidator,
    QTextCursor
)

# Everything that my IDE says aren't used doesn't need to be imported, and I have no idea why but im keeping it here anyways.
from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QApplication,
    QButtonGroup,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSpinBox,
    QStatusBar,
    QTabWidget,
    QTextBrowser,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget
)

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.uic import loadUi

from Worker import CASWorker

class DerivativeTab(QWidget):

    display_name = "Derivative"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/derivative.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.DerivExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.calc_deriv()
                        return True

        return super(DerivativeTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.DerivPrev.clicked.connect(self.prev_deriv)
        self.DerivCalc.clicked.connect(self.calc_deriv)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.DerivOut.setText(self.main_window.exact_ans)
            self.DerivApprox.setText(str(self.main_window.approx_ans))

    def prev_deriv(self):
        if self.DerivPP.isChecked():
            output_type = 1
        elif self.DerivLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_deriv", [
            self.DerivExp.toPlainText(),
            self.DerivVar.text(),
            self.DerivOrder.value(),
            self.DerivPoint.text(),
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def calc_deriv(self):
        """
        Function to call the worker thread to calculate the expression as a derivative.
        It checks what output type is selected.
        """
        if self.DerivPP.isChecked():
            output_type = 1
        elif self.DerivLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("calc_deriv", [
            self.DerivExp.toPlainText(),
            self.DerivVar.text(),
            self.DerivOrder.value(),
            self.DerivPoint.text(),
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class IntegralTab(QWidget):

    display_name = "Integral"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/integral.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.IntegExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.calc_integ()
                        return True

        return super(IntegralTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.IntegPrev.clicked.connect(self.prev_integ)
        self.IntegCalc.clicked.connect(self.calc_integ)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.IntegOut.setText(self.main_window.exact_ans)
            self.IntegApprox.setText(str(self.main_window.approx_ans))

    def prev_integ(self):
        if self.IntegPP.isChecked():
            output_type = 1
        elif self.IntegLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_integ", [
            self.IntegExp.toPlainText(),
            self.IntegVar.text(),
            self.IntegOrder.value(),
            self.IntegPoint.text(),
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def calc_integ(self):
        """
        Function to call the worker thread to calculate the expression as a integative.
        It checks what output type is selected.
        """
        if self.IntegPP.isChecked():
            output_type = 1
        elif self.IntegLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("calc_integ", [
            self.IntegExp.toPlainText(),
            self.IntegVar.text(),
            self.IntegLower.text(),
            self.IntegUpper.text(),
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class LimitTab(QWidget):

    display_name = "Limit"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/limit.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.LimExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.calc_limit()
                        return True

        return super(LimitTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.LimPrev.clicked.connect(self.prev_limit)
        self.LimCalc.clicked.connect(self.calc_limit)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.LimOut.setText(self.main_window.exact_ans)
            self.LimApprox.setText(str(self.main_window.approx_ans))

    def prev_limit(self):
        if self.LimPP.isChecked():
            output_type = 1
        elif self.LimLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        if self.LimSide.currentIndex() == 0:
            limit_side = "+-"
        elif self.LimSide.currentIndex() == 1:
            limit_side = "-"
        else:
            limit_side = "+"

        self.WorkerCAS = CASWorker("prev_limit", [
            self.LimExp.toPlainText(),
            self.LimVar.text(),
            self.LimApproach.text(),
            limit_side,
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def calc_limit(self):
        """
        Function to call the worker thread to calculate the expression as a limative.
        It checks what output type is selected.
        """
        if self.LimPP.isChecked():
            output_type = 1
        elif self.LimLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        if self.LimSide.currentIndex() == 0:
            limit_side = "+-"
        elif self.LimSide.currentIndex() == 1:
            limit_side = "-"
        else:
            limit_side = "+"

        self.WorkerCAS = CASWorker("calc_limit", [
            self.LimExp.toPlainText(),
            self.LimVar.text(),
            self.LimApproach.text(),
            limit_side,
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class SimplifyTab(QWidget):
    display_name = "Simplify"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/simplify.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.SimpExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.simp_exp()
                        return True

        return super(SimplifyTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.SimpPrev.clicked.connect(self.prev_simp_exp)
        self.SimpCalc.clicked.connect(self.simp_exp)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.SimpOut.setText(self.main_window.exact_ans)

    def prev_simp_exp(self):
        if self.SimpPP.isChecked():
            output_type = 1
        elif self.SimpLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_simp_eq", [
            self.SimpExp.toPlainText(),
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def simp_exp(self):
        if self.SimpPP.isChecked():
            output_type = 1
        elif self.SimpLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_simp_eq", [
            self.SimpExp.toPlainText(),
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class ExpandTab(QWidget):
    display_name = "Expand"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/expand.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.ExpExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.exp_exp()
                        return True

        return super(ExpandTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.ExpPrev.clicked.connect(self.prev_exp_exp)
        self.ExpCalc.clicked.connect(self.exp_exp)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.ExpOut.setText(self.main_window.exact_ans)

    def prev_exp_exp(self):
        if self.ExpPP.isChecked():
            output_type = 1
        elif self.ExpLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_exp_eq", [
            self.ExpExp.toPlainText(),
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def exp_exp(self):
        if self.ExpPP.isChecked():
            output_type = 1
        elif self.ExpLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_exp_eq", [
            self.ExpExp.toPlainText(),
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class EvaluateTab(QWidget):
    display_name = "Evaluate"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/evaluate.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.EvalExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.eval_exp()
                        return True

        return super(EvaluateTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.EvalPrev.clicked.connect(self.prev_eval_exp)
        self.EvalCalc.clicked.connect(self.eval_exp)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.EvalOut.setText(self.main_window.exact_ans)
            self.EvalApprox.setText(self.main_window.approx_ans)

    def prev_eval_exp(self):
        if self.EvalPP.isChecked():
            output_type = 1
        elif self.EvalLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_eval_exp", [
            self.EvalExp.toPlainText(),
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def eval_exp(self):
        if self.EvalPP.isChecked():
            output_type = 1
        elif self.EvalLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("eval_exp", [
            self.EvalExp.toPlainText(),
            output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class PfTab(QWidget):
    display_name = "Prime Factors"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/pf.ui", self)
        self.main_window = main_window
        self.init_bindings()

    def init_bindings(self):
        self.PfCalc.clicked.connect(self.calc_pf)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.PfOut.setText(self.main_window.exact_ans)
            self.PfApprox.setText(self.main_window.approx_ans)

    def calc_pf(self):
        self.WorkerCAS = CASWorker("calc_pf", [self.PfInput.value()])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class WebTab(QWidget):

    display_name = "Web"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/web.ui", self)
        self.main_window = main_window
        self.init_web_menu()
        self.web.load(QUrl("https://www.desmos.com/calculator"))

    def init_web_menu(self):
        self.menuWeb = self.main_window.menubar.addMenu("Web")
        self.WebList = self.main_window.json_file[2]
        webGroup = QActionGroup(self.menuWeb)
        for i in self.WebList:
            for key in i:
                webAction = QAction(key, self.menuWeb, checkable=True)
                if webAction.text() == "Desmos":
                    webAction.setChecked(True)
                self.menuWeb.addAction(webAction)
                webGroup.addAction(webAction)

        webGroup.setExclusive(True)
        webGroup.triggered.connect(self.updateWeb)

    def updateWeb(self, action):
        """
        Updates web tab when user selects new website.

        Parameters
        ---------------
        action: QAction
            action.text() shows text of selected radiobutton
        """

        self.main_window.exact_ans = 0
        self.main_window.approx_ans = 0
        for i in self.WebList:
            for key in i:
                if action.text() == key:
                    self.web.load(QUrl(i[key]))

class ShellTab(QWidget):
    display_name = "Shell"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/shell.ui", self)
        self.main_window = main_window
        self.current_code = self.consoleIn.toPlainText()
        self.previous_code_list = []

        self.install_event_filter()
        self.init_bindings()
        self.add_to_menu()

    def install_event_filter(self):
        self.consoleIn.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.consoleIn.appendPlainText("... ")
                        return True
                else:
                    self.execute_code()
                    return True

        return super(ShellTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.ShellRun.clicked.connect(self.execute_code)

    def add_to_menu(self):
        _translate = QCoreApplication.translate
        self.clear_shell_action = QAction("Clear Shell", self)
        self.clear_shell_action.setShortcut(_translate("MainWindow", "Ctrl+Shift+C"))
        self.main_window.menuSettings.addSeparator()
        self.main_window.menuSettings.addAction(self.clear_shell_action)
        self.clear_shell_action.triggered.connect(self.clear_shell)

    def clear_shell(self):
        # Clears shell of written text, and previously initialized variables and functions.
        self.previous_code_list = []
        code = "This is a very simple shell using 'exec' commands, so it has some limitations. Every variable declared and function defined will be saved until the program is closed or when the 'clear commands' button in the menubar is pressed. It will automatically output to the shell, but it can't use 'print' commands. To copy output, press the 'copy exact answer' in the menubar.\nTheses commands were executed:\nfrom __future__ import division\n\nfrom sympy import *\nfrom sympy.parsing.sympy_parser import parse_expr\nfrom sympy.abc import _clash1\n\nimport math as m\nimport cmath as cm\n\nx, y, z, t = symbols('x y z t')\nk, m, n = symbols('k m n', integer=True)\nf, g, h = symbols('f g h', cls=Function)\n\n>>> "
        self.consoleIn.clear()
        self.consoleIn.appendPlainText(code)
        self.current_code = code

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        if "list" in list(input_dict.keys()):
            self.previous_code_list = input_dict["list"]
        else:
            self.previous_code_list = []

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.consoleIn.insertPlainText(self.main_window.exact_ans + "\n>>> ")
            self.consoleIn.moveCursor(QTextCursor.End)
            self.current_code = self.consoleIn.toPlainText()

    def execute_code(self):
        self.new_code = self.consoleIn.toPlainText().replace(self.current_code, "")
        self.consoleIn.moveCursor(QTextCursor.End)

        self.WorkerCAS = CASWorker("execute_code", [self.new_code, self.previous_code_list])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)