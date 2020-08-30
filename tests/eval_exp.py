from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.evaluate import EvaluateWorker


class EvalExpTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_exp_eval(self):
        self.test_eval_exp_no_expression()
        self.test_eval_exp_invalid_expression()
        self.test_eval_exp()
        self.test_eval_exp_var_sub()
        self.test_eval_exp_var_sub_2()
        self.test_eval_exp_latex()
        self.test_eval_exp_normal()
        self.test_eval_exp_unicode()
        self.test_eval_exp_accuracy()
        self.test_eval_exp_scientific_notation()

    @BaseTester.call_worker(EvaluateWorker)
    def test_eval_exp_no_expression(self):
        command = "eval_exp"
        params = ['', '', 1, False, False, False, 10]
        solution = {'error': ['Enter an expression']}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_eval_exp_invalid_expression(self):
        command = "eval_exp"
        params = ['(', '', 1, False, False, False, 10]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_eval_exp(self):
        command = "eval_exp"
        params = ['sqrt(12)*sqrt(3)', '', 1, False, False, False, 10]
        solution = {'eval': ['6', '6.000000000'], 'latex': '6'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_eval_exp_var_sub(self):
        command = "eval_exp"
        params = ['x**3-2*pi*x', 'x: E', 1, False, False, False, 10]
        solution = {'eval': ['  /         2\\\nE*\\-2*pi + e /', '3.006068478'], 'latex': 'e \\left(- 2 \\pi + e^{2}\\right)'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_eval_exp_var_sub_2(self):
        command = "eval_exp"
        params = ['sqrt(3)*t', 't: 3', 1, False, False, False, 10]
        solution = {'eval': ['    ___\n3*\\/ 3 ', '5.196152423'], 'latex': '3 \\sqrt{3}'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_eval_exp_latex(self):
        command = "eval_exp"
        params = ['x**3-2*pi*x', 'x: E', 2, False, False, False, 10]
        solution = {'eval': ['e \\left(- 2 \\pi + e^{2}\\right)', '3.006068478'], 'latex': 'e \\left(- 2 \\pi + e^{2}\\right)'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_eval_exp_normal(self):
        command = "eval_exp"
        params = ['x**3-2*pi*x', 'x: E', 3, False, False, False, 10]
        solution = {'eval': ['E*(-2*pi + exp(2))', '3.006068478'], 'latex': 'e \\left(- 2 \\pi + e^{2}\\right)'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_eval_exp_unicode(self):
        command = "eval_exp"
        params = ['x**3-2*pi*x', 'x: E', 1, True, False, False, 10]
        solution = {'eval': ['  ⎛        2⎞\nℯ⋅⎝-2⋅π + ℯ ⎠', '3.006068478'], 'latex': 'e \\left(- 2 \\pi + e^{2}\\right)'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_eval_exp_accuracy(self):
        command = "eval_exp"
        params = ['x**3-2*pi*x', 'x: E', 1, False, False, False, 25]
        solution = {'eval': ['  /         2\\\nE*\\-2*pi + e /', '3.006068477840533610001428'], 'latex': 'e \\left(- 2 \\pi + e^{2}\\right)'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_eval_exp_scientific_notation(self):
        command = "eval_exp"
        params = ['x**3-2*pi*x', 'x: E', 1, False, False, 25, 10]
        solution = {'eval': ['  /         2\\\nE*\\-2*pi + e /', '3.006068477840533610001428*10**0'], 'latex': 'e \\left(- 2 \\pi + e^{2}\\right)'}
        return command, params, solution


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = EvalExpTester()
    tester.test_exp_eval()
    sys.exit(app.exec_())
