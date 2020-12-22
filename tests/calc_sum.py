from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.summation import SummationWorker


class CalcSumTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_sum_calc(self):
        self.test_calc_sum_no_expression()
        self.test_calc_sum_invalid_expression()
        self.test_calc_sum_one_start()
        self.test_calc_sum_invalid_varaible()
        self.test_calc_sum_invalid_start()
        self.test_calc_sum()
        self.test_calc_sum_latex()
        self.test_calc_sum_normal()
        self.test_calc_sum_var()
        self.test_calc_sum_unicode()
        self.test_calc_sum_accuracy()
        self.test_calc_sum_scientific_notation()

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum_no_expression(self):
        command = "calc_sum"
        params = ["", "k", "1", "m", 1, False, False, False, 10]
        solution = {"error": ["Enter an expression"]}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum_invalid_expression(self):
        command = "calc_sum"
        params = ["k**2(", "k", "1", "m", 1, False, False, False, 10]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum_one_start(self):
        command = "calc_sum"
        params = ["k**2", "k", "", "m", 1, False, False, False, 10]
        solution = {"error": ["Enter both start and end"]}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum_invalid_varaible(self):
        command = "calc_sum"
        params = ["k**2", "k(", "1", "m", 1, False, False, False, 10]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum_invalid_start(self):
        command = "calc_sum"
        params = ["k**2", "k", "1", "m(", 1, False, False, False, 10]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum(self):
        command = "calc_sum"
        params = ["k**2", "k", "1", "m", 1, False, False, False, 10]
        solution = {
            "sum": [
                " 3    2    \nm    m    m\n-- + -- + -\n3    2    6",
                "m*(0.3333333333*m**2 + 0.5*m + 0.1666666667)",
            ],
            "latex": "\\frac{m^{3}}{3} + \\frac{m^{2}}{2} + \\frac{m}{6}",
        }
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum_latex(self):
        command = "calc_sum"
        params = ["k**2", "k", "1", "m", 2, False, False, False, 10]
        solution = {
            "sum": [
                "\\frac{m^{3}}{3} + \\frac{m^{2}}{2} + \\frac{m}{6}",
                "m*(0.3333333333*m**2 + 0.5*m + 0.1666666667)",
            ],
            "latex": "\\frac{m^{3}}{3} + \\frac{m^{2}}{2} + \\frac{m}{6}",
        }
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum_normal(self):
        command = "calc_sum"
        params = ["k**2", "k", "1", "m", 3, False, False, False, 10]
        solution = {
            "sum": [
                "m**3/3 + m**2/2 + m/6",
                "m*(0.3333333333*m**2 + 0.5*m + 0.1666666667)",
            ],
            "latex": "\\frac{m^{3}}{3} + \\frac{m^{2}}{2} + \\frac{m}{6}",
        }
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum_var(self):
        command = "calc_sum"
        params = ["hi**2", "hi", "1", "m", 1, False, False, False, 10]
        solution = {
            "sum": [
                " 3    2    \nm    m    m\n-- + -- + -\n3    2    6",
                "m*(0.3333333333*m**2 + 0.5*m + 0.1666666667)",
            ],
            "latex": "\\frac{m^{3}}{3} + \\frac{m^{2}}{2} + \\frac{m}{6}",
        }
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum_unicode(self):
        command = "calc_sum"
        params = ["k**2", "k", "1", "m", 1, True, False, False, 10]
        solution = {
            "sum": [
                " 3    2    \nm    m    m\n── + ── + ─\n3    2    6",
                "m*(0.3333333333*m**2 + 0.5*m + 0.1666666667)",
            ],
            "latex": "\\frac{m^{3}}{3} + \\frac{m^{2}}{2} + \\frac{m}{6}",
        }
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum_accuracy(self):
        command = "calc_sum"
        params = ["2**k/factorial(k)", "k", "pi/2", "oo", 1, False, False, False, 25]
        solution = {
            "sum": [
                " pi           pi                     \n --    /  ___\\                       \n 2     |\\/ 2 |    2           /pi   \\\n2  *pi*|-----|  *e *lowergamma|--, 2|\n       \\  2  /                \\2    /\n-------------------------------------\n                  /    pi\\           \n           2*Gamma|1 + --|           \n                  \\    2 /           ",
                "5.310652941213842681726704",
            ],
            "latex": "\\frac{2^{\\frac{\\pi}{2}} \\pi \\left(\\frac{\\sqrt{2}}{2}\\right)^{\\pi} e^{2} \\gamma\\left(\\frac{\\pi}{2}, 2\\right)}{2 \\Gamma\\left(1 + \\frac{\\pi}{2}\\right)}",
        }
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_calc_sum_scientific_notation(self):
        command = "calc_sum"
        params = ["20**k/factorial(k)", "k", "pi/2", "oo", 1, False, False, 25, 10]
        solution = {
            "sum": [
                "  pi           pi                       \n  --    /  ___\\                         \n  2     |\\/ 5 |    20           /pi    \\\n20  *pi*|-----|  *e  *lowergamma|--, 20|\n        \\  10 /                 \\2     /\n----------------------------------------\n                   /    pi\\             \n            2*Gamma|1 + --|             \n                   \\    2 /             ",
                "4.851651890280590966754774*10**8",
            ],
            "latex": "\\frac{20^{\\frac{\\pi}{2}} \\pi \\left(\\frac{\\sqrt{5}}{10}\\right)^{\\pi} e^{20} \\gamma\\left(\\frac{\\pi}{2}, 20\\right)}{2 \\Gamma\\left(1 + \\frac{\\pi}{2}\\right)}",
        }
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = CalcSumTester()
    tester.test_sum_calc()
    sys.exit(app.exec_())
