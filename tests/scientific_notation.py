from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.worker import BaseWorker


class ScientificNotationTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_scientific_notation(self):
        self.test_to_scientific_notation()
        self.test_to_scientific_notation_negative_number()
        self.test_to_scientific_notation_large_number()
        self.test_to_scientific_notation_small_number()
        self.test_to_scientific_notation_accuracy()
        self.test_to_scientific_notation_invalid_accuracy()
        self.test_to_scientific_notation_non_complex_number()
        self.test_to_scientific_notation_complex()

    @BaseTester.call_worker(BaseWorker)
    def test_to_scientific_notation(self):
        command = "to_scientific_notation"
        params = ["12345"]
        solution = {"answer": "1.2345*10**4"}
        return command, params, solution

    @BaseTester.call_worker(BaseWorker)
    def test_to_scientific_notation_negative_number(self):
        command = "to_scientific_notation"
        params = ["-4345"]
        solution = {"answer": "-4.3450*10**3"}
        return command, params, solution

    @BaseTester.call_worker(BaseWorker)
    def test_to_scientific_notation_large_number(self):
        command = "to_scientific_notation"
        params = ["18446744073709551616"]
        solution = {"answer": "1.8447*10**19"}
        return command, params, solution

    @BaseTester.call_worker(BaseWorker)
    def test_to_scientific_notation_small_number(self):
        command = "to_scientific_notation"
        params = ["0.00000005747"]
        solution = {"answer": "5.7470*10**(-8)"}
        return command, params, solution

    @BaseTester.call_worker(BaseWorker)
    def test_to_scientific_notation_accuracy(self):
        command = "to_scientific_notation"
        params = ["18446744073709551616", 15]
        solution = {"answer": "1.84467440737096*10**19"}
        return command, params, solution

    @BaseTester.call_worker(BaseWorker)
    def test_to_scientific_notation_invalid_accuracy(self):
        command = "to_scientific_notation"
        params = ["18446744073709551616", "15"]
        solution = {"answer": "1.8447*10**19"}
        return command, params, solution

    @BaseTester.call_worker(BaseWorker)
    def test_to_scientific_notation_non_complex_number(self):
        command = "to_scientific_notation"
        params = ["-oo"]
        solution = {"answer": "-oo"}
        return command, params, solution

    @BaseTester.call_worker(BaseWorker)
    def test_to_scientific_notation_complex(self):
        command = "to_scientific_notation"
        params = [
            "-0.109021273701475854840359048696 - 0.500507948960587890643366835011*I",
            10,
        ]
        solution = {"answer": "-1.090212737*10**(-1) - 5.005079490*10**(-1)*I"}
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = ScientificNotationTester()
    tester.test_scientific_notation()
    sys.exit(app.exec_())
