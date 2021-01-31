#
#    CASPy - A program that provides both a GUI and a CLI to SymPy.
#    Copyright (C) 2021 Folke Ishii
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

# Standard library
import typing as ty
import traceback
import json

# Third party
import sympy as sy

# PyQt5
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QSplitter,
    QWidget,
)
from PyQt5.uic import loadUi

# Relative
from caspy3.qt_assets.widgets.tab import CaspyTab
from caspy3.qt_assets.widgets.worker import BaseWorker
from caspy3.qt_assets.widgets.searchable_combo import SearchableComboBox
from caspy3.qt_assets.widgets.fields_scroll import FieldsScrollArea

if ty.TYPE_CHECKING:
    from caspy3.qt_assets.app.mainwindow import MainWindow
    from caspy3.qt_assets.widgets.input import TextEdit
    from caspy3.qt_assets.widgets.output import OutputWidget


class IntegralWorker(BaseWorker):
    def __init__(
        self, command: str, params: list, copy: ty.Union[int, None] = None
    ) -> None:
        super().__init__(command, params, copy)

    @pyqtSlot()
    def prev_integral(
        self,
        input_expression: str,
        input_variable: str,
        input_order: int,
        input_point: str,
        output_type: int,
        use_unicode: bool,
        line_wrap: bool,
        clashes: ty.Dict[str, sy.Symbol],
    ) -> ty.Dict[str, ty.List[str]]:
        sy.init_printing(use_unicode=use_unicode, wrap_line=line_wrap)

        approx_ans = 0
        exact_ans = ""
        latex_ans = ""

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}

        try:
            expr = sy.parse_expr(input_expression, local_dict=clashes)
            var = sy.parse_expr(input_variable, local_dict=clashes)

            return {"deriv": [exact_ans, approx_ans], "latex": latex_ans}
        except:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

    @pyqtSlot()
    def calc_function_name(
        self,
        input_expression: str,
        input_variable: str,
        input_order: int,
        input_point: str,
        output_type: int,
        use_unicode: bool,
        line_wrap: bool,
        clashes: dict,
        use_scientific: int,
        accuracy: int,
    ) -> ty.Dict[str, ty.List[str]]:
        sy.init_printing(use_unicode=use_unicode, wrap_line=line_wrap)

        approx_ans = "..."
        exact_ans = ""
        latex_ans = ""

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}

        try:
            expr = sy.parse_expr(input_expression, local_dict=clashes)
            var = sy.parse_expr(input_variable, local_dict=clashes)

            return {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

        except:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}


class IntegralTab(CaspyTab):

    display_name = "Integrals"
    name = "integral"

    def __stubs(self) -> None:
        """Stubs for auto-completion"""
        self.integ_approx = OutputWidget(self)
        self.integ_calc = QPushButton()
        self.integ_exact = OutputWidget(self)
        self.integ_input = TextEdit(self)
        self.integ_methods_combo = SearchableComboBox(self)
        self.integ_methods_label = QLabel()
        self.integ_prev = QPushButton()
        self.integ_main_splitter = QSplitter()
        self.integ_input_splitter = QSplitter()
        self.integ_output_splitter = QSplitter()
        self.integral_tab = QWidget()
        self.methods_scroll_area = FieldsScrollArea()
        self.methods_scroll_area_contents = QWidget()
        self.verticalLayoutWidget = QWidget()

        raise AssertionError("This should never be called")

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window, self.name)
        loadUi(self.main_window.get_resource("qt_assets/tabs/integral.ui"), self)
        self.setStyleSheet(f"font-size: {self.main_window.tabs_font.pointSize()}pt; font-family: {self.main_window.tabs_font.family()};")

        self.eout = self.integ_exact
        self.aout = self.integ_approx
        self.out_splitter = self.integ_output_splitter

        self.splitters: ty.List[QSplitter] = [
            self.integ_main_splitter,
            self.integ_input_splitter,
            self.integ_output_splitter,
        ]

        self.read_data()

        self.init_bindings()
        self.init_methods()
        self.set_splitters(self.splitters)

    def read_data(self) -> None:
        with open(self.main_window.get_resource("data/integ_methods.json"), "r") as f:
            self.integ_methods = json.loads(f.read())

    def init_methods(self) -> None:
        for item in self.integ_methods:
            self.integ_methods_combo.addItem(item["name"])

    def init_bindings(self) -> None:
        self.integ_methods_combo.currentIndexChanged.connect(
            lambda i: self.methods_scroll_area.updateFields(self.integ_methods[i])
        )
        self.integ_prev.clicked.connect(self.preview)
        self.integ_calc.clicked.connect(self.calculate)

    def calculate(self) -> None:
        """Calculate from input, gets called on Ctrl+Return"""
        self.eout.set_cursor(Qt.WaitCursor)
        self.aout.set_cursor(Qt.WaitCursor)

        print(self.methods_scroll_area.get_data())

        # input_expression: str,
        # input_variable: str,
        # input_order: int,
        # input_point: str,
        # output_type: int,
        # use_unicode: bool,
        # line_wrap: bool,
        # clashes: dict,
        # use_scientific: int,
        # accuracy: int,

    def preview(self) -> None:
        """Preview from input, get called on Ctrl+Shift+Return"""
        self.eout.set_cursor(Qt.WaitCursor)
        self.aout.set_cursor(Qt.WaitCursor)

        # input_expression: str,
        # input_variable: str,
        # input_order: int,
        # input_point: str,
        # output_type: int,
        # use_unicode: bool,
        # line_wrap: bool,
        # clashes: ty.Dict[str, sy.Symbol],

    def close_event(self) -> None:
        self.write_splitters(self.splitters)
