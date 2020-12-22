from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.equations import EquationsWorker


class ParseDiffTextTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_text_diff_parse(self):
        self.test_parse_diff_text_no_apostrophe()
        self.test_parse_diff_text_one_apostrophe()
        self.test_parse_diff_text_two_apostrophe()
        self.test_parse_diff_text_five_apostrophe()

    @BaseTester.call_worker(EquationsWorker)
    def test_parse_diff_text_no_apostrophe(self):
        command = "parse_diff_text"
        params = ["f(x)"]
        solution = {"answer": "f(x)"}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_parse_diff_text_one_apostrophe(self):
        command = "parse_diff_text"
        params = ["f'(x)"]
        solution = {"answer": "f(x).diff(x,1)"}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_parse_diff_text_two_apostrophe(self):
        command = "parse_diff_text"
        params = ["g''(u)"]
        solution = {"answer": "g(u).diff(u,2)"}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_parse_diff_text_five_apostrophe(self):
        command = "parse_diff_text"
        params = ["ok'''''(hi)"]
        solution = {"answer": "ok(hi).diff(hi,5)"}
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = ParseDiffTextTester()
    tester.test_text_diff_parse()
    sys.exit(app.exec_())
