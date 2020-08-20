from PyQt5.QtWidgets import QApplication
from base_tester import BaseTester


class PrevDiffEqTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_diff_eq_prev(self):
        self.test_prev_diff_eq_no_expression()
        self.test_prev_diff_eq_invalid_expression()
        self.test_prev_diff_eq_no_function()
        self.test_prev_diff_eq_invalid_function()
        self.test_prev_diff_eq()
        self.test_prev_diff_eq_latex()
        self.test_prev_diff_eq_normal()
        self.test_prev_diff_eq_func()
        self.test_prev_diff_eq_hint()
        self.test_prev_diff_eq_unicode()

    @BaseTester.call_worker
    def test_prev_diff_eq_no_expression(self):
        command = "prev_diff_eq"
        params = ['', '', 'f(x)', 1, True, False]
        solution = {'error': ['Enter an expression both in left and right side']}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_diff_eq_invalid_expression(self):
        command = "prev_diff_eq"
        params = ['(', 'f(x)', 'f(x)', 1, True, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_diff_eq_no_function(self):
        command = "prev_diff_eq"
        params = ["f'(x)", '1/f(x)', '', 1, False, False]
        solution = {'error': ['Enter a function to solve for']}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_diff_eq_invalid_function(self):
        command = "prev_diff_eq"
        params = ["f'(x)", '1/f(x)', 'f(x', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_diff_eq(self):
        command = "prev_diff_eq"
        params = ["f'(x)", '1/f(x)', 'f(x)', 1, False, False]
        solution = {'eq': ["d           1  \n--(f(x)) = ----\ndx         f(x)\nClassification: ('separable', '1st_exact', 'Bernoulli', '1st_power_series', 'lie_group', 'separable_Integral', '1st_exact_Integral', 'Bernoulli_Integral')", 0], 'latex': '\\frac{d}{d x} f{\\left(x \\right)} = \\frac{1}{f{\\left(x \\right)}}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_diff_eq_latex(self):
        command = "prev_diff_eq"
        params = ["f'(x)", '1/f(x)', 'f(x)', 2, False, False]
        solution = {'eq': ["\\frac{d}{d x} f{\\left(x \\right)} = \\frac{1}{f{\\left(x \\right)}}\nClassification: ('separable', '1st_exact', 'Bernoulli', '1st_power_series', 'lie_group', 'separable_Integral', '1st_exact_Integral', 'Bernoulli_Integral')", 0], 'latex': '\\frac{d}{d x} f{\\left(x \\right)} = \\frac{1}{f{\\left(x \\right)}}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_diff_eq_normal(self):
        command = "prev_diff_eq"
        params = ["f'(x)", '1/f(x)', 'f(x)', 3, False, False]
        solution = {'eq': ["Derivative(f(x), x) = 1/f(x)\nClassification: ('separable', '1st_exact', 'Bernoulli', '1st_power_series', 'lie_group', 'separable_Integral', '1st_exact_Integral', 'Bernoulli_Integral')", 0], 'latex': '\\frac{d}{d x} f{\\left(x \\right)} = \\frac{1}{f{\\left(x \\right)}}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_diff_eq_func(self):
        command = "prev_diff_eq"
        params = ["ok'(x)", '1/ok(x)', 'ok(x)', 1, False, False]
        solution = {'eq': ["d             1  \n--(ok(x)) = -----\ndx          ok(x)\nClassification: ('separable', '1st_exact', 'Bernoulli', '1st_power_series', 'lie_group', 'separable_Integral', '1st_exact_Integral', 'Bernoulli_Integral')", 0], 'latex': '\\frac{d}{d x} \\operatorname{ok}{\\left(x \\right)} = \\frac{1}{\\operatorname{ok}{\\left(x \\right)}}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_diff_eq_hint(self):
        command = "prev_diff_eq"
        params = ["3*f'''(x) + 5*f''(x) +f'(x) - f(x) - x", 'exp(-x)', 'f(x)', 1, False, False]
        solution = {'eq': ["                           2             3            \n            d             d             d           -x\n-x - f(x) + --(f(x)) + 5*---(f(x)) + 3*---(f(x)) = e  \n            dx             2             3            \n                         dx            dx             \nClassification: ('nth_linear_constant_coeff_undetermined_coefficients', 'nth_linear_constant_coeff_variation_of_parameters', 'nth_linear_constant_coeff_variation_of_parameters_Integral')", 0], 'latex': '- x - f{\\left(x \\right)} + \\frac{d}{d x} f{\\left(x \\right)} + 5 \\frac{d^{2}}{d x^{2}} f{\\left(x \\right)} + 3 \\frac{d^{3}}{d x^{3}} f{\\left(x \\right)} = e^{- x}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_diff_eq_unicode(self):
        command = "prev_diff_eq"
        params = ["3*f'''(x) + 5*f''(x) +f'(x) - f(x) - x", 'exp(-x)', 'f(x)', 1, True, False]
        solution = {'eq': ["                           2             3            \n            d             d             d           -x\n-x - f(x) + ──(f(x)) + 5⋅───(f(x)) + 3⋅───(f(x)) = ℯ  \n            dx             2             3            \n                         dx            dx             \nClassification: ('nth_linear_constant_coeff_undetermined_coefficients', 'nth_linear_constant_coeff_variation_of_parameters', 'nth_linear_constant_coeff_variation_of_parameters_Integral')", 0], 'latex': '- x - f{\\left(x \\right)} + \\frac{d}{d x} f{\\left(x \\right)} + 5 \\frac{d^{2}}{d x^{2}} f{\\left(x \\right)} + 3 \\frac{d^{3}}{d x^{3}} f{\\left(x \\right)} = e^{- x}'}
        return command, params, solution


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    tester = PrevDiffEqTester()
    tester.test_diff_eq_prev()
    sys.exit(app.exec_())
