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
from PyQt5.QtWidgets import QShortcut, QTextBrowser, QWidget
from PyQt5.QtGui import QCursor, QKeySequence
from PyQt5.uic import loadUi

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

import traceback
import typing as ty

from .worker import BaseWorker


class DerivativeWorker(BaseWorker):
    def __init__(self, command: str, params: list, copy: int = None) -> None:
        super().__init__(command, params, copy)

    @BaseWorker.catch_error
    @pyqtSlot()
    def prev_deriv(
        self,
        input_expression: str,
        input_variable: str,
        input_order: int,
        input_point: str,
        output_type: int,
        use_unicode: bool,
        line_wrap: bool,
    ) -> ty.Dict[str, ty.List[str]]:
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}

        try:
            derivative = Derivative(str(input_expression), input_variable, input_order)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}
        self.latex_answer = str(latex(derivative))

        if input_point:
            self.exact_ans = f"At {input_variable} = {input_point}\n"

        if output_type == 1:
            self.exact_ans += str(pretty(derivative))
        elif output_type == 2:
            self.exact_ans += str(latex(derivative))
        else:
            self.exact_ans += str(derivative)

        return {"deriv": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @BaseWorker.catch_error
    @pyqtSlot()
    def calc_deriv(
        self,
        input_expression: str,
        input_variable: str,
        input_order: int,
        input_point: str,
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

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}

        try:
            self.exact_ans = diff(
                parse_expr(input_expression), parse_expr(input_variable), input_order
            )
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}
        self.latex_answer = str(latex(self.exact_ans))

        if input_point:
            calc_deriv_point = str(self.exact_ans).replace(
                input_variable, f"({input_point})"
            )

            if use_scientific:
                try:
                    self.approx_ans = self.to_scientific_notation(
                        str(N(calc_deriv_point, accuracy)), use_scientific
                    )
                except Exception:
                    return {"error": [f"Failed to parse {input_point}"]}
            else:
                try:
                    self.approx_ans = str(N(calc_deriv_point, accuracy))
                except Exception:
                    return {"error": [f"Failed to parse {input_point}"]}

            self.latex_answer = str(latex(simplify(calc_deriv_point)))
            if output_type == 1:
                self.exact_ans = str(pretty(simplify(calc_deriv_point)))
            elif output_type == 2:
                self.exact_ans = str(latex(simplify(calc_deriv_point)))
            else:
                self.exact_ans = str(simplify(calc_deriv_point))
        else:
            if output_type == 1:
                self.exact_ans = str(pretty(self.exact_ans))
            elif output_type == 2:
                self.exact_ans = str(latex(self.exact_ans))
            else:
                self.exact_ans = str(self.exact_ans)

        return {"deriv": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}


class DerivativeTab(QWidget):

    display_name = "Derivative"

    def __init__(self, main_window: "CASpyGUI") -> None:
        """
        A QWidget is created to be added in as a tab in the main window.

        :param main_window: class
            The main window class is passed on as a attribute to access its function and attributes such as exact_ans

        First the UI is loaded, then event filters are installed and bindings created.
        prev_deriv() and calc_deriv() calls the worker thread and the answer is set to the corresponding QTextBrowser.
        Every tab except the web tab works this way.
        """

        super().__init__()
        self.main_window = main_window
        loadUi(self.main_window.get_resource_path("qt_assets/tabs/derivative.ui"), self)
        self.eout: QTextBrowser = self.DerivOut
        self.aout: QTextBrowser = self.DerivApprox

        # Shortcuts
        cshortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        cshortcut.activated.connect(self.calc_deriv)
        pshortcut = QShortcut(QKeySequence("Ctrl+Shift+Return"), self)
        pshortcut.activated.connect(self.prev_deriv)
        self.init_bindings()

    def init_bindings(self) -> None:
        self.DerivPrev.clicked.connect(self.prev_deriv)
        self.DerivCalc.clicked.connect(self.calc_deriv)
        self.eout.mousePressEvent = lambda _: self.eout.selectAll()
        self.aout.mousePressEvent = lambda _: self.aout.selectAll()

    def stop_thread(self) -> None:
        pass

    def update_ui(self, input_dict: ty.Dict[str, ty.List[str]]) -> None:
        self.DerivOut.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.DerivApprox.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
            self.main_window.latex_text = ""
        else:
            self.main_window.latex_text = input_dict["latex"]
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.DerivOut.setText(self.main_window.exact_ans)
            self.DerivApprox.setText(str(self.main_window.approx_ans))

    def prev_deriv(self) -> None:
        self.DerivOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.DerivApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = DerivativeWorker(
            "prev_deriv",
            [
                self.DerivExp.toPlainText(),
                self.DerivVar.text(),
                self.DerivOrder.value(),
                self.DerivPoint.text(),
                self.main_window.output_type,
                self.main_window.use_unicode,
                self.main_window.line_wrap,
            ],
        )
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)

    def calc_deriv(self) -> None:
        self.DerivOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.DerivApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        worker = DerivativeWorker(
            "calc_deriv",
            [
                self.DerivExp.toPlainText(),
                self.DerivVar.text(),
                self.DerivOrder.value(),
                self.DerivPoint.text(),
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
