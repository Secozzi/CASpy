from PyQt5.QtCore import pyqtSlot, QCoreApplication, QEvent, QRegularExpression, Qt
from PyQt5.QtWidgets import QAction, QApplication, \
    QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QCursor, QFont, QTextCursor

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

import sys
import traceback

from qt_assets.tabs.shell.paren_highlight import TextEdit
from qt_assets.tabs.shell.syntax_pars import PythonHighlighter
from qt_assets.tabs.shell.start_code_dialog import StartCodeDialog

from worker import BaseWorker


class ShellWorker(BaseWorker):
    def __init__(self, command, params, copy=None):
        super().__init__(command, params, copy)

    @BaseWorker.catch_error
    @pyqtSlot()
    def execute_code(self, code, namespace):
        self.exact_ans = ""
        self.approx_ans = 0
        self.latex_answer = r"\text{LaTeX not supported for shell}"
        new_namespace = namespace

        class Capturing(list):
            from io import StringIO
            def __enter__(self):
                self._stdout = sys.stdout
                sys.stdout = self._stringio = self.StringIO()
                return self

            def __exit__(self, *args):
                self.extend(self._stringio.getvalue().splitlines())
                del self._stringio
                sys.stdout = self._stdout

        try:
            with Capturing() as self.output:
                try:
                    exec(f"print({code})", namespace)
                except Exception:
                    exec(code, namespace)
        except Exception:
            self.output = f"\nError: {traceback.format_exc()}"

        new_namespace.update(locals())

        if type(self.output) != str:
            for i in self.output:
                self.exact_ans += f"{i}\n"

            self.exact_ans = self.exact_ans[:-1]
        else:
            self.exact_ans = self.output

        return {"exec": [self.exact_ans, self.approx_ans], "latex": self.latex_answer, "new_namespace": new_namespace}


class Console(TextEdit):
    def __init__(self, start_text, start_code, main_window, parent=None):
        TextEdit.__init__(self, parent)
        self.setStyleSheet("QPlainTextEdit{font: 8pt 'Courier New'; color: #383a42; background-color: #fafafa;}")

        self.prompt = ">>> "
        self.new_line = "... "

        self.start_code = start_code
        self.start_text = start_text
        self.main_window = main_window

        self.base_namespace = {}
        self.namespace = {}
        self.history = []
        self.history_index = 0

        self.setPlainText(self.start_text + self.start_code + "\n\n" + self.prompt)
        self.moveCursor(QTextCursor.End)
        self.setUndoRedoEnabled(False)
        highlight = PythonHighlighter(self.document())
        self.create_base_namespace()

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        """
        Insert output if code returns anything. The start code will create a base namespace that will never change.
        The normal namespace will go back to the base namespace when shell is cleared.
        :param input_dict:
        :return:
        """
        self.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
            self.main_window.latex_text = ""
        else:
            self.main_window.latex_text = input_dict["latex"]
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            if self.main_window.exact_ans:
                self.insertPlainText("\n" + self.main_window.exact_ans + "\n>>> ")

            self.base_namespace = input_dict["new_namespace"]
            self.namespace = dict(self.namespace, **self.base_namespace)

        self.moveCursor(QTextCursor.End)

    def create_base_namespace(self):
        """
        Execute start code
        :return:
        """
        if self.start_code:
            self.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

            worker = ShellWorker("execute_code", [self.start_code, self.namespace])
            worker.signals.output.connect(self.update_ui)
            worker.signals.finished.connect(self.stop_thread)

            self.main_window.threadpool.start(worker)

    def update_namespace(self, namespace):
        self.namespace.update(namespace)

    def clear_shell(self):
        """Clears namespace and history and inserts default text into console"""
        self.setPlainText(self.start_text + self.start_code + "\n\n" + self.prompt)
        self.namespace = self.base_namespace
        self.history = []
        self.moveCursor(QTextCursor.End)

    def get_command(self):
        """
        Gets command entered. If the first four characters equals '... ' it knows it's a multiline command,
        and will loop over previous lines until it finds a line starting with '>>> '. Every line
        gets added to the list self.current_command
        """
        doc = self.document()
        current_line_number = doc.lineCount() - 1
        line_counter = 1
        current_command = []

        current_line = doc.findBlockByLineNumber(current_line_number).text()
        start = current_line[0:len(self.new_line)]

        if current_line.replace("\t", "") != "... ":
            current_command.append(current_line)

        while start == self.new_line:
            current_line = doc.findBlockByLineNumber(current_line_number - line_counter).text()
            start = current_line[0:len(self.new_line)]
            line_counter += 1

            if current_line.replace("\t", "") != "... ":
                current_command.append(current_line)

        output = ""
        for c in reversed(current_command):
            output += c[4:] + "\n"
        return output[:-1], self.namespace

    def add_to_history(self, line_text):
        """Checks if current line doesn't already exist or is empty and adds it to current line"""
        if line_text != self.prompt and line_text.replace("\t", "") != "... " and line_text[4:] not in self.history:
            self.history.append(line_text[4:])

        self.history_index = len(self.history)

    def set_command(self, command):
        """Sets command to current line"""
        self.moveCursor(QTextCursor.End)
        self.moveCursor(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        for i in range(len(self.prompt)):
            self.moveCursor(QTextCursor.Right, QTextCursor.KeepAnchor)
        self.textCursor().removeSelectedText()
        self.textCursor().insertText(command)
        self.moveCursor(QTextCursor.End)

    def get_previous_history_entry(self):
        if self.history:
            if self.history_index == 0:
                return self.history[self.history_index]
            else:
                self.history_index -= 1
                return self.history[self.history_index]
        else:
            return ""

    def get_next_history_entry(self):
        if self.history:
            if self.history_index == len(self.history):
                return self.history[self.history_index - 1]
            else:
                self.history_index += 1
                if self.history_index == len(self.history):
                    return self.history[self.history_index - 1]
                else:
                    return self.history[self.history_index]
        else:
            return ""

    def get_cursor_position(self):
        return self.textCursor().columnNumber() - len(self.prompt)


class ShellTab(QWidget):
    display_name = "Shell"

    def __init__(self, main_window):
        super(ShellTab, self).__init__()
        self.main_window = main_window
        self.setFont(QFont("Courier New", 8))

        if "start_code" in list(self.main_window.settings_data.keys()):
            self.start_code = self.main_window.settings_data["start_code"]
        else:
            self.start_code = "from __future__ import division\n\nfrom sympy import *\nfrom sympy.parsing.sympy_parser import " \
                     "parse_expr\nfrom sympy.abc import _clash1\n\nimport math\nimport cmath as cm\n\nx, y, z, " \
                     "t = symbols('x y z t')\nk, m, n = symbols('k m n', integer=True)\nf, g, h = symbols('f g h', " \
                     "cls=Function)"
        self.main_window.add_to_save_settings({"start_code": self.start_code})

        self.init_ui()
        self.init_bindings()
        self.install_event_filter()
        self.add_to_menu()

    def init_ui(self):
        self.shell_layout = QVBoxLayout()
        self.start_text = "# This is a very simple shell using 'exec' commands, so it has some limitations. Every variable " \
                     "declared and function defined will be saved until the program is closed or when the 'clear " \
                     "commands' button in the menubar is pressed. It will automatically output to the shell. To copy " \
                     "output, press the 'copy exact answer' in the " \
                     "menubar.\n# These commands were executed:\n"

        self.consoleIn = Console(self.start_text, self.start_code, self.main_window)
        self.ShellRun = QPushButton()
        self.ShellRun.setText("Run (Enter)")

        self.shell_layout.addWidget(self.consoleIn)
        self.shell_layout.addWidget(self.ShellRun)
        self.setLayout(self.shell_layout)

    def install_event_filter(self):
        self.consoleIn.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                last_line = self.consoleIn.document().lastBlock().text()

                self.consoleIn.add_to_history(last_line)

                if modifiers:
                    if modifiers[0] == "shift":
                        self.consoleIn.appendPlainText("... ")
                        return super(ShellTab, self).eventFilter(obj, event)
                else:
                    self.consoleIn.moveCursor(QTextCursor.End)
                    if last_line[-1] == ":" or (last_line[0:4] == "... " and len(last_line.replace("\t", "")) != 4):
                        no_of_tabs_regex = QRegularExpression(r"(?<=\.\.\. )(\t)+")
                        no_of_tabs_match = no_of_tabs_regex.match(last_line)
                        no_of_tabs = no_of_tabs_match.capturedLength()

                        if last_line[-1] == ":":
                            no_of_tabs += 1

                        self.consoleIn.appendPlainText("... " + "\t" * (no_of_tabs))
                        return True
                    else:
                        to_execute, namespace = self.consoleIn.get_command()
                        self.execute_code(to_execute, namespace)
                        return True

            if event.key() in (Qt.Key_Left, Qt.Key_Backspace):
                if self.consoleIn.get_cursor_position() == 0:
                    return True

            if event.key() == Qt.Key_Up:
                entry = self.consoleIn.get_previous_history_entry()
                self.consoleIn.set_command(entry)
                return True

            if event.key() == Qt.Key_Down:
                entry = self.consoleIn.get_next_history_entry()
                self.consoleIn.set_command(entry)
                return True

        return super(ShellTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.ShellRun.clicked.connect(self.execute_code)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        self.consoleIn.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
            self.main_window.latex_text = ""
        else:
            self.main_window.latex_text = input_dict["latex"]
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            if self.main_window.exact_ans:
                self.consoleIn.insertPlainText("\n" + self.main_window.exact_ans + "\n>>> ")
            else:
                self.consoleIn.insertPlainText("\n>>> ")

            self.consoleIn.update_namespace(input_dict["new_namespace"])

        self.consoleIn.moveCursor(QTextCursor.End)

    def add_to_menu(self):
        _translate = QCoreApplication.translate
        self.menuShell = self.main_window.menubar.addMenu("Shell")
        self.clear_shell_action = QAction("Clear Shell", self)
        self.clear_shell_action.setChecked(True)
        self.menuShell.addAction(self.clear_shell_action)
        self.clear_shell_action.setShortcut(_translate("MainWindow", "Ctrl+Shift+C"))
        self.clear_shell_action.triggered.connect(self.clear_shell)

        self.menuShell.addSeparator()

        self.edit_start_action = QAction("Edit Start Code", self)
        self.edit_start_action.triggered.connect(self.edit_start_code)
        self.menuShell.addAction(self.edit_start_action)

    def execute_start_code(self):
        self.execute_code(self.start_code, {})

    def clear_shell(self):
        self.consoleIn.clear_shell()

    def edit_start_code(self):
        self.start_text_dialog = StartCodeDialog(self.start_code, self)

    def update_start_code(self, text):
        self.main_window.update_save_settings({"start_code": text})

    def execute_code(self, command, namespace):
        if command:
            self.consoleIn.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

            worker = ShellWorker("execute_code", [command, namespace])
            worker.signals.output.connect(self.update_ui)
            worker.signals.finished.connect(self.stop_thread)

            self.main_window.threadpool.start(worker)
