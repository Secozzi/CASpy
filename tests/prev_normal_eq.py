from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.equations import EquationsWorker


class PrevNormalEqTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_normal_eq_prev(self):
        self.test_prev_normal_eq_no_expression()
        self.test_prev_normal_eq_one_expression()
        self.test_prev_normal_eq_invalid_expression()
        self.test_prev_normal_eq_no_variable()
        self.test_prev_normal_eq_invalid_varaible()
        self.test_prev_normal_eq()
        self.test_prev_normal_eq_equal_sign()
        self.test_prev_normal_eq_latex()
        self.test_prev_normal_eq_normal()
        self.test_prev_normal_eq_var()
        self.test_prev_normal_eq_unicode()

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_normal_eq_no_expression(self):
        command = "prev_normal_eq"
        params = ["", "", "x", "Complexes", 1, False, False]
        solution = {"error": ["Enter an expression both in left and right side"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_normal_eq_one_expression(self):
        command = "prev_normal_eq"
        params = ["x**x", "", "x", "Complexes", 1, False, False]
        solution = {"error": ["Enter an expression both in left and right side"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_normal_eq_invalid_expression(self):
        command = "prev_normal_eq"
        params = ["x**x(", "2", "x", "Complexes", 1, False, False]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_normal_eq_no_variable(self):
        command = "prev_normal_eq"
        params = ["x**x", "2", "", "Complexes", 1, False, False]
        solution = {"error": ["Enter a variable"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_normal_eq_invalid_varaible(self):
        command = "prev_normal_eq"
        params = ["x**x", "2", "x(", "Complexes", 1, False, False]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_normal_eq(self):
        command = "prev_normal_eq"
        params = ["x**x", "2", "x", "Complexes", 1, False, False]
        solution = {
            "eq": [" x    \nx  = 2\nDomain: Complexes", 0],
            "latex": "x^{x} = 2",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_normal_eq_equal_sign(self):
        command = "prev_normal_eq"
        params = ["x**x = 2", "", "x", "Complexes", 1, False, False]
        solution = {
            "eq": [" x    \nx  = 2\nDomain: Complexes", 0],
            "latex": "x^{x} = 2",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_normal_eq_latex(self):
        command = "prev_normal_eq"
        params = ["x**x", "2", "x", "Complexes", 2, False, False]
        solution = {"eq": ["x^{x} = 2\nDomain: Complexes", 0], "latex": "x^{x} = 2"}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_normal_eq_normal(self):
        command = "prev_normal_eq"
        params = ["x**x", "2", "x", "Complexes", 3, False, False]
        solution = {"eq": ["x**x = 2\nDomain: Complexes", 0], "latex": "x^{x} = 2"}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_normal_eq_var(self):
        command = "prev_normal_eq"
        params = ["hi**hi", "2", "hi", "Complexes", 1, False, False]
        solution = {
            "eq": ["  hi    \nhi   = 2\nDomain: Complexes", 0],
            "latex": "hi^{hi} = 2",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_normal_eq_unicode(self):
        command = "prev_normal_eq"
        params = ["x**pi", "2", "x", "Complexes", 1, True, False]
        solution = {
            "eq": [" π    \nx  = 2\nDomain: Complexes", 0],
            "latex": "x^{\\pi} = 2",
        }
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = PrevNormalEqTester()
    tester.test_normal_eq_prev()
    sys.exit(app.exec_())
