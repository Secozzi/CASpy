from PyQt5.QtCore import QCoreApplication, QEvent, Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QAction, QApplication, QWidget
from PyQt5.uic import loadUi
from worker import CASWorker


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
        self.menuShell = self.main_window.menubar.addMenu("Shell")
        self.clear_shell_action = QAction("Clear Shell", self)
        self.clear_shell_action.setChecked(True)
        self.menuShell.addAction(self.clear_shell_action)
        self.clear_shell_action.setShortcut(_translate("MainWindow", "Ctrl+Shift+C"))
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