from PyQt5.QtWidgets import QApplication
from base_tester import BaseTester


class PrevExpandExpTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_exp_expand_prev(self):
        self.test_prev_expand_exp_no_expression()
        self.test_prev_expand_exp_invalid_expression()
        self.test_prev_expand_exp()
        self.test_prev_expand_exp_latex()
        self.test_prev_expand_exp_normal()
        self.test_prev_expand_exp_unicode()

    @BaseTester.call_worker
    def test_prev_expand_exp_no_expression(self):
        command = "prev_expand_exp"
        params = ['', 1, False, False]
        solution = {'error': ['Enter an expression']}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_expand_exp_invalid_expression(self):
        command = "prev_expand_exp"
        params = ['(', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_expand_exp(self):
        command = "prev_expand_exp"
        params = ['(a+b-c)**3', 1, False, False]
        solution = {'exp': ['           3\n(a + b - c) ', 0], 'latex': '\\left(a + b - c\\right)^{3}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_expand_exp_latex(self):
        command = "prev_expand_exp"
        params = ['(a+b-c)**3', 2, False, False]
        solution = {'exp': ['\\left(a + b - c\\right)^{3}', 0], 'latex': '\\left(a + b - c\\right)^{3}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_expand_exp_normal(self):
        command = "prev_expand_exp"
        params = ['(a+b-c)**3', 3, False, False]
        solution = {'exp': ['(a+b-c)**3', 0], 'latex': '\\left(a + b - c\\right)^{3}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_expand_exp_unicode(self):
        command = "prev_expand_exp"
        params = ['(a+b-pi)**3', 1, True, False]
        solution = {'exp': ['           3\n(a + b - π) ', 0], 'latex': '\\left(a + b - \\pi\\right)^{3}'}
        return command, params, solution


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = PrevExpandExpTester()
    tester.test_exp_expand_prev()
    sys.exit(app.exec_())
