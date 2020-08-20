from PyQt5.QtWidgets import QApplication
from base_tester import BaseTester


class PrevDerivTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_deriv_prev(self):
        self.test_prev_deriv_no_expression()
        self.test_prev_deriv_invalid_expression()
        self.test_prev_deriv_no_variable()
        self.test_prev_deriv_invalid_variable()
        self.test_prev_deriv()
        self.test_prev_deriv_latex()
        self.test_prev_deriv_normal()
        self.test_prev_deriv_order()
        self.test_prev_deriv_point()
        self.test_prev_deriv_var()
        self.test_prev_deriv_unicode()

    @BaseTester.call_worker
    def test_prev_deriv_no_expression(self):
        command = "prev_deriv"
        params = ['', 'x', 1, '', 1, False, False]
        solution = {'error': ['Enter an expression']}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_deriv_invalid_expression(self):
        command = "prev_deriv"
        params = ['(', 'x', 1, '', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_deriv_no_variable(self):
        command = "prev_deriv"
        params = ['x**x', '', 1, '', 1, False, False]
        solution = {'error': ['Enter a variable']}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_deriv_invalid_variable(self):
        command = "prev_deriv"
        params = ['x**x', '(', 1, '', 1, False, False]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_deriv(self):
        command = "prev_deriv"
        params = ['x**x', 'x', 1, '', 1, False, False]
        solution = {'deriv': ['d / x\\\n--\\x /\ndx    ', 0], 'latex': '\\frac{d}{d x} x^{x}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_deriv_latex(self):
        command = "prev_deriv"
        params = ['x**x', 'x', 1, '', 2, False, False]
        solution = {'deriv': ['\\frac{d}{d x} x^{x}', 0], 'latex': '\\frac{d}{d x} x^{x}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_deriv_normal(self):
        command = "prev_deriv"
        params = ['x**x', 'x', 1, '', 3, False, False]
        solution = {'deriv': ['Derivative(x**x, x)', 0], 'latex': '\\frac{d}{d x} x^{x}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_deriv_order(self):
        command = "prev_deriv"
        params = ['x**x', 'x', 3, '', 1, False, False]
        solution = {'deriv': ['  3    \n d / x\\\n---\\x /\n  3    \ndx     ', 0],
                    'latex': '\\frac{d^{3}}{d x^{3}} x^{x}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_deriv_point(self):
        command = "prev_deriv"
        params = ['x**x', 'x', 1, 'pi', 1, False, False]
        solution = {'deriv': ['At x = pi\nd / x\\\n--\\x /\ndx    ', 0], 'latex': '\\frac{d}{d x} x^{x}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_deriv_var(self):
        command = "prev_deriv"
        params = ['g**g', 'g', 1, '', 1, False, False]
        solution = {'deriv': ['d / g\\\n--\\g /\ndg    ', 0], 'latex': '\\frac{d}{d g} g^{g}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_deriv_unicode(self):
        command = "prev_deriv"
        params = ['x**x', 'x', 1, '', 1, True, False]
        solution = {'deriv': ['d ⎛ x⎞\n──⎝x ⎠\ndx    ', 0], 'latex': '\\frac{d}{d x} x^{x}'}
        return command, params, solution


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    tester = PrevDerivTester()
    tester.test_deriv_prev()
    sys.exit(app.exec_())
