from PyQt5.QtCore import pyqtSlot, QEvent, Qt
from PyQt5.QtWidgets import QAction, QApplication, QWidget
from PyQt5.QtGui import QCursor
from PyQt5.uic import loadUi

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

import traceback

from worker import BaseWorker


class IntegralWorker(BaseWorker):
    def __init__(self, command, params, copy=None):
        super().__init__(command, params, copy)

    @BaseWorker.catch_error
    @pyqtSlot()
    def prev_integ(self, input_expression, input_variable, input_lower, input_upper, output_type, use_unicode,
                   line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}
        if (input_lower and not input_upper) or (not input_lower and input_upper):
            return {"error": ["Enter both upper and lower bound"]}

        if input_lower:
            try:
                self.exact_ans = Integral(parse_expr(input_expression), (parse_expr(input_variable),
                                                                         input_lower, input_upper))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
        else:
            try:
                self.exact_ans = Integral(parse_expr(input_expression), parse_expr(input_variable))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

        self.latex_answer = str(latex(self.exact_ans))
        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"integ": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @BaseWorker.catch_error
    @pyqtSlot()
    def calc_integ(self, input_expression, input_variable, input_lower, input_upper, approx_integ, output_type,
                   use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}
        if (input_lower and not input_upper) or (not input_lower and input_upper):
            return {"error": ["Enter both upper and lower bound"]}

        if input_lower:
            try:
                self.exact_ans = Integral(parse_expr(input_expression),
                                          (parse_expr(input_variable), input_lower, input_upper))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

            if approx_integ:
                self.exact_ans = N(self.exact_ans, accuracy)
            else:
                try:
                    self.exact_ans = self.exact_ans.doit()
                except Exception:
                    return {"error": [f"Error: \n{traceback.format_exc()}"]}

            self.latex_answer = str(latex(self.exact_ans))

            try:
                if use_scientific:
                    self.approx_ans = self.to_scientific_notation(str(N(self.exact_ans, accuracy)), use_scientific)
                else:
                    self.approx_ans = str(simplify(N(self.exact_ans, accuracy)))
            except Exception:
                self.approx_ans = 0
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
            else:
                if use_scientific:
                    self.approx_ans = self.to_scientific_notation(str(N(self.exact_ans, accuracy)), use_scientific)
                else:
                    self.approx_ans = str(N(self.exact_ans, accuracy))

        else:
            try:
                self.exact_ans = integrate(parse_expr(input_expression), parse_expr(input_variable))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
            self.latex_answer = str(latex(self.exact_ans))

        unable_to_integrate = issubclass(type(self.exact_ans), Integral)

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        if unable_to_integrate:
            self.exact_ans = "Unable to evaluate integral:\n" + self.exact_ans

        return {"integ": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}


class IntegralTab(QWidget):

    display_name = "Integral"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/integral.ui", self)
        self.main_window = main_window

        if "approx_integ" in list(self.main_window.settings_data.keys()):
            self.approx_integ = self.main_window.settings_data["approx_integ"]
        else:
            self.approx_integ = False
        self.main_window.add_to_save_settings({"approx_integ": self.approx_integ})

        self.install_event_filters()
        self.init_integral_menu()
        self.init_bindings()

    def install_event_filters(self):
        self.IntegExp.installEventFilter(self)

    def init_integral_menu(self):
        self.menuInteg = self.main_window.menubar.addMenu("Integral")
        self.menuInteg.setToolTipsVisible(True)
        approx_integ = QAction("Approximate integral", self, checkable=True)
        approx_integ.setToolTip("Approximates integral by N(). Note: this overrides the normal calculation")
        approx_integ.setChecked(self.approx_integ)
        self.menuInteg.addAction(approx_integ)
        approx_integ.triggered.connect(self.toggle_approx_integ)

    def toggle_approx_integ(self, state):
        if state:
            self.approx_integ = True
        else:
            self.approx_integ = False

        self.main_window.update_save_settings({"approx_integ": self.approx_integ})

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
        self.IntegOut.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.IntegApprox.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
            self.main_window.latex_text = ""
        else:
            self.main_window.latex_text = input_dict["latex"]
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.IntegOut.setText(self.main_window.exact_ans)
            self.IntegApprox.setText(str(self.main_window.approx_ans))

    def prev_integ(self):
        self.IntegOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.IntegApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = IntegralWorker("prev_integ", [
            self.IntegExp.toPlainText(),
            self.IntegVar.text(),
            self.IntegLower.text(),
            self.IntegUpper.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)

    def calc_integ(self):
        self.IntegOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.IntegApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = IntegralWorker("calc_integ", [
            self.IntegExp.toPlainText(),
            self.IntegVar.text(),
            self.IntegLower.text(),
            self.IntegUpper.text(),
            self.approx_integ,
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)