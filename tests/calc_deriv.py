from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.derivative import DerivativeWorker


class CalcDerivTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_deriv_calc(self):
        self.test_calc_deriv_no_expression()
        self.test_calc_deriv_invalid_expression()
        self.test_calc_deriv_no_variable()
        self.test_calc_deriv_invalid_variable()
        self.test_calc_deriv()
        self.test_calc_deriv_latex()
        self.test_calc_deriv_normal()
        self.test_calc_deriv_order()
        self.test_calc_deriv_point()
        self.test_calc_deriv_var()
        self.test_calc_deriv_unicode()
        self.test_calc_deriv_accuracy()
        self.test_calc_deriv_scientific_notation()

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_no_expression(self):
        command = "calc_deriv"
        params = ["", "x", 1, "", 1, False, False, False, 10]
        solution = {"error": ["Enter an expression"]}
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_invalid_expression(self):
        command = "calc_deriv"
        params = ["(", "x", 1, "", 1, False, False, False, 10]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_no_variable(self):
        command = "calc_deriv"
        params = ["x**x", "", 1, "", 1, False, False, False, 10]
        solution = {"error": ["Enter a variable"]}
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_invalid_variable(self):
        command = "calc_deriv"
        params = ["x**x", "x", 1, "(", 1, False, False, False, 10]
        solution = {"error": ["Failed to parse ("]}
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv(self):
        command = "calc_deriv"
        params = ["x**x", "x", 1, "", 1, False, False, False, 10]
        solution = {
            "deriv": [" x             \nx *(log(x) + 1)", 0],
            "latex": "x^{x} \\left(\\log{\\left(x \\right)} " "+ 1\\right)",
        }
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_latex(self):
        command = "calc_deriv"
        params = ["x**x", "x", 1, "", 2, False, False, False, 10]
        solution = {
            "deriv": ["x^{x} \\left(\\log{\\left(x \\right)} + 1\\right)", 0],
            "latex": "x^{x} \\left(\\log{" "\\left(x \\right)} +" " 1\\right)",
        }
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_normal(self):
        command = "calc_deriv"
        params = ["x**x", "x", 1, "", 3, False, False, False, 10]
        solution = {
            "deriv": ["x**x*(log(x) + 1)", 0],
            "latex": "x^{x} \\left(\\log{\\left(x \\right)} + 1\\right)",
        }
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_order(self):
        command = "calc_deriv"
        params = ["x**x", "x", 4, "", 1, False, False, False, 10]
        solution = {
            "deriv": [
                "   /                              2                           \\\n x |            4   6*(log(x) + 1)    4*(log(x) + 1)   3    2 |\nx *|(log(x) + 1)  + --------------- - -------------- + -- + --|\n   |                       x                 2          2    3|\n   \\                                        x          x    x /",
                0,
            ],
            "latex": "x^{x} \\left(\\left(\\log{\\left(x \\right)} + 1\\right)^{4} + \\frac{6 \\left(\\log{\\left(x \\right)} + 1\\right)^{2}}{x} - \\frac{4 \\left(\\log{\\left(x \\right)} + 1\\right)}{x^{2}} + \\frac{3}{x^{2}} + \\frac{2}{x^{3}}\\right)",
        }
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_point(self):
        command = "calc_deriv"
        params = ["x**x", "x", 1, "pi/E", 1, False, False, False, 10]
        solution = {
            "deriv": [
                "            -1        \n        pi*e          \n/    -1\\              \n\\pi*e  /      *log(pi)",
                "1.353152410",
            ],
            "latex": "\\left(\\frac{\\pi}{e}\\right)^{\\frac{\\pi}{e}} \\log{\\left(\\pi \\right)}",
        }
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_var(self):
        command = "calc_deriv"
        params = ["hi**hi", "hi", 1, "", 1, False, False, False, 10]
        solution = {
            "deriv": ["  hi              \nhi  *(log(hi) + 1)", 0],
            "latex": "hi^{hi} \\left(\\log{\\left(hi \\right)} + 1\\right)",
        }
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_unicode(self):
        command = "calc_deriv"
        params = ["x**x", "x", 1, "", 1, True, False, False, 10]
        solution = {
            "deriv": [" x             \nx ⋅(log(x) + 1)", 0],
            "latex": "x^{x} \\left(\\log{\\left(x \\right)} + 1\\right)",
        }
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_accuracy(self):
        command = "calc_deriv"
        params = ["x**x", "x", 1, "pi/E", 1, False, False, False, 50]
        solution = {
            "deriv": [
                "            -1        \n        pi*e          \n/    -1\\              \n\\pi*e  /      *log(pi)",
                "1.3531524102872950107282503746161198228191041349456",
            ],
            "latex": "\\left(\\frac{\\pi}{e}\\right)^{\\frac{\\pi}{e}} \\log{\\left(\\pi \\right)}",
        }
        return command, params, solution

    @BaseTester.call_worker(DerivativeWorker)
    def test_calc_deriv_scientific_notation(self):
        command = "calc_deriv"
        params = ["x**x", "x", 1, "pi/E", 1, False, False, 20, 10]
        solution = {
            "deriv": [
                "            -1        \n        pi*e          \n/    -1\\              \n\\pi*e  /      *log(pi)",
                "1.3531524102872950107*10**0",
            ],
            "latex": "\\left(\\frac{\\pi}{e}\\right)^{\\frac{\\pi}{e}} \\log{\\left(\\pi \\right)}",
        }
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = CalcDerivTester()
    tester.test_deriv_calc()
    sys.exit(app.exec_())
