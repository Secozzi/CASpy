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

# PyQt5
from PyQt5.QtCore import (
    pyqtSignal,
    pyqtSlot,
    QObject,
    QRunnable,
    QSize,
    Qt,
)
from PyQt5.QtWidgets import (
    QAction,
    QGridLayout,
    QLabel,
    QLineEdit,
    QShortcut,
    QTreeWidgetItem,
    QWidget,
)
from PyQt5.QtGui import (
    QCursor,
    QFont,
    QKeySequence,
    QPixmapCache,
)
from PyQt5.uic import loadUi

# Misc
import typing as ty
import re as pyreg

# SymPy
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

# matplotlib
import matplotlib.pyplot as mpl

# Relative
from .worker import BaseWorker
from .drag_label import DragLabel
from .latex import mathTex_to_QPixmap


class LaTeXSignals(QObject):
    finished = pyqtSignal()
    current = pyqtSignal(int)
    output = pyqtSignal(list)


class LaTeXWorker(QRunnable):
    def __init__(self, latex_list, fig):
        super(LaTeXWorker, self).__init__()

        self.latex_list = latex_list
        self.fig = fig

        self.signals = LaTeXSignals()

    @pyqtSlot()
    def run(self) -> None:
        out = []
        for i, formula in enumerate(self.latex_list):
            expr = formula.split("=")

            left = parse_expr(expr[0], evaluate=False)
            right = parse_expr(expr[1], evaluate=False)
            latex_pixmap = mathTex_to_QPixmap(
                f"${latex(Eq(left, right))}$",
                15,
                fig=self.fig,
            )

            out.append(latex_pixmap)
            self.signals.current.emit(i)

        self.signals.output.emit(out)
        self.signals.finished.emit()


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

        cshortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        cshortcut.activated.connect(self.calc_formula)
        pshortcut = QShortcut(QKeySequence("Ctrl+Shift+Return"), self)
        pshortcut.activated.connect(self.prev_formula)

        self.info = self.main_window.formulas_data[0]
        self.data = self.main_window.formulas_data[1]

        # TODO
        self.use_latex = True
        self.imag = pyreg.compile("\b_i\b")

        self.fig = mpl.figure()
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

        self.init_formula_menu()
        self.init_bindings()
        self.add_formulas()

    def init_ui(self) -> None:
        self.FormulaTree.sortByColumn(0, Qt.AscendingOrder)
        self.grid_scroll_area = QGridLayout(self.FormulaScrollArea)
        self.grid_scroll_area.setObjectName("grid_scroll_area")
        self.splitter_2.setSizes([int(self.height() * 0.45), int(self.height() * 0.55)])

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

    def init_bindings(self) -> None:
        self.FormulaTree.itemDoubleClicked.connect(self.formula_tree_selected)
        self.FormulaTree.itemExpanded.connect(self.expanded_sub)
        self.FormulaTree.itemCollapsed.connect(self.collapsed_sub)

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
        """
        Create QTreeWidgetItems and QLabels
        """
        for branch in self.data:
            parent = QTreeWidgetItem(self.FormulaTree)
            parent.setText(0, branch)

            for sub_branch in self.data[branch]:
                child = QTreeWidgetItem(parent)
                child.setText(0, sub_branch)

                for formula in self.data[branch][sub_branch]:
                    formula_child = QTreeWidgetItem(child)
                    formula_label = DragLabel(self, formula)

                    formula_label.setObjectName(f"{formula}")
                    if not self.use_latex:
                        formula_label.setText(formula)
                    self.FormulaTree.setItemWidget(formula_child, 0, formula_label)

    def expanded_sub(self, item):
        # Collapse everything else
        if self.use_latex:
            root = self.FormulaTree.invisibleRootItem()
            for i in range(root.childCount()):
                branch = root.child(i)
                for j in range(branch.childCount()):
                    sub_branch = branch.child(j)
                    if sub_branch != item:
                        self.FormulaTree.collapseItem(sub_branch)

            # Get formulas and start worker
            if item.parent():
                formulas = [
                    self.FormulaTree.itemWidget(item.child(i), 0).objectName()
                    for i in range(item.childCount())
                ]
                formulas = [self.imag.sub("(sqrt(-1))", f) for f in formulas]
                title = item.text(0)
                total = len(formulas)

                worker = LaTeXWorker(formulas, fig=self.fig)
                worker.signals.current.connect(
                    lambda current: self.update_current(current, total, title, item)
                )
                worker.signals.output.connect(lambda output: self.set_pixmap(output, item))
                worker.signals.finished.connect(lambda: item.setText(0, title))

                self.main_window.threadpool.start(worker)

    def collapsed_sub(self, item):
        """
        In order to save memory, LaTeX QPixmaps are generated when shown
        and cleared once the user clicks on another sub-branch.

        :param item: QTreeWidgetItem
            The item the user clicked at
        :return:
        """
        if self.use_latex:
            if item.parent():
                for i in range(item.childCount()):
                    qlabel = self.FormulaTree.itemWidget(item.child(i), 0)
                    qlabel.clear()

            QPixmapCache.clear()

    def update_current(self, curr, total, title, item):
        """
        Updates title of sub-branch

        :param curr: int
            Index of the LaTeX image being processed
        :param total: int
            Total number of formulas to be processed
        :param title: str
            Title of sub-branch
        :param item: QTreeWidgetItem
            QTreeWidgetItem being expanded
        """
        item.setText(
            0, f"{title} - Generating LaTeX [{curr}/{total}] {int((curr/total)*100)}%"
        )

    def set_pixmap(self, qp_list, item):
        """
        Sets pixmaps to respective QLabels

        :param qp_list: list
            List of QPixmaps
        :param item: QTreeWidgetItem
            QTreeWidgetItem being expanded
        """
        for i in range(item.childCount()):
            pixmap = qp_list[i]

            qlabel = self.FormulaTree.itemWidget(item.child(i), 0)
            item.child(i).setSizeHint(
                0, QSize(self.FormulaTree.width(), pixmap.height())
            )
            qlabel.setPixmap(pixmap)
        self.FormulaTree.updateGeometries()
        QPixmapCache.clear()

    def formula_tree_selected(self):
        """
        Retrieve symbols from formula.
        self.formula_symbol_list contains strings of symbols
        """
        selected = self.FormulaTree.selectedItems()
        if selected:
            widget = selected[0]
            qlabel = self.FormulaTree.itemWidget(widget, 0)

            formula = qlabel.objectName()
            formula = self.imag.sub("(sqrt(-1))", formula)
            expr = formula.split("=")

            self.formula_symbol_list = [
                list(i)
                for i in [
                    self.S(expr[j], locals=self._clash1).atoms(self.Symbol)
                    for j in (0, 1)
                ]
            ]
            self.formula_symbol_list = [
                str(i) for j in self.formula_symbol_list for i in j
            ]
            self.formula_symbol_list.sort()

            self.formula_update_vars()
            self.formula_info = self.formula_get_info(
                qlabel.objectName(), self.data
            )
            self.formula_set_tool_tip()

    def formula_update_vars(self):
        """
        Clear QScrollArea, then set a Qlabel and QLineEdit
        for every symbol present in the formula.
        """
        for i in reversed(range(self.grid_scroll_area.count())):
            self.grid_scroll_area.itemAt(i).widget().setParent(None)

        for i in range(len(self.formula_symbol_list)):
            symbol = self.formula_symbol_list[i]
            self.formula_label = QLabel(self.FormulaScrollArea)
            self.formula_label.setText(symbol)
            self.formula_label.setObjectName(symbol + "label")
            self.formula_label.setFont(QFont("Courier New", 8))

            self.formula_qline = QLineEdit(self.FormulaScrollArea)
            self.formula_qline.setFixedHeight(30)
            self.formula_qline.setObjectName(symbol + "line")
            self.formula_qline.setFont(QFont("Courier New", 8))

            self.grid_scroll_area.addWidget(self.formula_label, i, 0)
            self.grid_scroll_area.addWidget(self.formula_qline, i, 1)

    def formula_set_tool_tip(self):
        for name in self.formula_symbol_list:
            label = self.FormulaScrollArea.findChild(QLabel, f"{name}label")
            qline = self.FormulaScrollArea.findChild(QLineEdit, f"{name}line")

            _info = self.formula_info[name]
            if type(_info) == list:
                info = _info[0]
                _, unit = self.info[_info[1]]
            else:
                info, unit = self.info[self.formula_info[name]]
            qline.setToolTip(f"{info}, mäts i {unit}")
            label.setToolTip(f"{unit}")

    @staticmethod
    def formula_get_info(text: str, data: dict) -> dict:
        """
        Retrieves info that's correlated with given formula

        :param text: str
            Formula whose information is requested
        :param data: dict
            Dictionary that holds all information
        :return: dict
            Information about formula
        """
        for branch in data:
            for subbranch in data[branch]:
                for formula in data[branch][subbranch]:
                    if formula == text:
                        return data[branch][subbranch][formula]

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
