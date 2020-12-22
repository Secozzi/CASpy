from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.integral import IntegralWorker


class PrevIntegTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_integ_prev(self):
        self.test_prev_integ_no_expression()
        self.test_prev_integ_invalid_expression()
        self.test_prev_integ_one_boundary()
        self.test_prev_integ_invalid_varaible()
        self.test_prev_integ()
        self.test_prev_integ_latex()
        self.test_prev_integ_normal()
        self.test_prev_integ_var()
        self.test_prev_integ_unicode()
        self.test_prev_integ_boundary()

    @BaseTester.call_worker(IntegralWorker)
    def test_prev_integ_no_expression(self):
        command = "prev_integ"
        params = ["", "x", "", "", 1, False, False]
        solution = {"error": ["Enter an expression"]}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_prev_integ_invalid_expression(self):
        command = "prev_integ"
        params = ["(", "x", "", "", 1, False, False]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_prev_integ_one_boundary(self):
        command = "prev_integ"
        params = ["x**3", "x", "2", "", 1, False, False]
        solution = {"error": ["Enter both upper and lower bound"]}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_prev_integ_invalid_varaible(self):
        command = "prev_integ"
        params = ["x**3", "(", "", "", 1, False, False]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_prev_integ(self):
        command = "prev_integ"
        params = ["1/(1+x**4)", "x", "", "", 1, False, False]
        solution = {
            "integ": [
                "  /         \n |          \n |   1      \n | ------ dx\n |  4       \n | x  + 1   \n |          \n/           ",
                0,
            ],
            "latex": "\\int \\frac{1}{x^{4} + 1}\\, dx",
        }
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_prev_integ_latex(self):
        command = "prev_integ"
        params = ["1/(1+x**4)", "x", "", "", 2, False, False]
        solution = {
            "integ": ["\\int \\frac{1}{x^{4} + 1}\\, dx", 0],
            "latex": "\\int \\frac{1}{x^{4} + 1}\\, dx",
        }
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_prev_integ_normal(self):
        command = "prev_integ"
        params = ["1/(1+x**4)", "x", "", "", 3, False, False]
        solution = {
            "integ": ["Integral(1/(x**4 + 1), x)", 0],
            "latex": "\\int \\frac{1}{x^{4} + 1}\\, dx",
        }
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_prev_integ_var(self):
        command = "prev_integ"
        params = ["1/(1+hi**4)", "hi", "", "", 1, False, False]
        solution = {
            "integ": [
                "  /             \n |              \n |    1         \n | ------- d(hi)\n |   4          \n | hi  + 1      \n |              \n/               ",
                0,
            ],
            "latex": "\\int \\frac{1}{hi^{4} + 1}\\, dhi",
        }
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_prev_integ_unicode(self):
        command = "prev_integ"
        params = ["1/(1+x**4)", "x", "", "", 1, True, False]
        solution = {
            "integ": [
                "⌠          \n⎮   1      \n⎮ ────── dx\n⎮  4       \n⎮ x  + 1   \n⌡          ",
                0,
            ],
            "latex": "\\int \\frac{1}{x^{4} + 1}\\, dx",
        }
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_prev_integ_boundary(self):
        command = "prev_integ"
        params = ["1/sqrt(1-x**2)", "x", "-1", "1", 1, False, False]
        solution = {
            "integ": [
                "  1               \n  /               \n |                \n |       1        \n |  ----------- dx\n |     ________   \n |    /      2    \n |  \\/  1 - x     \n |                \n/                 \n-1                ",
                0,
            ],
            "latex": "\\int\\limits_{-1}^{1} \\frac{1}{\\sqrt{1 - x^{2}}}\\, dx",
        }
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = PrevIntegTester()
    tester.test_integ_prev()
    sys.exit(app.exec_())
