from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QAction, QApplication, QGridLayout, QLabel, QLineEdit, QWidget
from PyQt5.uic import loadUi

from worker import CASWorker

class EquationsTab(QWidget):

    display_name = "Equation Solver"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/equations.ui", self)
        self.main_window = main_window
        self.verify_domain = self.main_window.settings_data["verify_domain"]
        self.main_window.add_to_save_settings({"verify_domain": self.verify_domain})

        self.init_ui()
        self.init_equation_menu()
        self.install_event_filters()
        self.init_bindings()
        self.update_eq_line()

    def init_ui(self):
        self.EqSysGridArea = QGridLayout(self.EqSysScroll)
        self.EqSysGridArea.setObjectName("EqSysGridArea")

    def init_equation_menu(self):
        self.menuEq = self.main_window.menubar.addMenu("Equations")
        verify_domain = QAction("Verify domain", self, checkable=True)
        verify_domain.setChecked(self.verify_domain)
        self.menuEq.addAction(verify_domain)
        verify_domain.triggered.connect(self.toggle_verify_domain)

    def toggle_verify_domain(self, state):
        if state:
            self.verify_domain = True
        else:
            self.verify_domain = False

        self.main_window.add_to_save_settings({"verify_domain": self.verify_domain})

    def install_event_filters(self):
        self.EqNormalLeft.installEventFilter(self)
        self.EqNormalRight.installEventFilter(self)
        self.EqDiffLeft.installEventFilter(self)
        self.EqDiffRight.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.calc_eq()
                        return True

        return super(EquationsTab, self).eventFilter(obj, event)

    def init_bindings(self):
        # Setting up buttons for selecting equation mode
        self.normalNormal.setChecked(True)
        self.EqNormalDomain.currentIndexChanged.connect(self.set_interval)

        for normal_btn in [self.normalNormal, self.diffNormal, self.systemNormal]:
            normal_btn.clicked.connect(lambda: self.set_eq_state([self.normalDiff, self.normalSystem], 0, self.normalNormal))

        for diff_btn in [self.normalDiff, self.diffDiff, self.systemDiff]:
            diff_btn.clicked.connect(lambda: self.set_eq_state([self.diffNormal, self.diffSystem], 1, self.diffDiff))

        for system_btn in [self.normalSystem, self.diffSystem, self.systemSystem]:
            system_btn.clicked.connect(lambda: self.set_eq_state([self.systemNormal, self.systemDiff], 2, self.systemSystem))

        # Connect prev and calc buttons
        self.EqPrev.clicked.connect(self.prev_eq)
        self.EqCalc.clicked.connect(self.calc_eq)

        # Connect spinbox
        self.EqSysNo.valueChanged.connect(self.update_eq_line)

    def set_interval(self, index):
        if index >= 5:
            self.EqNormalDomain.setEditable(True)
            # Update Font
            self.EqNormalDomain.lineEdit().setFont(self.EqNormalDomain.font())
        else:
            self.EqNormalDomain.setEditable(False)
        self.EqNormalDomain.update()

    def set_eq_state(self, btn_list, stacked_index, btn_true):
        """
        :param btn_list: list
            List of buttons to set to false.
        :param stacked_index: int
            Sets the stacked widget to index
        :param btn_true: QPushButton
            Button to set to True
        :return:
        """
        self.eqStackedWidget.setCurrentIndex(stacked_index)
        btn_true.setChecked(True)
        for btn in btn_list:
            btn.setChecked(False)

    def update_eq_line(self):

        for i in reversed(range(self.EqSysGridArea.count())):
            self.EqSysGridArea.itemAt(i).widget().setParent(None)
        no_of_eq = self.EqSysNo.value()
        for i in range(no_of_eq):
            self.SysEqLabel = QLabel(self.EqSysScroll)
            self.SysEqLabel.setText(f"Eq. {i+1}")
            self.SysEqLabel.setObjectName(f"label_{i}")
            self.EqSysGridArea.addWidget(self.SysEqLabel, i, 0)

            self.SysEqLine = QLineEdit(self.EqSysScroll)
            self.SysEqLine.setObjectName(f"line_{i}")
            self.SysEqLine.setFixedHeight(25)
            self.EqSysGridArea.addWidget(self.SysEqLine, i, 1)

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

            self.EqOut.setText(self.main_window.exact_ans)
            self.EqApprox.setText(str(self.main_window.approx_ans))

    def prev_eq(self):
        current_index = self.eqStackedWidget.currentIndex()
        if current_index == 0:
            self.prev_normal_eq()
        elif current_index == 1:
            self.prev_diff_eq()
        else:
            self.prev_system_eq()

    def calc_eq(self):
        current_index = self.eqStackedWidget.currentIndex()
        if current_index == 0:
            self.calc_normal_eq()
        elif current_index == 1:
            self.calc_diff_eq()
        else:
            self.calc_system_eq()

    #  def calc_normal_eq(self, left_expression, right_expression, input_variable, solve_type, domain, output_type, use_unicode, line_wrap, use_scientific, accuracy):
    def calc_normal_eq(self):
        if self.EqNormalSolve.isChecked():
            solve_type = 2
        if self.EqNormalSolveSet.isChecked():
            solve_type = 1

        self.WorkerCAS = CASWorker("calc_normal_eq", [
            self.EqNormalLeft.toPlainText(),
            self.EqNormalRight.toPlainText(),
            self.EqNormalVar.text(),
            solve_type,
            self.EqNormalDomain.currentText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy,
            self.verify_domain
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    # def calc_diff_eq(self, left_expression, right_expression, function_solve, output_type, use_unicode, line_wrap, use_scientific, accuracy):
    def calc_diff_eq(self):
        self.WorkerCAS = CASWorker("calc_diff_eq", [
            self.EqDiffLeft.toPlainText(),
            self.EqDiffRight.toPlainText(),
            self.EqDiffHint.text(),
            self.EqDiffFunc.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])

        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)
        #print(self.EqDiffLeft.toPlainText())
        #print(self.EqDiffRight.toPlainText())

    def calc_system_eq(self):
        print(self.EqSysNo.value())

    def prev_normal_eq(self):
        self.WorkerCAS = CASWorker("prev_normal_eq", [
            self.EqNormalLeft.toPlainText(),
            self.EqNormalRight.toPlainText(),
            self.EqNormalVar.text(),
            self.EqNormalDomain.currentText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def prev_diff_eq(self):
        self.WorkerCAS = CASWorker("prev_diff_eq", [
            self.EqDiffLeft.toPlainText(),
            self.EqDiffRight.toPlainText(),
            self.EqDiffFunc.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def prev_system_eq(self):
        print(self.EqSysNo.value())