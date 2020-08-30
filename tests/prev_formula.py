from PyQt5.QtWidgets import QApplication, QLineEdit

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.formulas import FormulaWorker


class PrevFormulaTester(BaseTester):
    def __init__(self):
        super().__init__()

        self.formula = ["Ek", "0.5*m*v**2"]

    def test_formula_prev(self):
        self.test_prev_formula_no_selected()
        self.test_prev_formula_invalid_line_entry()
        self.test_prev_formula_no_var()
        self.test_prev_formula_too_many_var()
        self.test_prev_formula()
        self.test_prev_formula_latex()
        self.test_prev_formula_normal()
        self.test_prev_formula_var()
        self.test_prev_formula_unicode()

    @BaseTester.call_worker(FormulaWorker)
    def test_prev_formula_no_selected(self):
        command = "prev_formula"
        params = [None, self.formula, 'Complexes', 1, False, False]
        solution = {'error': ['Error: select a formula']}
        return command, params, solution

    @BaseTester.call_worker(FormulaWorker)
    def test_prev_formula_invalid_line_entry(self):
        command = "prev_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        value_string = [23, 2, 3]

        params = [[[line_1, "K"], [line_2, "m"], [line_3, "v"]], value_string,
                  'Complexes', 1, False, False]
        solution = {'error': [f'Error: Unable to get equation from {value_string}']}
        return command, params, solution

    @BaseTester.call_worker(FormulaWorker)
    def test_prev_formula_no_var(self):
        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("")
        line_2[0].setText("25")
        line_3[0].setText("")

        command = "prev_formula"
        params = [[line_1, line_2, line_3], self.formula,
                  'Complexes', 1, False, False]
        solution = {'error': ["Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"]}
        return command, params, solution

    @BaseTester.call_worker(FormulaWorker)
    def test_prev_formula_too_many_var(self):
        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("")
        line_2[0].setText("var")
        line_3[0].setText("var")

        command = "prev_formula"
        params = [[line_1, line_2, line_3], self.formula,
                  'Complexes', 1, False, False]
        solution = {'error': ["Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"]}
        return command, params, solution

    @BaseTester.call_worker(FormulaWorker)
    def test_prev_formula(self):
        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("3")
        line_2[0].setText("")
        line_3[0].setText("5")

        command = "prev_formula"
        params = [[line_1, line_2, line_3], self.formula,
                  'Complexes', 1, False, False]
        solution = {'eq': ['            2\nEk = 0.5*m*v \nDomain: Complexes', 0], 'latex': 'Ek = 0.5 m v^{2}'}
        return command, params, solution

    @BaseTester.call_worker(FormulaWorker)
    def test_prev_formula_latex(self):
        command = "prev_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("3")
        line_2[0].setText("")
        line_3[0].setText("5")

        params = [[line_1, line_2, line_3], self.formula,
                  'Complexes', 2, False, False]
        solution = {'eq': ['Ek = 0.5 m v^{2}\nDomain: Complexes', 0], 'latex': 'Ek = 0.5 m v^{2}'}
        return command, params, solution

    @BaseTester.call_worker(FormulaWorker)
    def test_prev_formula_normal(self):
        command = "prev_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("3")
        line_2[0].setText("")
        line_3[0].setText("5")

        params = [[line_1, line_2, line_3], self.formula,
                  'Complexes', 3, False, False]
        solution = {'eq': ['Ek = 0.5*m*v**2\nDomain: Complexes', 0], 'latex': 'Ek = 0.5 m v^{2}'}
        return command, params, solution

    @BaseTester.call_worker(FormulaWorker)
    def test_prev_formula_var(self):
        command = "prev_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("")
        line_2[0].setText("var")
        line_3[0].setText("")

        params = [[line_1, line_2, line_3], self.formula, 'Complexes', 1, False, False]
        solution = {'eq': ['            2\nEk = 0.5*m*v \nDomain: Complexes', 0], 'latex': 'Ek = 0.5 m v^{2}'}
        return command, params, solution

    @BaseTester.call_worker(FormulaWorker)
    def test_prev_formula_unicode(self):
        command = "prev_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("-5")
        line_2[0].setText("2")
        line_3[0].setText("")

        params = [[line_1, line_2, line_3], self.formula, 'Complexes', 1, True, False]
        solution = {'eq': ['            2\nEk = 0.5⋅m⋅v \nDomain: Complexes', 0], 'latex': 'Ek = 0.5 m v^{2}'}
        return command, params, solution

    @BaseTester.call_worker(FormulaWorker)
    def test_prev_formula_domain(self):
        command = "prev_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("6")
        line_2[0].setText("4")
        line_3[0].setText("")

        params = [[line_1, line_2, line_3], self.formula, 'Integers', 1, False, False]
        solution = {'eq': ['EmptySet', 0], 'latex': '\\emptyset'}
        return command, params, solution



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = PrevFormulaTester()
    tester.test_formula_prev()
    sys.exit(app.exec_())
