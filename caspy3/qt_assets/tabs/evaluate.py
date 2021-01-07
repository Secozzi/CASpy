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

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QShortcut, QWidget
from PyQt5.QtGui import QCursor, QKeySequence
from PyQt5.uic import loadUi

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

import traceback
import re as pyreg
import typing as ty

from .worker import BaseWorker


class EvaluateWorker(BaseWorker):
    def __init__(self, command: str, params: list, copy: int = None) -> None:
        super().__init__(command, params, copy)

    @BaseWorker.catch_error
    @pyqtSlot()
    def prev_eval_exp(
        self,
        expression: str,
        var_sub: str,
        output_type: int,
        use_unicode: bool,
        line_wrap: bool,
    ) -> ty.Dict[str, ty.List[str]]:
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
    def parse_var_sub(self, var_sub: str) -> ty.Dict[str, str]:
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
    def eval_exp(
        self,
        expression: str,
        var_sub: str,
        output_type: int,
        use_unicode: bool,
        line_wrap: bool,
        use_scientific: ty.Union[int, None],
        accuracy: int,
    ) -> ty.Dict[str, ty.List[str]]:
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
                return {
                    "error": [
                        "A ':' must be present after variable to indicate end of variable"
                    ]
                }

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
                self.approx_ans = self.to_scientific_notation(
                    str(N(self.exact_ans, accuracy)), use_scientific
                )
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

    def __init__(self, main_window: "CASpyGUI") -> None:
        super().__init__()
        self.main_window = main_window
        loadUi(self.main_window.get_resource_path("qt_assets/tabs/evaluate.ui"), self)
        self.eout = self.EvalOut
        self.aout = self.EvalApprox

        # Shortcuts
        cshortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        cshortcut.activated.connect(self.eval_exp)
        pshortcut = QShortcut(QKeySequence("Ctrl+Shift+Return"), self)
        pshortcut.activated.connect(self.prev_eval_exp)

        self.init_bindings()

    def init_bindings(self) -> None:
        self.EvalPrev.clicked.connect(self.prev_eval_exp)
        self.EvalCalc.clicked.connect(self.eval_exp)
        self.eout.mousePressEvent = lambda _: self.eout.selectAll()
        self.aout.mousePressEvent = lambda _: self.aout.selectAll()
        self.eout.focusOutEvent = lambda _: self.deselect(self.eout)
        self.aout.focusOutEvent = lambda _: self.deselect(self.aout)

    @staticmethod
    def deselect(textbrowser: "QTextBrowser") -> None:
        cursor = textbrowser.textCursor()
        cursor.clearSelection()
        textbrowser.setTextCursor(cursor)

    def stop_thread(self) -> None:
        pass

    def update_ui(self, input_dict: ty.Dict[str, ty.List[str]]) -> None:
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

    def prev_eval_exp(self) -> None:
        self.EvalOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.EvalApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = EvaluateWorker(
            "prev_eval_exp",
            [
                self.EvalExp.toPlainText(),
                self.EvalVarSub.text(),
                self.main_window.output_type,
                self.main_window.use_unicode,
                self.main_window.line_wrap,
            ],
        )
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)

    def eval_exp(self) -> None:
        self.EvalOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.EvalApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = EvaluateWorker(
            "eval_exp",
            [
                self.EvalExp.toPlainText(),
                self.EvalVarSub.text(),
                self.main_window.output_type,
                self.main_window.use_unicode,
                self.main_window.line_wrap,
                self.main_window.use_scientific,
                self.main_window.accuracy,
            ],
        )
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)
