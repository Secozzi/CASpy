from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.expand import ExpandWorker


class ExpandExpTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_exp_expand(self):
        self.test_expand_exp_no_expression()
        self.test_expand_exp_invalid_expression()
        self.test_expand_exp()
        self.test_expand_exp_latex()
        self.test_expand_exp_normal()
        self.test_expand_exp_unicode()

    @BaseTester.call_worker(ExpandWorker)
    def test_expand_exp_no_expression(self):
        command = "expand_exp"
        params = ['', 1, False, False]
        solution = {'error': ['Enter an expression']}
        return command, params, solution

    @BaseTester.call_worker(ExpandWorker)
    def test_expand_exp_invalid_expression(self):
        command = "expand_exp"
        params = ['(', 1, False, False]
        solution = {"error": ["Error: \nTraceback"]}
        return command, params, solution

    @BaseTester.call_worker(ExpandWorker)
    def test_expand_exp(self):
        command = "expand_exp"
        params = ['(a+b-c)**3', 1, False, False]
        solution = {'exp': [' 3      2        2          2                  2    3      2          2    3\na  + 3*a *b - 3*a *c + 3*a*b  - 6*a*b*c + 3*a*c  + b  - 3*b *c + 3*b*c  - c ', 0], 'latex': 'a^{3} + 3 a^{2} b - 3 a^{2} c + 3 a b^{2} - 6 a b c + 3 a c^{2} + b^{3} - 3 b^{2} c + 3 b c^{2} - c^{3}'}
        return command, params, solution

    @BaseTester.call_worker(ExpandWorker)
    def test_expand_exp_latex(self):
        command = "expand_exp"
        params = ['(a+b-c)**3', 2, False, False]
        solution = {'exp': ['a^{3} + 3 a^{2} b - 3 a^{2} c + 3 a b^{2} - 6 a b c + 3 a c^{2} + b^{3} - 3 b^{2} c + 3 b c^{2} - c^{3}', 0], 'latex': 'a^{3} + 3 a^{2} b - 3 a^{2} c + 3 a b^{2} - 6 a b c + 3 a c^{2} + b^{3} - 3 b^{2} c + 3 b c^{2} - c^{3}'}
        return command, params, solution

    @BaseTester.call_worker(ExpandWorker)
    def test_expand_exp_normal(self):
        command = "expand_exp"
        params = ['(a+b-c)**3', 3, False, False]
        solution = {'exp': ['a**3 + 3*a**2*b - 3*a**2*c + 3*a*b**2 - 6*a*b*c + 3*a*c**2 + b**3 - 3*b**2*c + 3*b*c**2 - c**3', 0], 'latex': 'a^{3} + 3 a^{2} b - 3 a^{2} c + 3 a b^{2} - 6 a b c + 3 a c^{2} + b^{3} - 3 b^{2} c + 3 b c^{2} - c^{3}'}
        return command, params, solution

    @BaseTester.call_worker(ExpandWorker)
    def test_expand_exp_unicode(self):
        command = "expand_exp"
        params = ['(a+b-pi)**3', 1, True, False]
        solution = {'exp': [' 3      2          2        2                2      3        2      2      3\na  + 3⋅a ⋅b - 3⋅π⋅a  + 3⋅a⋅b  - 6⋅π⋅a⋅b + 3⋅π ⋅a + b  - 3⋅π⋅b  + 3⋅π ⋅b - π ', 0], 'latex': 'a^{3} + 3 a^{2} b - 3 \\pi a^{2} + 3 a b^{2} - 6 \\pi a b + 3 \\pi^{2} a + b^{3} - 3 \\pi b^{2} + 3 \\pi^{2} b - \\pi^{3}'}
        return command, params, solution


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = ExpandExpTester()
    tester.test_exp_expand()
    sys.exit(app.exec_())
