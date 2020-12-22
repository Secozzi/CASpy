from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.pf import PfWorker


class CalcPfTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_pf_calc(self):
        self.test_calc_pf_non_integer()
        self.test_calc_pf_0()
        self.test_calc_pf_1()
        self.test_calc_pf()

    @BaseTester.call_worker(PfWorker)
    def test_calc_pf_non_integer(self):
        command = "calc_pf"
        params = ["Hello"]
        solution = {"error": ["Error: Hello is not an integer."]}
        return command, params, solution

    @BaseTester.call_worker(PfWorker)
    def test_calc_pf_0(self):
        command = "calc_pf"
        params = [0]
        solution = {
            "error": ["Error: 0 is lower than 2, only number 2 and above is accepted."]
        }
        return command, params, solution

    @BaseTester.call_worker(PfWorker)
    def test_calc_pf_1(self):
        command = "calc_pf"
        params = [1]
        solution = {
            "error": ["Error: 1 is lower than 2, only number 2 and above is accepted."]
        }
        return command, params, solution

    @BaseTester.call_worker(PfWorker)
    def test_calc_pf(self):
        command = "calc_pf"
        params = [94136]
        solution = {
            "pf": [{2: 3, 7: 1, 41: 2}, "(2**3)*(7**1)*(41**2)"],
            "latex": "2^{3} \\cdot 41^{2} \\cdot 7^{1}",
        }
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = CalcPfTester()
    tester.test_pf_calc()
    sys.exit(app.exec_())
