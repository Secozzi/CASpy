from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi

from worker import CASWorker

class DerivativeTab(QWidget):

    display_name = "Derivative"

    def __init__(self, main_window):
        """
        A QWidget is created to be added in as a tab in the main window.

        :param main_window: class
            The main window class is passed on as a attribute to access its function and attributes such as exact_ans

        First the UI is loaded, then event filters are installed and bindings created.
        prev_deriv() and calc_deriv() calls the worker thread and the answer is set to the corresponding QTextBrowser.
        Every tab except the web tab works this way.
        """

        super().__init__()
        loadUi("qt_assets/tabs/derivative.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.DerivExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        """
        Add modifiers and if shift + enter or shift + return is pressed, run calc_deriv()
        """
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')
        #if (QModifiers & Qt.AltModifier) == Qt.AltModifier:
        #    modifiers.append('alt')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.calc_deriv()
                        return True

            #if event.key() in (Qt.Key_E, Qt.Key_A):
            #    if modifiers:
            #        if modifiers[0] == 'alt':
            #            if event.key() == Qt.Key_E:
            #                self.main_window.view_exact_ans()
            #                return True
            #            else:
            #                self.main_window.view_approx_ans()
            #                return True

        return super(DerivativeTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.DerivPrev.clicked.connect(self.prev_deriv)
        self.DerivCalc.clicked.connect(self.calc_deriv)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
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

    def prev_deriv(self):
        self.WorkerCAS = CASWorker("prev_deriv", [
            self.DerivExp.toPlainText(),
            self.DerivVar.text(),
            self.DerivOrder.value(),
            self.DerivPoint.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def calc_deriv(self):
        self.WorkerCAS = CASWorker("calc_deriv", [
            self.DerivExp.toPlainText(),
            self.DerivVar.text(),
            self.DerivOrder.value(),
            self.DerivPoint.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)