from PyQt5.QtCore import pyqtSlot, QEvent, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QCursor
from PyQt5.uic import loadUi

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

import traceback

from .worker import BaseWorker


class SimpWorker(BaseWorker):
    def __init__(self, command, params, copy=None):
        super().__init__(command, params, copy)

    @BaseWorker.catch_error
    @pyqtSlot()
    def prev_simp_exp(self, expression, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not expression:
            return {"error": ["Enter an expression"]}

        if output_type == 1:
            try:
                self.exact_ans = str(pretty(parse_expr(expression, evaluate=False)))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
        elif output_type == 2:
            try:
                self.exact_ans = str(latex(parse_expr(expression, evaluate=False)))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
            self.latex_answer = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(expression)
        self.latex_answer = str(latex(parse_expr(expression, evaluate=False)))

        return {"simp": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @BaseWorker.catch_error
    @pyqtSlot()
    def simp_exp(self, expression, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not expression:
            return {"error": ["Enter an expression"]}

        try:
            self.exact_ans = simplify(expression)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        self.latex_answer = str(latex(self.exact_ans))
        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"simp": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}


class SimplifyTab(QWidget):

    display_name = "Simplify"

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        loadUi(self.main_window.get_resource_path("qt_assets/tabs/simplify.ui"), self)

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
        self.SimpOut.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
            self.main_window.latex_text = ""
        else:
            self.main_window.latex_text = input_dict["latex"]
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.SimpOut.setText(self.main_window.exact_ans)

    def prev_simp_exp(self):
        self.SimpOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = SimpWorker("prev_simp_exp", [
            self.SimpExp.toPlainText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)

    def simp_exp(self):
        self.SimpOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = SimpWorker("simp_exp", [
            self.SimpExp.toPlainText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)
