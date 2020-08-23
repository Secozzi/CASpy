from PyQt5.QtCore import pyqtSlot, QEvent, Qt
from PyQt5.QtWidgets import QAction, QApplication, QGridLayout, QLabel, QLineEdit, QWidget
from PyQt5.QtGui import QCursor, QFont
from PyQt5.uic import loadUi

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

import traceback

import re as pyreg

from worker import BaseWorker


class EquationsWorker(BaseWorker):
    def __init__(self, command, params, copy=None):
        super().__init__(command, params, copy)

    @BaseWorker.catch_error
    @pyqtSlot()
    def prev_diff_eq(self, left_expression, right_expression, function_solve, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)

        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if "=" in left_expression:
            if left_expression.count("=") > 1:
                return {"error": ["Enter only one equals sign"]}
            else:
                eq = left_expression.split("=")
                try:
                    left_side = parse_expr(self.parse_diff_text(eq[0]))
                    right_side = parse_expr(self.parse_diff_text(eq[1]))
                except Exception:
                    return {"error": [f"Error: \n{traceback.format_exc()}"]}
        else:
            if not left_expression or not right_expression:
                return {"error": ["Enter an expression both in left and right side"]}

            try:
                left_side = parse_expr(self.parse_diff_text(left_expression))
                right_side = parse_expr(self.parse_diff_text(right_expression))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

        if not function_solve:
            return {"error": ["Enter a function to solve for"]}

        try:
            function_solve = parse_expr(function_solve)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        try:
            full_equation = Eq(left_side, right_side)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        self.latex_answer = str(latex(full_equation))

        if output_type == 1:
            self.exact_ans = str(pretty(full_equation))
        elif output_type == 2:
            self.exact_ans = self.latex_answer
        else:
            self.exact_ans = self.eq_to_text(full_equation)

        try:
            self.exact_ans += f"\nClassification: {str(classify_ode(full_equation))}"
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @BaseWorker.catch_error
    @pyqtSlot()
    def prev_system_eq(self, equations, variables, domain, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)

        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        equations = self.get_equations(equations)
        if equations[0] == "error":
            return {"error": [f"Error: \nEnter only one '=' on line {equations[1] + 1}"]}
        if equations[0] == "traceback":
            return {"error": [f"Error: \nEquation number {equations[1] + 1} is invalid"]}

        variables = self.get_vars(variables)
        if variables[0] == "error":
            return {"error": [f"Error: \n{variables[1]}"]}

        try:
            domain = parse_expr(domain)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        self.exact_ans = f"Domain: {domain}\n\n"

        for eq in equations:
            if output_type == 1:
                self.exact_ans += str(pretty(eq)) + "\n\n"
            elif output_type == 2:
                self.exact_ans += str(latex(eq)) + "\n\n"
            else:
                self.exact_ans += self.eq_to_text(eq) + "\n\n"

        for eq in equations:
            self.latex_answer += str(latex(eq)) + " \\ "

        self.exact_ans += f"Variables to solve for: {variables}"
        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer[:-3]}

    @BaseWorker.catch_error
    @pyqtSlot()
    def calc_diff_eq(self, left_expression, right_expression, hint, function_solve,
                     output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        try:
            if "=" in left_expression:
                if left_expression.count("=") > 1:
                    return {"error": ["Enter only one equals sign"]}
                else:
                    eq = left_expression.split("=")
                    left_side = parse_expr(self.parse_diff_text(eq[0]))
                    right_side = parse_expr(self.parse_diff_text(eq[1]))
            else:
                if not left_expression or not right_expression:
                    return {"error": ["Enter an expression both in left and right side"]}

                left_side = parse_expr(self.parse_diff_text(left_expression))
                right_side = parse_expr(self.parse_diff_text(right_expression))
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        if not function_solve:
            return {"error": ["Enter a function"]}

        try:
            function_solve = parse_expr(function_solve)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        if not hint:
            hint = 'default'

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        diffeq = Eq(left_side, right_side)

        try:
            self.exact_ans = dsolve(diffeq, function_solve, hint=hint)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        self.latex_answer = str(latex(self.exact_ans))

        if type(self.exact_ans) != list:
            self.exact_ans = [self.exact_ans]

        approx_list = [N(i, accuracy) for i in self.exact_ans]
        if use_scientific:
            return {"error": ["Scientific notation not supported for differential equations"]}

        self.approx_ans = approx_list[0] if len(approx_list) == 1 else approx_list

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
            self.approx_ans = str(pretty(self.approx_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
            self.approx_ans = str(latex(self.approx_ans))
        else:
            self.exact_ans = str(self.exact_ans)
            self.approx_ans = str(self.approx_ans)

        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @BaseWorker.catch_error
    @pyqtSlot()
    def calc_system_eq(self, equations, variables, domain, output_type,
                       use_unicode, line_wrap, use_scientific, accuracy, verify_domain):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = []
        self.exact_ans = []
        self.latex_answer = ""

        equations = self.get_equations(equations)
        if equations[0] == "error":
            return {"error": [f"Error: \nEnter only one '=' on line {equations[1] + 1}"]}
        if equations[0] == "traceback":
            return {"error": [f"Error: \nEquation number {equations[1] + 1} is invalid"]}

        variables = self.get_vars(variables)
        if variables[0] == "error":
            return {"error": [f"Error: \n{variables[1]}"]}

        try:
            domain = parse_expr(domain)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        try:
            result = solve(equations, variables, set=True)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        if not result:
            return {"error": [f"Invalid variables"]}

        var_list = result[0]
        solutions = list(result[1])

        for i, sol_list in enumerate(solutions):
            temp_sol = []
            temp_approx = []

            if verify_domain:
                sol_list_len = len(sol_list)
                sol_list = tuple(self.verify_domain(sol_list, domain))
                if len(sol_list) != sol_list_len:
                    sol_list = []

            approx_list = [N(j, accuracy) for j in sol_list]

            if use_scientific:
                approx_list = [self.to_scientific_notation(str(i), use_scientific) for i in approx_list]

            for j, sol in enumerate(sol_list):
                temp_sol.append(Eq(var_list[j], sol))

            for j, sol in enumerate(approx_list):
                temp_approx.append(f"{var_list[j]} = {sol}")

            if sol_list:
                self.exact_ans.append(temp_sol)
                self.approx_ans.append(temp_approx)

        temp_out = ""
        for i in self.exact_ans:
            temp_out += str(latex(i))
            temp_out += r" \\ "

        self.latex_answer = temp_out[:-4]

        if output_type == 1:
            temp_out = ""
            for i in self.exact_ans:
                temp_out += str(pretty(i))
                temp_out += "\n\n"

            self.exact_ans = temp_out
        elif output_type == 2:
            temp_out = ""
            for i in self.exact_ans:
                temp_out += str(latex(i))
                temp_out += r" \\ "

            self.exact_ans = temp_out
        else:
            self.exact_ans = str(self.exact_ans)

        self.approx_ans = self.approx_ans[0] if len(self.approx_ans) == 1 else self.approx_ans

        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @BaseWorker.catch_error
    @pyqtSlot()
    def get_equations(self, equations):
        """
        Each equation is to be typed as 'expr1 = expr2'.
        This checks that exactly one '=' is present and if not, show error box and return "error"
        :param equations: list
            List of all equations as strings
        :return: list
            Returns list of SymPy Eq()
        """
        eq = []

        for line in equations:
            if line.count("=") != 1:
                return ["error", equations.index(line)]
            line_equal = line.split("=")
            try:
                eq.append(Eq(parse_expr(line_equal[0]), parse_expr(line_equal[1])))
            except Exception:
                return ["traceback", equations.index(line)]
        return eq

    @BaseWorker.catch_error
    @pyqtSlot()
    def get_vars(self, var_text):
        """
        Return vars that is separated by anything other than a-z, 0-9, and _
        :param var_text: str
            Text of QLineEdit
        :return: list
            Returns list of SymPified symbols
        """

        var_re = pyreg.compile(r"[a-zA-Z0-9_]+")
        vars = var_re.findall(var_text)
        output = []
        for var in vars:
            try:
                output.append(parse_expr(var))
            except Exception:
                return ["error", traceback.format_exc()]
        if not output:
            return ["error", "Please enter at least one variable"]
        return output

    @BaseWorker.catch_error
    @pyqtSlot()
    def parse_diff_text(self, text):
        """
        Catches all derivatives and transforms it so SymPy can read it.
        No nested functions because no.
        Function already in SymPy syntax (Ex. 'f(x).diff(x,3)') will be ignored.
        Examples (Not what function will return, just how it transforms functions)
            f'''(x)
            => f(x).diff(x,3)

            f''(x, y, z)
            => f(x, y, z).diff(x,2,y,2,z,2)

        :param text: str
            String to be parsed
        :return: str
            String with transformed derivatives
        """

        diff_functions = pyreg.compile(r"(?:[a-zA-Z])+('+)\(.*?\)")
        inside_params = pyreg.compile(r"(?<=\().+?(?=\))")
        quotations = pyreg.compile(r"'+(?=\()")

        functions = diff_functions.finditer(text)

        for function in functions:
            output = ""
            func_str = function.group(0)
            inside_param = inside_params.search(func_str).group(0)
            order = len(function.group(1))
            function_no_order = quotations.sub("", func_str)

            inside_param = inside_param.strip(" ")
            vars = [i.strip() for i in inside_param.split(",")]

            output += f"{function_no_order}.diff("
            for var in vars:
                output += f"{var},{order},"

            output = output[:-1]
            output += ")"

            text = text.replace(func_str, output)

        return text


class EquationsTab(QWidget):

    display_name = "Equation Solver"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/equations.ui", self)
        self.main_window = main_window

        if "verify_domain_eq" in list(self.main_window.settings_data.keys()):
            self.verify_domain_eq = self.main_window.settings_data["verify_domain_eq"]
        else:
            self.verify_domain_eq = False
        self.main_window.add_to_save_settings({"verify_domain_eq": self.verify_domain_eq})

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
        verify_domain_eq = QAction("Verify domain", self, checkable=True)
        verify_domain_eq.setChecked(self.verify_domain_eq)
        self.menuEq.addAction(verify_domain_eq)
        verify_domain_eq.triggered.connect(self.toggle_verify_domain_eq)

    def toggle_verify_domain_eq(self, state):
        if state:
            self.verify_domain_eq = True
        else:
            self.verify_domain_eq = False

        self.main_window.update_save_settings({"verify_domain_eq": self.verify_domain_eq})

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
        self.EqNormalDomain.currentIndexChanged.connect(self.set_normal_interval)
        self.EqSysDomain.currentIndexChanged.connect(self.set_sys_interval)

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

    def set_normal_interval(self, index):
        if index >= 5:
            self.EqNormalDomain.setEditable(True)
            # Update Font
            self.EqNormalDomain.lineEdit().setFont(self.EqNormalDomain.font())
        else:
            self.EqNormalDomain.setEditable(False)
        self.EqNormalDomain.update()

    def set_sys_interval(self, index):
        if index >= 5:
            self.EqSysDomain.setEditable(True)
            # Update Font
            self.EqSysDomain.lineEdit().setFont(self.EqSysDomain.font())
        else:
            self.EqSysDomain.setEditable(False)
        self.EqSysDomain.update()

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
        self.eq_sys_line_list = []

        # Clear the GridArea
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
            self.SysEqLine.setFont(QFont("Courier New", 8))
            self.eq_sys_line_list.append(self.SysEqLine)
            self.EqSysGridArea.addWidget(self.SysEqLine, i, 1)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        self.EqOut.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.EqApprox.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))

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
        self.EqOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.EqApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        current_index = self.eqStackedWidget.currentIndex()
        if current_index == 0:
            self.prev_normal_eq()
        elif current_index == 1:
            self.prev_diff_eq()
        else:
            self.prev_system_eq()

    def calc_eq(self):
        self.EqOut.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.EqApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        current_index = self.eqStackedWidget.currentIndex()
        if current_index == 0:
            self.calc_normal_eq()
        elif current_index == 1:
            self.calc_diff_eq()
        else:
            self.calc_system_eq()

    def calc_normal_eq(self):
        if self.EqNormalSolve.isChecked():
            solve_type = 2
        if self.EqNormalSolveSet.isChecked():
            solve_type = 1

        worker = EquationsWorker("calc_normal_eq", [
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
            self.verify_domain_eq
        ])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)

    def calc_diff_eq(self):
        worker = EquationsWorker("calc_diff_eq", [
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

        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)

    def calc_system_eq(self):
        equations = [line.text() for line in self.eq_sys_line_list]
        vars = self.EqSysVar.text()

        worker = EquationsWorker("calc_system_eq", [
            equations,
            vars,
            self.EqSysDomain.currentText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy,
            self.verify_domain_eq
        ])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)

    def prev_normal_eq(self):
        worker = EquationsWorker("prev_normal_eq", [
            self.EqNormalLeft.toPlainText(),
            self.EqNormalRight.toPlainText(),
            self.EqNormalVar.text(),
            self.EqNormalDomain.currentText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)

    def prev_diff_eq(self):
        worker = EquationsWorker("prev_diff_eq", [
            self.EqDiffLeft.toPlainText(),
            self.EqDiffRight.toPlainText(),
            self.EqDiffFunc.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)

    def prev_system_eq(self):
        equations = [line.text() for line in self.eq_sys_line_list]
        vars = self.EqSysVar.text()

        worker = EquationsWorker("prev_system_eq", [
            equations,
            vars,
            self.EqSysDomain.currentText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])

        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)