from PyQt5.QtCore import pyqtSlot, QRegExp, Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QCursor, QRegExpValidator
from PyQt5.uic import loadUi

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

import traceback

from worker import BaseWorker


class PfWorker(BaseWorker):
    def __init__(self, command, params, copy=None):
        super().__init__(command, params, copy)

    @BaseWorker.catch_error
    @pyqtSlot()
    def calc_pf(self, input_number):
        self.approx_ans = ""
        self.latex_answer = ""

        try:
            input_number = int(input_number)
        except:
            return {"error": [f"Error: {input_number} is not an integer."]}

        if input_number < 2:
            return {"error": [f"Error: {input_number} is lower than 2, only number 2 and above is accepted."]}

        try:
            self.exact_ans = factorint(input_number)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        for base in self.exact_ans:
            self.latex_answer += f"({base}**{self.exact_ans[base]})*"
            self.approx_ans += f"({base}**{self.exact_ans[base]})*"

        self.latex_answer = latex(parse_expr(self.latex_answer[0:-1], evaluate=False))
        return {"pf": [self.exact_ans, self.approx_ans[0:-1]], "latex": self.latex_answer}


class PfTab(QWidget):
    display_name = "Prime Factors"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/pf.ui", self)
        self.main_window = main_window
        self.init_menu()
        self.init_bindings()

    def init_menu(self):
        self.number_reg = QRegExp("[0-9]+")
        self.number_reg_validator = QRegExpValidator(self.number_reg, self)

        self.PfInput.setValidator(self.number_reg_validator)

    def init_bindings(self):
        self.PfCalc.clicked.connect(self.calc_pf)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
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

    def calc_pf(self):
        self.PfOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.PfApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        number = int(self.PfInput.text())
        worker = PfWorker("calc_pf", [number])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)