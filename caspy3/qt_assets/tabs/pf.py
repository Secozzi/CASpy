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

from PyQt5.QtCore import pyqtSlot, QRegExp, Qt
from PyQt5.QtWidgets import QShortcut, QWidget
from PyQt5.QtGui import QCursor, QKeySequence, QRegExpValidator
from PyQt5.uic import loadUi

import typing as ty

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

import traceback

from .worker import BaseWorker


class PfWorker(BaseWorker):
    def __init__(self, command: str, params: list, copy: int = None) -> None:
        super().__init__(command, params, copy)

    @BaseWorker.catch_error
    @pyqtSlot()
    def calc_pf(self, input_number: int) -> ty.Dict[str, ty.List[str]]:
        self.approx_ans = ""
        self.latex_answer = ""

        try:
            input_number = int(input_number)
        except:
            return {"error": [f"Error: {input_number} is not an integer."]}

        if input_number < 2:
            return {
                "error": [
                    f"Error: {input_number} is lower than 2, only number 2 and above is accepted."
                ]
            }

        try:
            self.exact_ans = factorint(input_number)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        for base in self.exact_ans:
            self.latex_answer += f"({base}**{self.exact_ans[base]})*"
            self.approx_ans += f"({base}**{self.exact_ans[base]})*"

        self.latex_answer = latex(parse_expr(self.latex_answer[0:-1], evaluate=False))
        return {
            "pf": [self.exact_ans, self.approx_ans[0:-1]],
            "latex": self.latex_answer,
        }


class PfTab(QWidget):
    display_name = "Prime Factors"

    def __init__(self, main_window: "CASpyGUI") -> None:
        super().__init__()
        self.main_window = main_window
        loadUi(self.main_window.get_resource_path("qt_assets/tabs/pf.ui"), self)
        self.eout = self.PfOut
        self.aout = self.PfApprox

        # Shortcuts
        cshortcut = QShortcut(QKeySequence("Shift+Return"), self)
        cshortcut.activated.connect(self.calc_pf)

        self.init_menu()
        self.init_bindings()

    def init_menu(self) -> None:
        self.number_reg = QRegExp("[0-9]+")
        self.number_reg_validator = QRegExpValidator(self.number_reg, self)

        self.PfInput.setValidator(self.number_reg_validator)

    def init_bindings(self) -> None:
        self.PfCalc.clicked.connect(self.calc_pf)
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
        self.PfOut.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.PfApprox.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
            self.main_window.latex_text = ""
        else:
            self.main_window.latex_text = input_dict["latex"]
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.PfOut.setText(self.main_window.exact_ans)
            self.PfApprox.setText(self.main_window.approx_ans)

    def calc_pf(self) -> None:
        self.PfOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.PfApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        number = int(self.PfInput.text())
        worker = PfWorker("calc_pf", [number])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)
