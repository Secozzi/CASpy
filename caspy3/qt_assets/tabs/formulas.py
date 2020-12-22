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

from PyQt5.QtCore import pyqtSlot, QCoreApplication, QEvent, Qt
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QTreeWidgetItem,
    QWidget,
)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.uic import loadUi

import typing as ty

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

from .worker import BaseWorker


class FormulaWorker(BaseWorker):
    def __init__(self, command: str, params: list, copy: int = None) -> None:
        super().__init__(command, params, copy)

    @BaseWorker.catch_error
    @pyqtSlot()
    def prev_formula(
        self,
        lines: ty.List[list],
        value_string: ty.List[str],
        domain: str,
        output_type: int,
        use_unicode: bool,
        line_wrap: bool,
    ) -> ty.Dict[str, ty.List[str]]:
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        empty_var_list, var_list, values = [], [], []
        self.exact_ans = ""
        self.approx_ans = 0
        self.latex_answer = ""

        if not lines:
            return {"error": ["Error: select a formula"]}

        if type(value_string) == list:
            if len(value_string) != 2:
                return {"error": [f"Error: Unable to get equation from {value_string}"]}
        else:
            return {"error": [f"Error: Unable to get equation from {value_string}"]}

        for line in lines:
            if line[0].text() == "":
                empty_var_list.append(line[1])
            elif line[0].text() == "var":
                var_list.append(line[1])
            else:
                values.append([line[0].text(), line[1]])

        if len(var_list) > 1:
            return {
                "error": [
                    "Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"
                ]
            }

        if len(empty_var_list) > 1:
            if len(var_list) != 1:
                return {
                    "error": [
                        "Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"
                    ]
                }

        if len(var_list) == 1:
            final_var = var_list[0]
        else:
            final_var = empty_var_list[0]

        left_side = value_string[0]
        right_side = value_string[1]

        result = self.prev_normal_eq(
            left_side,
            right_side,
            final_var,
            domain,
            output_type,
            use_unicode,
            line_wrap,
        )
        return result

    @BaseWorker.catch_error
    @pyqtSlot()
    def calc_formula(
        self,
        lines: ty.List[list],
        value_string: ty.List[str],
        solve_type: int,
        domain: str,
        output_type: int,
        use_unicode: bool,
        line_wrap: bool,
        use_scientific: ty.Union[int, None],
        accuracy: int,
        verify_domain: bool,
        approximate: ty.Union[str, None],
    ) -> ty.Dict[str, ty.List[str]]:
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        empty_var_list, var_list, values = [], [], []
        self.exact_ans = ""
        self.approx_ans = 0
        self.latex_answer = "\\text{LaTeX support not yet implemented for formula}"

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not lines:
            return {"error": ["Error: select a formula"]}

        if type(value_string) == list:
            if len(value_string) != 2:
                return {"error": [f"Error: Unable to get equation from {value_string}"]}
        else:
            return {"error": [f"Error: Unable to get equation from {value_string}"]}

        for line in lines:
            if line[0].text() == "":
                empty_var_list.append(line[1])
            elif line[0].text() == "var":
                var_list.append(line[1])
            else:
                values.append([line[0].text(), line[1]])

        if len(var_list) > 1:
            return {
                "error": [
                    "Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"
                ]
            }

        if len(empty_var_list) > 1:
            if len(var_list) != 1:
                return {
                    "error": [
                        "Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"
                    ]
                }

        if len(var_list) == 1:
            final_var = var_list[0]
        else:
            final_var = empty_var_list[0]

        left_side = parse_expr(value_string[0])
        right_side = parse_expr(value_string[1])

        for i in values:
            left_side = left_side.subs(parse_expr(i[1]), i[0])
            right_side = right_side.subs(parse_expr(i[1]), i[0])

        left_side = str(left_side).replace("_i", "(sqrt(-1))")
        right_side = str(right_side).replace("_i", "(sqrt(-1))")

        result = self.calc_normal_eq(
            left_side,
            right_side,
            final_var,
            solve_type,
            domain,
            output_type,
            use_unicode,
            line_wrap,
            use_scientific,
            accuracy,
            verify_domain,
            approximate,
        )
        return result


class FormulaTab(QWidget):

    from sympy import Symbol, S
    from sympy.abc import _clash1

    display_name = "Formulas"

    def __init__(self, main_window: "CASpyGUI") -> None:
        super().__init__()
        self.main_window = main_window
        loadUi(self.main_window.get_resource_path("qt_assets/tabs/formulas.ui"), self)

        self.init_ui()

        if "verify_domain_formula" in list(self.main_window.settings_data.keys()):
            self.verify_domain_formula = self.main_window.settings_data[
                "verify_domain_formula"
            ]
        else:
            self.verify_domain_formula = False
        self.main_window.add_to_save_settings(
            {"verify_domain_formula": self.verify_domain_formula}
        )

        self.install_event_filter()
        self.init_formula_menu()
        self.init_bindings()
        self.add_formulas()

    def init_ui(self) -> None:
        self.FormulaTree.sortByColumn(0, Qt.AscendingOrder)
        self.grid_scroll_area = QGridLayout(self.FormulaScrollArea)
        self.grid_scroll_area.setObjectName("grid_scroll_area")

    def init_formula_menu(self) -> None:
        self.menuFormula = self.main_window.menubar.addMenu("Formulas")
        verify_domain_formula = QAction("Verify domain", self, checkable=True)
        verify_domain_formula.setChecked(self.verify_domain_formula)
        self.menuFormula.addAction(verify_domain_formula)
        verify_domain_formula.triggered.connect(self.toggle_verify_domain_formula)

    def toggle_verify_domain_formula(self, state: bool) -> None:
        if state:
            self.verify_domain_formula = True
        else:
            self.verify_domain_formula = False

        self.main_window.update_save_settings(
            {"verify_domain_formula": self.verify_domain_formula}
        )

    def install_event_filter(self) -> None:
        self.FormulaScrollArea.installEventFilter(self)

    def eventFilter(self, obj: "QObject", event: "QEvent") -> bool:
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append("shift")

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.calc_formula()
                        return True

        return super(FormulaTab, self).eventFilter(obj, event)

    def init_bindings(self) -> None:
        self.FormulaTree.itemDoubleClicked.connect(self.formula_tree_selected)
        self.FormulaPreview.clicked.connect(self.prev_formula)
        self.FormulaCalculate.clicked.connect(self.calc_formula)

        self.FormulaDomain.currentIndexChanged.connect(self.set_interval)
        self.FormulaNsolve.stateChanged.connect(self.approximate_state)

    def set_interval(self, index: int) -> None:
        if index >= 5:
            self.FormulaDomain.setEditable(True)
            # Update Font
            self.FormulaDomain.lineEdit().setFont(self.FormulaDomain.font())
        else:
            self.FormulaDomain.setEditable(False)
        self.FormulaDomain.update()

    def approximate_state(self) -> None:
        _state = self.FormulaNsolve.isChecked()
        self.FormulaStartV.setEnabled(_state)

    def add_formulas(self) -> None:
        self.formula_info_dict = self.main_window.formulas_data[0]
        self.formula_tree_data = self.main_window.formulas_data[1]

        for branch in self.formula_tree_data:
            parent = QTreeWidgetItem(self.FormulaTree)
            branch_name = str(list(branch.keys())[0])
            parent.setText(0, branch_name)

            for sub_branch in list(branch[branch_name].keys()):
                child = QTreeWidgetItem(parent)
                child.setText(0, sub_branch)

                for formula in branch[branch_name][sub_branch]:
                    formula_child = QTreeWidgetItem(child)
                    formula_child.setText(0, formula)

    def formula_tree_selected(self) -> None:
        """
        Retrieves formula and information about formula that user double clicked.
        Splits equation into left side of equals symbol and right side.
        Uses _i as imaginary unit instead of I and removes other similar functions/variables so they can be used as variables in formula.
        """
        get_selected = self.FormulaTree.selectedItems()
        if get_selected:
            base_node = get_selected[0]
            self.selected_tree_item = base_node.text(0)
            if "=" in self.selected_tree_item:
                expr = self.selected_tree_item.split("=")
                expr = list(map(lambda x: x.replace("_i", "(sqrt(-1))"), expr))
                self.formula_symbols_list = [
                    str(i)
                    for i in list(
                        self.S(expr[0], locals=self._clash1).atoms(self.Symbol)
                    )
                ]
                self.formula_symbols_list.extend(
                    (
                        str(i)
                        for i in list(
                            self.S(expr[1], locals=self._clash1).atoms(self.Symbol)
                        )
                    )
                )
                self.formula_symbols_list = list(set(self.formula_symbols_list))
                self.formula_symbols_list.sort()

                self.formula_update_vars()
                self.formula_info = self.formula_get_info(
                    self.selected_tree_item, self.formula_tree_data
                )
                self.formula_set_tool_tip()

    def formula_update_vars(self) -> None:
        for i in reversed(range(self.grid_scroll_area.count())):
            self.grid_scroll_area.itemAt(i).widget().setParent(None)
        self.formula_label_names = self.formula_symbols_list
        self.formula_label_pos = [[i, 0] for i in range(len(self.formula_label_names))]
        self.formula_line_pos = [[i, 1] for i in range(len(self.formula_label_names))]

        for self.formula_name_label, formula_pos_label, formula_pos_line in zip(
            self.formula_label_names, self.formula_label_pos, self.formula_line_pos
        ):
            self.formula_label = QLabel(self.FormulaScrollArea)
            self.formula_label.setText(self.formula_name_label)
            self.formula_label.setObjectName(self.formula_name_label + "line")
            self.grid_scroll_area.addWidget(self.formula_label, *formula_pos_label)
            self.formula_QLine = QLineEdit(self.FormulaScrollArea)
            self.formula_QLine.setFixedHeight(30)
            self.formula_QLine.setObjectName(self.formula_name_label + "line")
            self.formula_QLine.setFont(QFont("Courier New", 8))
            self.grid_scroll_area.addWidget(self.formula_QLine, *formula_pos_line)

    def formula_set_tool_tip(self) -> None:
        """
        Retrieves info from json file, set tooltip and set value of constants if needed
        """
        _translate = QCoreApplication.translate

        lines = []
        for name in self.formula_label_names:
            info = self.formula_info[name]

            if info in list(self.formula_info_dict.keys()):
                full_info = self.formula_info_dict[info]
            else:
                full_info = f"{info}|N/A|N/A"
            lines.append(
                [
                    self.FormulaScrollArea.findChild(QLineEdit, str(name) + "line"),
                    full_info,
                ]
            )

        for line in lines:
            info_list = line[1].split("|")

            name = info_list[0]
            unit_info = info_list[1]
            unit = info_list[2]

            if ";" in name:
                line[0].setText(name.split(";")[1])

            line[0].setToolTip(_translate("MainWindow", f"{unit_info}, mäts i {unit}"))

    def formula_get_info(self, text: str, data: dict) -> str:
        """
        Retrieves info that's correlated with given formula

        Parameters
        -------------
        text: string
            Formula whose information is requested.
        data: JSON file
            Data that stores formulas and respective information.

        Returns
        ------------
        formula[1]: string
            Information correlated to formula.
        """

        for branch in data:
            branch_name = str(list(branch.keys())[0])
            for sub_branch in list(branch[branch_name].keys()):
                if text in list(branch[branch_name][sub_branch].keys()):
                    return branch[branch_name][sub_branch][text]

    def stop_thread(self) -> None:
        pass

    def update_ui(self, input_dict: ty.Dict[str, ty.List[str]]) -> None:
        self.FormulaExact.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.FormulaApprox.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
            self.main_window.latex_text = ""
        else:
            self.main_window.latex_text = input_dict["latex"]
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.FormulaExact.setText(str(self.main_window.exact_ans))
            self.FormulaApprox.setText(str(self.main_window.approx_ans))

    def prev_formula(self) -> None:
        try:
            lines = [
                [self.FormulaScrollArea.findChild(QLineEdit, str(i) + "line"), i]
                for i in self.formula_label_names
            ]
        except:
            self.main_window.show_error_box("Error: select a formula")
        else:
            values_string = self.selected_tree_item.split("=")

            self.FormulaExact.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
            self.FormulaApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

            worker = FormulaWorker(
                "prev_formula",
                [
                    lines,
                    values_string,
                    self.FormulaDomain.currentText(),
                    self.main_window.output_type,
                    self.main_window.use_unicode,
                    self.main_window.line_wrap,
                ],
            )
            worker.signals.output.connect(self.update_ui)
            worker.signals.finished.connect(self.stop_thread)

            self.main_window.threadpool.start(worker)

    def calc_formula(self) -> None:
        if self.FormulaSolveSolve.isChecked():
            solve_type = 2
        if self.FormulaSolveSolveSet.isChecked():
            solve_type = 1

        try:
            lines = [
                [self.FormulaScrollArea.findChild(QLineEdit, str(i) + "line"), i]
                for i in self.formula_label_names
            ]
            values_string = self.selected_tree_item.split("=")
        except:
            self.main_window.show_error_box("Error: select a formula")
            return

        self.FormulaExact.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))
        self.FormulaApprox.viewport().setProperty("cursor", QCursor(Qt.WaitCursor))

        if self.FormulaNsolve.isChecked():
            _start = self.FormulaStartV.text()
        else:
            _start = None

        worker = FormulaWorker(
            "calc_formula",
            [
                lines,
                values_string,
                solve_type,
                self.FormulaDomain.currentText(),
                self.main_window.output_type,
                self.main_window.use_unicode,
                self.main_window.line_wrap,
                self.main_window.use_scientific,
                self.main_window.accuracy,
                self.verify_domain_formula,
                _start,
            ],
        )
        worker.signals.output.connect(self.update_ui)
        worker.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(worker)
