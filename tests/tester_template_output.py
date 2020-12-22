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
        params = 0
        solution = 0
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_invalid_expression(self):
        command = "prev_sum"
        params = 0
        solution = 0
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_one_start(self):
        command = "prev_sum"
        params = 0
        solution = 0
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_invalid_varaible(self):
        command = "prev_sum"
        params = 0
        solution = 0
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_invalid_start(self):
        command = "prev_sum"
        params = 0
        solution = 0
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum(self):
        command = "prev_sum"
        params = 0
        solution = 0
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_latex(self):
        command = "prev_sum"
        params = 0
        solution = 0
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_normal(self):
        command = "prev_sum"
        params = 0
        solution = 0
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_var(self):
        command = "prev_sum"
        params = 0
        solution = 0
        return command, params, solution

    @BaseTester.call_worker(SummationWorker)
    def test_prev_sum_unicode(self):
        command = "prev_sum"
        params = 0
        solution = 0
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = PrevSumTester()
    tester.test_sum_prev()
    sys.exit(app.exec_())
