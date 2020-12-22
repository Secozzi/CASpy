from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.limit import LimitWorker


class CalcLimitTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_limit_calc(self):
        self.test_calc_limit_no_expression()
        self.test_calc_limit_invalid_expression()
        self.test_calc_limit_no_variable()
        self.test_calc_limit_invalid_varaible()
        self.test_calc_limit_no_approach()
        self.test_calc_limit_invalid_approach()
        self.test_calc_limit()
        self.test_calc_limit_latex()
        self.test_calc_limit_normal()
        self.test_calc_limit_var()
        self.test_calc_limit_unicode()
        self.test_calc_limit_accuracy()
        self.test_calc_limit_scientific_notation()
        self.test_calc_limit_invalid_limit()
        self.test_calc_limit_side_specific()

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_no_expression(self):
        command = "calc_limit"
        params = ["", "x", "0", "+-", 1, False, False, False, 10]
        solution = {"error": ["Enter an expression"]}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_invalid_expression(self):
        command = "calc_limit"
        params = ["x(", "x", "0", "+-", 1, False, False, False, 10]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_no_variable(self):
        command = "calc_limit"
        params = ["x!**(1/x)", "", "0", "+-", 1, False, False, False, 10]
        solution = {"error": ["Enter a variable"]}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_invalid_varaible(self):
        command = "calc_limit"
        params = ["x!**(1/x)", "(", "0", "+-", 1, False, False, False, 10]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_no_approach(self):
        command = "calc_limit"
        params = ["x!**(1/x)", "x", "", "+-", 1, False, False, False, 10]
        solution = {"error": ["Enter value that the variable approaches"]}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_invalid_approach(self):
        command = "calc_limit"
        params = ["x!**(1/x)", "x", "(", "+-", 1, False, False, False, 10]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit(self):
        command = "calc_limit"
        params = ["x!**(1/x)", "x", "0", "+-", 1, False, False, False, 10]
        solution = {
            "limit": [" -EulerGamma\ne           ", "0.5614594836"],
            "latex": "e^{- \\gamma}",
        }
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_latex(self):
        command = "calc_limit"
        params = ["x!**(1/x)", "x", "0", "+-", 2, False, False, False, 10]
        solution = {
            "limit": ["e^{- \\gamma}", "0.5614594836"],
            "latex": "e^{- \\gamma}",
        }
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_normal(self):
        command = "calc_limit"
        params = ["x!**(1/x)", "x", "0", "+-", 3, False, False, False, 10]
        solution = {
            "limit": ["exp(-EulerGamma)", "0.5614594836"],
            "latex": "e^{- \\gamma}",
        }
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_var(self):
        command = "calc_limit"
        params = ["hi!**(1/hi)", "hi", "0", "+-", 1, False, False, False, 10]
        solution = {
            "limit": [" -EulerGamma\ne           ", "0.5614594836"],
            "latex": "e^{- \\gamma}",
        }
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_unicode(self):
        command = "calc_limit"
        params = ["x!**(1/x)", "x", "0", "+-", 1, True, False, False, 10]
        solution = {"limit": [" -γ\nℯ  ", "0.5614594836"], "latex": "e^{- \\gamma}"}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_accuracy(self):
        command = "calc_limit"
        params = ["x!**(1/x)", "x", "0", "+-", 1, False, False, False, 25]
        solution = {
            "limit": [" -EulerGamma\ne           ", "0.5614594835668851698241432"],
            "latex": "e^{- \\gamma}",
        }
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_scientific_notation(self):
        command = "calc_limit"
        params = ["x!**(1/x)", "x", "0", "+-", 1, False, False, 25, 10]
        solution = {
            "limit": [
                " -EulerGamma\ne           ",
                "5.614594835668851698241432*10**(-1)",
            ],
            "latex": "e^{- \\gamma}",
        }
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_invalid_limit(self):
        command = "calc_limit"
        params = ["1/x", "x", "0", "+-", 1, False, False, False, 10]

        from sympy import __version__

        if __version__.split(".")[1] == "7":
            solution = {'limit': ['zoo', 'zoo'], 'latex': '\\tilde{\\infty}'}
        else:
            solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_calc_limit_side_specific(self):
        command = "calc_limit"
        params = ["1/x", "x", "0", "-", 1, False, False, False, 10]
        solution = {"limit": ["-oo", "-oo"], "latex": "-\\infty"}
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = CalcLimitTester()
    tester.test_limit_calc()
    sys.exit(app.exec_())
