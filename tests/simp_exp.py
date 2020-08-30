from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.simplify import SimpWorker


class SimpExpTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_exp_simp(self):
        self.test_simp_exp_no_expression()
        self.test_simp_exp_invalid_expression()
        self.test_simp_exp()
        self.test_simp_exp_latex()
        self.test_simp_exp_normal()
        self.test_simp_exp_unicode()

    @BaseTester.call_worker(SimpWorker)
    def test_simp_exp_no_expression(self):
        command = "simp_exp"
        params = ['', 1, False, False]
        solution = {'error': ['Enter an expression']}
        return command, params, solution

    @BaseTester.call_worker(SimpWorker)
    def test_simp_exp_invalid_expression(self):
        command = "simp_exp"
        params = ['(', 1, False, False]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker(SimpWorker)
    def test_simp_exp(self):
        command = "simp_exp"
        params = ['4*sin(x)**2 - sin(x)**2', 1, False, False]
        solution = {'simp': ['     2   \n3*sin (x)', 0], 'latex': '3 \\sin^{2}{\\left(x \\right)}'}
        return command, params, solution

    @BaseTester.call_worker(SimpWorker)
    def test_simp_exp_latex(self):
        command = "simp_exp"
        params = ['4*sin(x)**2 - sin(x)**2', 2, False, False]
        solution = {'simp': ['3 \\sin^{2}{\\left(x \\right)}', 0], 'latex': '3 \\sin^{2}{\\left(x \\right)}'}
        return command, params, solution

    @BaseTester.call_worker(SimpWorker)
    def test_simp_exp_normal(self):
        command = "simp_exp"
        params = ['4*sin(x)**2 - sin(x)**2', 3, False, False]
        solution = {'simp': ['3*sin(x)**2', 0], 'latex': '3 \\sin^{2}{\\left(x \\right)}'}
        return command, params, solution

    @BaseTester.call_worker(SimpWorker)
    def test_simp_exp_unicode(self):
        command = "simp_exp"
        params = ['4*sin(x)**pi - sin(x)**pi', 1, True, False]
        solution = {'simp': ['     π   \n3⋅sin (x)', 0], 'latex': '3 \\sin^{\\pi}{\\left(x \\right)}'}
        return command, params, solution


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = SimpExpTester()
    tester.test_exp_simp()
    sys.exit(app.exec_())
