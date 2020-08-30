from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.summation import SummationWorker


class PrevSumTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_sum_prev(self):
        self.test_prev_sum_no_expression()
        self.test_prev_sum_invalid_expression()
        self.test_prev_sum_one_start()
        self.test_prev_sum_invalid_varaible()
        self.test_prev_sum_invalid_start()
        self.test_prev_sum()
        self.test_prev_sum_latex()
        self.test_prev_sum_normal()
        self.test_prev_sum_var()
        self.test_prev_sum_unicode()

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_no_expression(self):
        command = "prev_sum"
        params = ['', 'k', '1', 'm', 1, False, False]
        solution = {'error': ['Enter an expression']}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_invalid_expression(self):
        command = "prev_sum"
        params = ['k**2(', 'k', '1', 'm', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_one_start(self):
        command = "prev_sum"
        params = ['k**2', 'k', '', 'm', 1, False, False]
        solution = {'error': ['Enter both start and end']}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_invalid_varaible(self):
        command = "prev_sum"
        params = ['k**2', 'k(', '1', 'm', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_invalid_start(self):
        command = "prev_sum"
        params = ['k**2', 'k', '1(', 'm', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum(self):
        command = "prev_sum"
        params = ['k**2', 'k', '1', 'm', 1, False, False]
        solution = {'sum': ['  m     \n ___    \n \\  `   \n  \\    2\n  /   k \n /__,   \nk = 1   ', 0], 'latex': '\\sum_{k=1}^{m} k^{2}'}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_latex(self):
        command = "prev_sum"
        params = ['k**2', 'k', '1', 'm', 2, False, False]
        solution = {'sum': ['\\sum_{k=1}^{m} k^{2}', 0], 'latex': '\\sum_{k=1}^{m} k^{2}'}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_normal(self):
        command = "prev_sum"
        params = ['k**2', 'k', '1', 'm', 3, False, False]
        solution = {'sum': ['Sum(k**2, (k, 1, m))', 0], 'latex': '\\sum_{k=1}^{m} k^{2}'}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_var(self):
        command = "prev_sum"
        params = ['hi**2', 'hi', '1', 'm', 1, False, False]
        solution = {'sum': ['  m       \n ___      \n \\  `     \n  \\      2\n  /    hi \n /__,     \nhi = 1    ', 0], 'latex': '\\sum_{hi=1}^{m} hi^{2}'}
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_unicode(self):
        command = "prev_sum"
        params = ['k**2', 'k', '1', 'm', 1, True, False]
        solution = {'sum': ['  m     \n ___    \n ╲      \n  ╲    2\n  ╱   k \n ╱      \n ‾‾‾    \nk = 1   ', 0], 'latex': '\\sum_{k=1}^{m} k^{2}'}
        return command, params, solution


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = PrevSumTester()
    tester.test_sum_prev()
    sys.exit(app.exec_())
