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

import typing as ty

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

import traceback

from .worker import BaseWorker


class SimpWorker(BaseWorker):
    def __init__(self, command: str, params: list, copy: int = None) -> None:
        super().__init__(command, params, copy)

    @BaseWorker.catch_error
    @pyqtSlot()
    def prev_simp_exp(
        self, expression: str, output_type: int, use_unicode: bool, line_wrap: bool
    ) -> ty.Dict[str, ty.List[str]]:
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
    def simp_exp(
        self, expression: str, output_type: int, use_unicode: bool, line_wrap: bool
    ) -> ty.Dict[str, ty.List[str]]:
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

    def __init__(self, main_window: "CASpyGUI") -> None:
        super().__init__()
        self.main_window = main_window
        loadUi(self.main_window.get_resource_path("qt_assets/tabs/simplify.ui"), self)
        self.eout = self.SimpOut
        self.aout = None

        # Shortcuts
        cshortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        cshortcut.activated.connect(self.simp_exp)
        pshortcut = QShortcut(QKeySequence("Ctrl+Shift+Return"), self)
        pshortcut.activated.connect(self.prev_simp_exp)

        self.init_bindings()

    def init_bindings(self) -> None:
        self.SimpPrev.clicked.connect(self.prev_simp_exp)
        self.SimpCalc.clicked.connect(self.simp_exp)
        self.eout.mousePressEvent = lambda _: self.eout.selectAll()
        self.eout.focusOutEvent = lambda _: self.deselect(self.eout)

    @staticmethod
    def deselect(textbrowser: "QTextBrowser") -> None:
        cursor = textbrowser.textCursor()
        cursor.clearSelection()
        textbrowser.setTextCursor(cursor)

    def stop_thread(self) -> None:
        pass

    def update_ui(self, input_dict: ty.Dict[str, ty.List[str]]) -> None:
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

    def prev_simp_exp(self) -> None:
        self.SimpOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = SimpWorker(
            "prev_simp_exp",
            [
                self.SimpExp.toPlainText(),
                self.main_window.output_type,
                self.main_window.use_unicode,
                self.main_window.line_wrap,
            ],
        )
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)

    def simp_exp(self) -> None:
        self.SimpOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = SimpWorker(
            "simp_exp",
            [
                self.SimpExp.toPlainText(),
                self.main_window.output_type,
                self.main_window.use_unicode,
                self.main_window.line_wrap,
            ],
        )
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)
