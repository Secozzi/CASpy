from PyQt5.QtWidgets import QApplication, QLineEdit
from base_tester import BaseTester


class CalcFormulaTester(BaseTester):
    def __init__(self):
        super().__init__()

        self.formula = ["Ek", "0.5*m*v**2"]

    def test_formula_calc(self):
        self.test_calc_formula_no_selected()
        self.test_calc_formula_invalid_line_entry()
        self.test_calc_formula_no_var()
        self.test_calc_formula_too_many_var()
        self.test_calc_formula()
        self.test_calc_formula_latex()
        self.test_calc_formula_normal()
        self.test_calc_formula_var()
        self.test_calc_formula_unicode()
        self.test_calc_formula_accuracy()
        self.test_calc_formula_scientific_notation()
        self.test_calc_formula_verify_domain()
        self.test_calc_formula_solveset()
        self.test_calc_formula_domain()

    @BaseTester.call_worker
    def test_calc_formula_no_selected(self):
        command = "calc_formula"
        params = [None, self.formula, 2, 'Complexes', 1, False, False, False, 10, False]
        solution = {'error': ['Error: select a formula']}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_invalid_line_entry(self):
        command = "calc_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        value_string = [23, 2, 3]

        params = [[[line_1, "K"], [line_2, "m"], [line_3, "v"]], value_string, 2,
                  'Complexes', 1, False, False, False, 10, False]
        solution = {'error': [f'Error: Unable to get equation from {value_string}']}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_no_var(self):
        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("")
        line_2[0].setText("25")
        line_3[0].setText("")

        command = "calc_formula"
        params = [[line_1, line_2, line_3], self.formula, 2,
                  'Complexes', 1, False, False, False, 10, False]
        solution = {'error': ["Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"]}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_too_many_var(self):
        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("")
        line_2[0].setText("var")
        line_3[0].setText("var")

        command = "calc_formula"
        params = [[line_1, line_2, line_3], self.formula, 2,
                  'Complexes', 1, False, False, False, 10, False]
        solution = {'error': ["Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"]}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula(self):
        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("3")
        line_2[0].setText("")
        line_3[0].setText("5")

        command = "calc_formula"
        params = [[line_1, line_2, line_3], self.formula, 2,
                  'Complexes', 1, False, False, False, 10, False]
        solution = {'eq': ['[6/25]', '0.2400000000'], 'latex': '\\left[ \\frac{6}{25}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_latex(self):
        command = "calc_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("3")
        line_2[0].setText("")
        line_3[0].setText("5")

        params = [[line_1, line_2, line_3], self.formula, 2,
                  'Complexes', 2, False, False, False, 10, True]
        solution = {'eq': ['\\left[ \\frac{6}{25}\\right]', '0.2400000000'], 'latex': '\\left[ \\frac{6}{25}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_normal(self):
        command = "calc_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("3")
        line_2[0].setText("")
        line_3[0].setText("5")

        params = [[line_1, line_2, line_3], self.formula, 2,
                  'Complexes', 3, False, False, False, 10, True]
        solution = {'eq': [['6/25'], '0.2400000000'], 'latex': '\\left[ \\frac{6}{25}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_var(self):
        command = "calc_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("")
        line_2[0].setText("var")
        line_3[0].setText("")

        params = [[line_1, line_2, line_3], self.formula, 2, 'Complexes', 3, False, False, False, 10, True]
        solution = {'eq': [['2*Ek/v**2'], '2.0*Ek/v**2'], 'latex': '\\left[ \\frac{2 Ek}{v^{2}}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_unicode(self):
        command = "calc_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("-5")
        line_2[0].setText("2")
        line_3[0].setText("")

        params = [[line_1, line_2, line_3], self.formula, 2, 'Complexes', 1, True, False, False, 10, True]
        solution = {'eq': ['[-√5⋅ⅈ, √5⋅ⅈ]', ['-2.236067978*I', '2.236067978*I']], 'latex': '\\left[ - \\sqrt{5} i, \\  \\sqrt{5} i\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_accuracy(self):
        command = "calc_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("6")
        line_2[0].setText("")
        line_3[0].setText("7")

        params = [[line_1, line_2, line_3], self.formula, 2, 'Complexes', 1, False, False, False, 25, True]
        solution = {'eq': [' 12 \n[--]\n 49 ', '0.2448979591836734693877551'], 'latex': '\\left[ \\frac{12}{49}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_scientific_notation(self):
        command = "calc_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("6")
        line_2[0].setText("")
        line_3[0].setText("7")

        params = [[line_1, line_2, line_3], self.formula, 2, 'Complexes', 1, False, False, 25, 10, False]
        solution = {'eq': [' 12 \n[--]\n 49 ', '2.448979591836734693877551*10**(-1)'], 'latex': '\\left[ \\frac{12}{49}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_verify_domain(self):
        command = "calc_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("6")
        line_2[0].setText("4")
        line_3[0].setText("")

        params = [[line_1, line_2, line_3], self.formula, 2, 'Interval(-oo, 0)', 1, False, False, 25, 10, True]
        solution = {'eq': ['    ___ \n[-\\/ 3 ]', '-1.732050807568877293527446*10**0'], 'latex': '\\left[ - \\sqrt{3}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_solveset(self):
        command = "calc_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("6")
        line_2[0].setText("4")
        line_3[0].setText("")

        params = [[line_1, line_2, line_3], self.formula, 1, 'Interval(-oo, 0)', 1, False, False, False, 10, True]
        solution = {'eq': ['{-1.73205080756888}', 0], 'latex': '\\left\\{-1.73205080756888\\right\\}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_formula_domain(self):
        command = "calc_formula"

        line_1 = [QLineEdit(self), "Ek"]
        line_2 = [QLineEdit(self), "m"]
        line_3 = [QLineEdit(self), "v"]

        line_1[0].setText("6")
        line_2[0].setText("4")
        line_3[0].setText("")

        params = [[line_1, line_2, line_3], self.formula, 1, 'Integers', 1, False, False, False, 10, False]
        solution = {'eq': ['EmptySet', 0], 'latex': '\\emptyset'}
        return command, params, solution



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = CalcFormulaTester()
    tester.test_formula_calc()
    sys.exit(app.exec_())
