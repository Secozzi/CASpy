from PyQt5.QtCore import QRegExp , Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QCursor, QRegExpValidator
from PyQt5.uic import loadUi

from worker import CASWorker

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
        self.WorkerCAS = CASWorker("calc_pf", [number])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)