from PyQt5.QtWidgets import QApplication
from base_tester import BaseTester


class PrevSimpExpTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_exp_simp_prev(self):
        self.test_prev_simp_exp_no_expression()
        self.test_prev_simp_exp_invalid_expression()
        self.test_prev_simp_exp()
        self.test_prev_simp_exp_latex()
        self.test_prev_simp_exp_normal()
        self.test_prev_simp_exp_unicode()

    @BaseTester.call_worker
    def test_prev_simp_exp_no_expression(self):
        command = "prev_simp_exp"
        params = ['', 1, False, False]
        solution = {'error': ['Enter an expression']}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_simp_exp_invalid_expression(self):
        command = "prev_simp_exp"
        params = ['(', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_simp_exp(self):
        command = "prev_simp_exp"
        params = ['sin(x)**2+cos(x)**2', 1, False, False]
        solution = {'simp': ['   2         2   \nsin (x) + cos (x)', 0], 'latex': '\\sin^{2}{\\left(x \\right)} + \\cos^{2}{\\left(x \\right)}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_simp_exp_latex(self):
        command = "prev_simp_exp"
        params = ['sin(x)**2+cos(x)**2', 2, False, False]
        solution = {'simp': ['\\sin^{2}{\\left(x \\right)} + \\cos^{2}{\\left(x \\right)}', 0], 'latex': '\\sin^{2}{\\left(x \\right)} + \\cos^{2}{\\left(x \\right)}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_simp_exp_normal(self):
        command = "prev_simp_exp"
        params = ['sin(x)**2+cos(x)**2', 3, False, False]
        solution = {'simp': ['sin(x)**2+cos(x)**2', 0],'latex': '\\sin^{2}{\\left(x \\right)} + \\cos^{2}{\\left(x \\right)}'}
        return command, params, solution

    @BaseTester.call_worker
    def test_prev_simp_exp_unicode(self):
        command = "prev_simp_exp"
        params = ['exp(pi)', 1, True, False]
        solution = {'simp': [' π\nℯ ', 0], 'latex': 'e^{\\pi}'}
        return command, params, solution


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = PrevSimpExpTester()
    tester.test_exp_simp_prev()
    sys.exit(app.exec_())
