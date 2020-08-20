from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QCursor
from PyQt5.uic import loadUi

from worker import CASWorker

class LimitTab(QWidget):

    display_name = "Limit"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/limit.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.LimExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.calc_limit()
                        return True

        return super(LimitTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.LimPrev.clicked.connect(self.prev_limit)
        self.LimCalc.clicked.connect(self.calc_limit)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        self.LimOut.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.LimApprox.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
            self.main_window.latex_text = ""
        else:
            self.main_window.latex_text = input_dict["latex"]
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.LimOut.setText(self.main_window.exact_ans)
            self.LimApprox.setText(str(self.main_window.approx_ans))

    def prev_limit(self):
        self.LimOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.LimApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        if self.LimSide.currentIndex() == 0:
            limit_side = "+-"
        elif self.LimSide.currentIndex() == 1:
            limit_side = "-"
        else:
            limit_side = "+"

        self.WorkerCAS = CASWorker("prev_limit", [
            self.LimExp.toPlainText(),
            self.LimVar.text(),
            self.LimApproach.text(),
            limit_side,
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def calc_limit(self):
        self.LimOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.LimApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        if self.LimSide.currentIndex() == 0:
            limit_side = "+-"
        elif self.LimSide.currentIndex() == 1:
            limit_side = "-"
        else:
            limit_side = "+"

        self.WorkerCAS = CASWorker("calc_limit", [
            self.LimExp.toPlainText(),
            self.LimVar.text(),
            self.LimApproach.text(),
            limit_side,
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)