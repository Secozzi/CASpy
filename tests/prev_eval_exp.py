from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.evaluate import EvaluateWorker


class PrevEvalExpTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_exp_eval_prev(self):
        self.test_prev_eval_exp_no_expression()
        self.test_prev_eval_exp_invalid_expression()
        self.test_prev_eval_exp()
        self.test_prev_eval_exp_var_sub()
        self.test_prev_eval_exp_var_sub_2()
        self.test_prev_eval_exp_latex()
        self.test_prev_eval_exp_normal()
        self.test_prev_eval_exp_unicode()

    @BaseTester.call_worker(EvaluateWorker)
    def test_prev_eval_exp_no_expression(self):
        command = "prev_eval_exp"
        params = ['', '', 1, False, False]
        solution = {'error': ['Enter an expression']}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_prev_eval_exp_invalid_expression(self):
        command = "prev_eval_exp"
        params = ['(', '', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_prev_eval_exp(self):
        command = "prev_eval_exp"
        params = ['sqrt(12)*sqrt(3)', '', 1, False, False]
        solution = {'eval': ['  ___     ___\n\\/ 3 *2*\\/ 3 ', 0], 'latex': '\\sqrt{3} \\cdot 2 \\sqrt{3}'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_prev_eval_exp_var_sub(self):
        command = "prev_eval_exp"
        params = ['x**3-2*pi*x', 'x: E', 1, False, False]
        solution = {'eval': ['With variable substitution x: E\n 3         \nx  - 2*pi*x', 0], 'latex': 'x^{3} - 2 \\pi x'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_prev_eval_exp_var_sub_2(self):
        command = "prev_eval_exp"
        params = ['sqrt(3)*t', 't: 3', 1, False, False]
        solution = {'eval': ['With variable substitution t: 3\n  ___  \n\\/ 3 *t', 0], 'latex': '\\sqrt{3} t'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_prev_eval_exp_latex(self):
        command = "prev_eval_exp"
        params = ['x**3-2*pi*x', 'x: E', 2, False, False]
        solution = {'eval': ['With variable substitution x: E\nx^{3} - 2 \\pi x', 0], 'latex': 'x^{3} - 2 \\pi x'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_prev_eval_exp_normal(self):
        command = "prev_eval_exp"
        params = ['x**3-2*pi*x', 'x: E', 3, False, False]
        solution = {'eval': ['With variable substitution x: E\nx**3-2*pi*x', 0], 'latex': 'x^{3} - 2 \\pi x'}
        return command, params, solution

    @BaseTester.call_worker(EvaluateWorker)
    def test_prev_eval_exp_unicode(self):
        command = "prev_eval_exp"
        params = ['x**3-2*pi*x', 'x: E', 1, True, False]
        solution = {'eval': ['With variable substitution x: E\n 3        \nx  - 2⋅π⋅x', 0], 'latex': 'x^{3} - 2 \\pi x'}
        return command, params, solution


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = PrevEvalExpTester()
    tester.test_exp_eval_prev()
    sys.exit(app.exec_())
