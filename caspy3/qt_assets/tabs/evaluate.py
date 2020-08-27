from PyQt5.QtCore import pyqtSlot, QEvent, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QCursor
from PyQt5.uic import loadUi

from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from sympy.physics.units import degree

import traceback

import re as pyreg

from worker import BaseWorker


class EvaluateWorker(BaseWorker):
    def __init__(self, command, params, copy=None):
        super().__init__(command, params, copy)

    @BaseWorker.catch_error
    @pyqtSlot()
    def prev_eval_exp(self, expression, var_sub, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not expression:
            return {"error": ["Enter an expression"]}

        if var_sub:
            self.exact_ans = f"With variable substitution {var_sub}\n"

        try:
            _ = parse_expr(expression)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        self.latex_answer = str(latex(parse_expr(expression, evaluate=False)))
        if output_type == 1:
            try:
                self.exact_ans += str(pretty(parse_expr(expression, evaluate=False)))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
        elif output_type == 2:
            try:
                self.exact_ans += str(latex(parse_expr(expression, evaluate=False)))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
        else:
            self.exact_ans += str(expression)

        return {"eval": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @BaseWorker.catch_error
    @pyqtSlot()
    def parse_var_sub(self, var_sub):
        """
        Parses var_sub and returns a dictionary. Any variable followed by a ':' will be subtituted by everything
        between the ':' and the next variable. It must be of the type var1: value1 var2: value2 or else
        it will return an error

        Examples:
            t: 34 y: pi/3 z: 5
            => {'t': '34', 'y': 'pi/3', 'z': '5'}

        :param var_sub: string
            String containing variables
        :return: Dict
            Dictionary with variable as key and subtition as value
        """
        match_key = pyreg.compile(r"[a-zA-Z0-9_]+:")
        output = {}

        if ":" not in var_sub:
            return {"error": f"Colon missing"}

        key_reg = match_key.finditer(var_sub)
        keys = [i.group(0) for i in key_reg]

        for key in range(len(keys) - 1):
            start = keys[key]
            end = keys[key + 1]
            in_between = pyreg.compile(f"{start}(.*){end}")

            result = in_between.search(var_sub).group(1).strip()
            if not result:
                return {"error": f"Variable '{start[0:-1]}' is missing a value"}

            output[start[0:-1]] = result

        last_value = var_sub.split(keys[-1])[1].strip()
        if not last_value:
            return {"error": f"Variable '{keys[-1][0:-1]}' is missing a value"}
        output[keys[-1][0:-1]] = last_value
        return output

    @BaseWorker.catch_error
    @pyqtSlot()
    def eval_exp(self, expression, var_sub, output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not expression:
            return {"error": ["Enter an expression"]}

        expression = str(expression)

        if var_sub:
            if ":" not in var_sub:
                return {"error": ["A ':' must be present after variable to indicate end of variable"]}

            var_sub = self.parse_var_sub(var_sub)
            if "error" in list(var_sub.keys()):
                return {"error": [var_sub["error"]]}

            try:
                expression = parse_expr(expression, evaluate=False)

                for var in var_sub.keys():
                    expression = expression.subs(parse_expr(var), f"({var_sub[var]})")

            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
        try:
            expression = str(expression)
            self.exact_ans = simplify(parse_expr(expression))
            if use_scientific:
                self.approx_ans = self.to_scientific_notation(str(N(self.exact_ans, accuracy)), use_scientific)
            else:
                self.approx_ans = str(N(self.exact_ans, accuracy))
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}
        self.latex_answer = str(latex(self.exact_ans))

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"eval": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

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
        self.EvalVarSub.installEventFilter(self)

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
        self.EvalOut.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.EvalApprox.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(str(input_dict[first_key][0]))
            self.main_window.latex_text = ""
        else:
            self.main_window.latex_text = input_dict["latex"]
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.EvalOut.setText(str(self.main_window.exact_ans))
            self.EvalApprox.setText(str(self.main_window.approx_ans))

    def prev_eval_exp(self):
        self.EvalOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.EvalApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = EvaluateWorker("prev_eval_exp", [
            self.EvalExp.toPlainText(),
            self.EvalVarSub.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)

    def eval_exp(self):
        self.EvalOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.EvalApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = EvaluateWorker("eval_exp", [
            self.EvalExp.toPlainText(),
            self.EvalVarSub.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)