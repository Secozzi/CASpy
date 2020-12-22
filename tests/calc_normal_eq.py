from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.equations import EquationsWorker


class CalcNormalEqTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_normal_eq_calc(self):
        self.test_calc_normal_eq_no_expression()
        self.test_calc_normal_eq_one_expression()
        self.test_calc_normal_eq_invalid_expression()
        self.test_calc_normal_eq_no_variable()
        self.test_calc_normal_eq_invalid_varaible()
        self.test_calc_normal_eq()
        self.test_calc_normal_eq_equal_sign()
        self.test_calc_normal_eq_latex()
        self.test_calc_normal_eq_normal()
        self.test_calc_normal_eq_var()
        self.test_calc_normal_eq_unicode()
        self.test_calc_normal_eq_accuracy()
        self.test_calc_normal_eq_approximate()
        self.test_calc_normal_eq_scientific_notation()
        self.test_calc_normal_eq_verify_domain()
        self.test_calc_normal_eq_verify_domain_2()
        self.test_calc_normal_eq_domain()
        self.test_calc_normal_eq_solveset()

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_no_expression(self):
        command = "calc_normal_eq"
        params = ["", "", "x", 2, "Complexes", 1, False, False, False, 10, False]
        solution = {"error": ["Enter an expression both in left and right side"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_one_expression(self):
        command = "calc_normal_eq"
        params = ["x**x", "", "x", 2, "Complexes", 1, False, False, False, 10, False]
        solution = {"error": ["Enter an expression both in left and right side"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_invalid_expression(self):
        command = "calc_normal_eq"
        params = ["x**x(", "2", "x", 2, "Complexes", 1, False, False, False, 10, False]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_no_variable(self):
        command = "calc_normal_eq"
        params = ["x**x", "2", "", 2, "Complexes", 1, False, False, False, 10, False]
        solution = {"error": ["Enter a variable"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_invalid_varaible(self):
        command = "calc_normal_eq"
        params = ["x**x", "2", "x(", 2, "Complexes", 1, False, False, False, 10, False]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq(self):
        command = "calc_normal_eq"
        params = ["x**x", "2", "x", 2, "Complexes", 1, False, False, False, 10, False]
        solution = {
            "eq": ["  W(log(2)) \n[e         ]", "1.559610469"],
            "latex": "\\left[ e^{W\\left(\\log{\\left(2 \\right)}\\right)}\\right]",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_equal_sign(self):
        command = "calc_normal_eq"
        params = [
            "x**x = 2",
            "",
            "x",
            2,
            "Complexes",
            1,
            False,
            False,
            False,
            10,
            False,
        ]
        solution = {
            "eq": ["  W(log(2)) \n[e         ]", "1.559610469"],
            "latex": "\\left[ e^{W\\left(\\log{\\left(2 \\right)}\\right)}\\right]",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_latex(self):
        command = "calc_normal_eq"
        params = ["x**x", "2", "x", 2, "Complexes", 2, False, False, False, 10, False]
        solution = {
            "eq": [
                "\\left[ e^{W\\left(\\log{\\left(2 \\right)}\\right)}\\right]",
                "1.559610469",
            ],
            "latex": "\\left[ e^{W\\left(\\log{\\left(2 \\right)}\\right)}\\right]",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_normal(self):
        command = "calc_normal_eq"
        params = ["x**x", "2", "x", 2, "Complexes", 3, False, False, False, 10, False]
        solution = {
            "eq": [["exp(LambertW(log(2)))"], "1.559610469"],
            "latex": "\\left[ e^{W\\left(\\log{\\left(2 \\right)}\\right)}\\right]",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_var(self):
        command = "calc_normal_eq"
        params = [
            "hi**hi",
            "2",
            "hi",
            2,
            "Complexes",
            1,
            False,
            False,
            False,
            10,
            False,
        ]
        solution = {
            "eq": ["  W(log(2)) \n[e         ]", "1.559610469"],
            "latex": "\\left[ e^{W\\left(\\log{\\left(2 \\right)}\\right)}\\right]",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_unicode(self):
        command = "calc_normal_eq"
        params = ["x**x", "2", "x", 2, "Complexes", 1, True, False, False, 10, False]
        solution = {
            "eq": ["⎡ W(log(2))⎤\n⎣ℯ         ⎦", "1.559610469"],
            "latex": "\\left[ e^{W\\left(\\log{\\left(2 \\right)}\\right)}\\right]",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_accuracy(self):
        command = "calc_normal_eq"
        params = ["x**x", "2", "x", 2, "Complexes", 1, False, False, False, 25, False]
        solution = {
            "eq": ["  W(log(2)) \n[e         ]", "1.559610469462369349970389"],
            "latex": "\\left[ e^{W\\left(\\log{\\left(2 \\right)}\\right)}\\right]",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_approximate(self):
        command = "calc_normal_eq"
        params = ["4**x-3**x-2**x", "4", "x", 2, "Complexes", 1, False, False, False, 25, False, "2"]
        solution = {
            'eq': ['2.095889929671676257021721', '2.095889929671676257021721'],
            'latex': '\\mathtt{\\text{2.095889929671676257021721}}'
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_scientific_notation(self):
        command = "calc_normal_eq"
        params = ["x**x", "2", "x", 2, "Complexes", 1, False, False, 25, 10, False]
        solution = {
            "eq": ["  W(log(2)) \n[e         ]", "1.559610469462369349970389*10**0"],
            "latex": "\\left[ e^{W\\left(\\log{\\left(2 \\right)}\\right)}\\right]",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_verify_domain(self):
        command = "calc_normal_eq"
        params = [
            "x**2",
            "3",
            "x",
            2,
            "Interval(-oo, 0)",
            1,
            False,
            False,
            25,
            10,
            True,
        ]
        solution = {
            "eq": ["    ___ \n[-\\/ 3 ]", "-1.732050807568877293527446*10**0"],
            "latex": "\\left[ - \\sqrt{3}\\right]",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_verify_domain_2(self):
        command = "calc_normal_eq"
        params = ["x**x", "2", "x", 2, "Integers", 1, False, False, False, 10, True]
        solution = {"eq": ["[]", []], "latex": "\\left[ \\right]"}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_domain(self):
        command = "calc_normal_eq"
        params = [
            "x**2",
            "3",
            "x",
            1,
            "Interval(-oo, 0)",
            1,
            False,
            False,
            25,
            10,
            True,
        ]
        solution = {
            "eq": ["    ___ \n{-\\/ 3 }", 0],
            "latex": "\\left\\{- \\sqrt{3}\\right\\}",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_normal_eq_solveset(self):
        command = "calc_normal_eq"
        params = ["sin(x)", "1", "x", 1, "Complexes", 1, True, False, False, 10, True]
        solution = {
            "eq": ["⎧        π        ⎫\n⎨2⋅n⋅π + ─ | n ∊ ℤ⎬\n⎩        2        ⎭", 0],
            "latex": "\\left\\{2 n \\pi + \\frac{\\pi}{2}\\; |\\; n \\in \\mathbb{Z}\\right\\}",
        }
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = CalcNormalEqTester()
    tester.test_normal_eq_calc()
    sys.exit(app.exec_())
