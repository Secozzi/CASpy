from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.limit import LimitWorker


class PrevLimitTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_limit_prev(self):
        self.test_prev_limit_no_expression()
        self.test_prev_limit_invalid_expression()
        self.test_prev_limit_no_variable()
        self.test_prev_limit_invalid_varaible()
        self.test_prev_limit_no_approach()
        self.test_prev_limit_invalid_approach()
        self.test_prev_limit()
        self.test_prev_limit_latex()
        self.test_prev_limit_normal()
        self.test_prev_limit_var()
        self.test_prev_limit_unicode()
        self.test_prev_limit_side_specific()

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit_no_expression(self):
        command = "prev_limit"
        params = ['', 'x', '0', '+-', 1, False, False]
        solution = {'error': ['Enter an expression']}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit_invalid_expression(self):
        command = "prev_limit"
        params = ['x(', 'x', '0', '+-', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit_no_variable(self):
        command = "prev_limit"
        params = ['x!**(1/x)', '', '0', '+-', 1, False, False]
        solution = {'error': ['Enter a variable']}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit_invalid_varaible(self):
        command = "prev_limit"
        params = ['x!**(1/x)', 'x(', '0', '+-', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit_no_approach(self):
        command = "prev_limit"
        params = ['x!**(1/x)', 'x', '', '+-', 1, False, False]
        solution = {'error': ['Enter value that the variable approaches']}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit_invalid_approach(self):
        command = "prev_limit"
        params = ['x!**(1/x)', 'x', '(', '+-', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit(self):
        command = "prev_limit"
        params = ['x!**(1/x)', 'x', '0', '+-', 1, False, False]
        solution = {'limit': ['    x ____\nlim \\/ x! \nx->0      ', 0], 'latex': '\\lim_{x \\to 0} x!^{\\frac{1}{x}}'}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit_latex(self):
        command = "prev_limit"
        params = ['x!**(1/x)', 'x', '0', '+-', 2, False, False]
        solution = {'limit': ['\\lim_{x \\to 0} x!^{\\frac{1}{x}}', 0], 'latex': '\\lim_{x \\to 0} x!^{\\frac{1}{x}}'}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit_normal(self):
        command = "prev_limit"
        params = ['x!**(1/x)', 'x', '0', '+-', 3, False, False]
        solution = {'limit': ["Limit(factorial(x)**(1/x), x, 0, dir='+-')", 0], 'latex': '\\lim_{x \\to 0} x!^{\\frac{1}{x}}'}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit_var(self):
        command = "prev_limit"
        params = ['hi!**(1/hi)', 'hi', '0', '+-', 1, False, False]
        solution = {'limit': ['     hi_____\n lim \\/ hi! \nhi->0       ', 0], 'latex': '\\lim_{hi \\to 0} hi!^{\\frac{1}{hi}}'}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit_unicode(self):
        command = "prev_limit"
        params = ['x!**(1/x)', 'x', '0', '+-', 1, True, False]
        solution = {'limit': ['    x ____\nlim ╲╱ x! \nx─→0      ', 0], 'latex': '\\lim_{x \\to 0} x!^{\\frac{1}{x}}'}
        return command, params, solution

    @BaseTester.call_worker(LimitWorker)
    def test_prev_limit_side_specific(self):
        command = "prev_limit"
        params = ['x!**(1/x)', 'x', '0', '-', 1, False, False]
        solution = {'limit': ['     x ____\n lim \\/ x! \nx->0-      ', 0], 'latex': '\\lim_{x \\to 0^-} x!^{\\frac{1}{x}}'}
        return command, params, solution


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = PrevLimitTester()
    tester.test_limit_prev()
    sys.exit(app.exec_())
