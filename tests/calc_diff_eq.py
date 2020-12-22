from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.equations import EquationsWorker


class CalcDiffEqTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_diff_eq_calc(self):
        self.test_calc_diff_eq_no_expression()
        self.test_calc_diff_eq_invalid_expression()
        self.test_calc_diff_eq_no_function()
        self.test_calc_diff_eq_invalid_function()
        self.test_calc_diff_eq()
        self.test_calc_diff_eq_latex()
        self.test_calc_diff_eq_normal()
        self.test_calc_diff_eq_func()
        self.test_calc_diff_eq_hint()
        self.test_calc_diff_eq_invalid_hint()
        self.test_calc_diff_eq_unicode()
        self.test_calc_diff_eq_accuracy()
        self.test_calc_diff_eq_scientific_notation()

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_no_expression(self):
        command = "calc_diff_eq"
        params = ["", "", "", "f(x)", 1, False, False, False, 10]
        solution = {"error": ["Enter an expression both in left and right side"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_invalid_expression(self):
        command = "calc_diff_eq"
        params = ["sin(x)", "3*f(x", "", "f(x)", 1, False, False, False, 10]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_no_function(self):
        command = "calc_diff_eq"
        params = ["sin(x)", "3*f'(x)", "", "", 1, False, False, False, 10]
        solution = {"error": ["Enter a function"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_invalid_function(self):
        command = "calc_diff_eq"
        params = ["sin(x) = f'(x)", "", "", "f(x", 1, False, False, False, 10]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq(self):
        command = "calc_diff_eq"
        params = ["f''(x)-f'(x)", "2*f(x)", "", "f(x)", 1, False, False, False, 10]
        solution = {
            "eq": [
                "            -x       2*x \n[f(x) = C1*e   + C2*e   ]",
                "           -x       2*x\nf(x) = C1*e   + C2*e   ",
            ],
            "latex": "f{\\left(x \\right)} = C_{1} e^{- x} + C_{2} e^{2 x}",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_latex(self):
        command = "calc_diff_eq"
        params = ["f''(x)-f'(x) = 2*f(x)", "", "", "f(x)", 2, False, False, False, 10]
        solution = {
            "eq": [
                "\\left[ f{\\left(x \\right)} = C_{1} e^{- x} + C_{2} e^{2 x}\\right]",
                "f{\\left(x \\right)} = C_{1} e^{- x} + C_{2} e^{2 x}",
            ],
            "latex": "f{\\left(x \\right)} = C_{1} e^{- x} + C_{2} e^{2 x}",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_normal(self):
        command = "calc_diff_eq"
        params = ["f''(x)-f'(x) = 2*f(x)", "", "", "f(x)", 3, False, False, False, 10]
        solution = {
            "eq": [
                "[Eq(f(x), C1*exp(-x) + C2*exp(2*x))]",
                "Eq(f(x), C1*exp(-x) + C2*exp(2*x))",
            ],
            "latex": "f{\\left(x \\right)} = C_{1} e^{- x} + C_{2} e^{2 x}",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_func(self):
        command = "calc_diff_eq"
        params = ["u''(x)-u'(x) = 2*u(x)", "", "", "u(x)", 1, False, False, False, 10]
        solution = {
            "eq": [
                "            -x       2*x \n[u(x) = C1*e   + C2*e   ]",
                "           -x       2*x\nu(x) = C1*e   + C2*e   ",
            ],
            "latex": "u{\\left(x \\right)} = C_{1} e^{- x} + C_{2} e^{2 x}",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_hint(self):
        command = "calc_diff_eq"
        params = [
            "3*f'''(x) + 5*f''(x) + f'(x) - f(x) - x",
            "exp(-x)",
            "nth_linear_constant_coeff_undetermined_coefficients",
            "f(x)",
            1,
            False,
            False,
            False,
            10,
        ]
        solution = {
            "eq": [
                "            x                                 \n            -                                 \n            3       /       /     x\\\\  -x     \n[f(x) = C3*e  - x + |C1 + x*|C2 - -||*e   - 1]\n                    \\       \\     8//         ",
                "           x                                        \n           -                                        \n           3                                -x      \nf(x) = C3*e  - x + (C1 + x*(C2 - 0.125*x))*e   - 1.0",
            ],
            "latex": "f{\\left(x \\right)} = C_{3} e^{\\frac{x}{3}} - x + \\left(C_{1} + x \\left(C_{2} - \\frac{x}{8}\\right)\\right) e^{- x} - 1",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_invalid_hint(self):
        command = "calc_diff_eq"
        params = ["f'(x)", "exp(-x)", "(", "f(x)", 1, False, False, False, 10]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_unicode(self):
        command = "calc_diff_eq"
        params = ["f''(x)-f'(x) = 2*f(x)", "", "", "f(x)", 1, True, False, False, 10]
        solution = {
            "eq": [
                "⎡           -x       2⋅x⎤\n⎣f(x) = C₁⋅ℯ   + C₂⋅ℯ   ⎦",
                "           -x       2⋅x\nf(x) = C₁⋅ℯ   + C₂⋅ℯ   ",
            ],
            "latex": "f{\\left(x \\right)} = C_{1} e^{- x} + C_{2} e^{2 x}",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_accuracy(self):
        command = "calc_diff_eq"
        params = ["1/f(x)", "f'(x)", "", "f(x)", 1, False, False, False, 25]
        solution = {
            "eq": [
                "           __________           __________ \n[f(x) = -\\/ C1 + 2*x , f(x) = \\/ C1 + 2*x ]",
                "                                                0.5                                                0.5 \n[f(x) = -1.414213562373095048801689*(0.5*C1 + x)   , f(x) = 1.414213562373095048801689*(0.5*C1 + x)   ]",
            ],
            "latex": "\\left[ f{\\left(x \\right)} = - \\sqrt{C_{1} + 2 x}, \\  f{\\left(x \\right)} = \\sqrt{C_{1} + 2 x}\\right]",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_calc_diff_eq_scientific_notation(self):
        command = "calc_diff_eq"
        params = ["1/f(x) = f'(x)", "", "", "f(x)", 1, False, False, 25, 10]
        solution = {
            "error": ["Scientific notation not supported for differential equations"]
        }
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = CalcDiffEqTester()
    tester.test_diff_eq_calc()
    sys.exit(app.exec_())
