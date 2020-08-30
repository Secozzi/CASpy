from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.integral import IntegralWorker


class CalcIntegTester(BaseTester):
    def __init__(self):
        super().__init__()

    def test_integ_calc(self):
        self.test_calc_integ_no_expression()
        self.test_calc_integ_invalid_expression()
        self.test_calc_integ_one_boundary()
        self.test_calc_integ_invalid_varaible()
        self.test_calc_integ()
        self.test_calc_integ_latex()
        self.test_calc_integ_normal()
        self.test_calc_integ_var()
        self.test_calc_integ_unicode()
        self.test_calc_integ_accuracy()
        self.test_calc_integ_scientific_notation()
        self.test_calc_integ_approximate_integral()
        self.test_calc_integ_cant_evaluate()

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_no_expression(self):
        command = "calc_integ"
        params = ['', 'x', '', '', False, 1, False, False, False, 10]
        solution = {'error': ['Enter an expression']}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_invalid_expression(self):
        command = "calc_integ"
        params = ['x**3(', 'x', '', '', False, 1, False, False, False, 10]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_one_boundary(self):
        command = "calc_integ"
        params = ['x**3', 'x', '2', '', False, 1, False, False, False, 10]
        solution = {'error': ['Enter both upper and lower bound']}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_invalid_varaible(self):
        command = "calc_integ"
        params = ['x**3', '(', '', '', False, 1, False, False, False, 10]
        solution = {'error': ['Error: \nTraceback']}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ(self):
        command = "calc_integ"
        params = ['1/(1+x**4)', 'x', '', '', False, 1, False, False, False, 10]
        solution = {'integ': ['    ___    / 2     ___      \\     ___    / 2     ___      \\     ___     /  ___      \\     ___     /  ___      \\\n  \\/ 2 *log\\x  - \\/ 2 *x + 1/   \\/ 2 *log\\x  + \\/ 2 *x + 1/   \\/ 2 *atan\\\\/ 2 *x - 1/   \\/ 2 *atan\\\\/ 2 *x + 1/\n- --------------------------- + --------------------------- + ----------------------- + -----------------------\n               8                             8                           4                         4           ', 0], 'latex': '- \\frac{\\sqrt{2} \\log{\\left(x^{2} - \\sqrt{2} x + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\log{\\left(x^{2} + \\sqrt{2} x + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} x - 1 \\right)}}{4} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} x + 1 \\right)}}{4}'}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_latex(self):
        command = "calc_integ"
        params = ['1/(1+x**4)', 'x', '', '', False, 2, False, False, False, 10]
        solution = {'integ': ['- \\frac{\\sqrt{2} \\log{\\left(x^{2} - \\sqrt{2} x + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\log{\\left(x^{2} + \\sqrt{2} x + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} x - 1 \\right)}}{4} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} x + 1 \\right)}}{4}', 0], 'latex': '- \\frac{\\sqrt{2} \\log{\\left(x^{2} - \\sqrt{2} x + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\log{\\left(x^{2} + \\sqrt{2} x + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} x - 1 \\right)}}{4} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} x + 1 \\right)}}{4}'}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_normal(self):
        command = "calc_integ"
        params = ['1/(1+x**4)', 'x', '', '', False, 3, False, False, False, 10]
        solution = {'integ': ['-sqrt(2)*log(x**2 - sqrt(2)*x + 1)/8 + sqrt(2)*log(x**2 + sqrt(2)*x + 1)/8 + sqrt(2)*atan(sqrt(2)*x - 1)/4 + sqrt(2)*atan(sqrt(2)*x + 1)/4', 0], 'latex': '- \\frac{\\sqrt{2} \\log{\\left(x^{2} - \\sqrt{2} x + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\log{\\left(x^{2} + \\sqrt{2} x + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} x - 1 \\right)}}{4} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} x + 1 \\right)}}{4}'}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_var(self):
        command = "calc_integ"
        params = ['1/(1+hi**4)', 'hi', '', '', False, 1, False, False, False, 10]
        solution = {'integ': ['    ___    /  2     ___       \\     ___    /  2     ___       \\     ___     /  ___       \\     ___     /  ___       \\\n  \\/ 2 *log\\hi  - \\/ 2 *hi + 1/   \\/ 2 *log\\hi  + \\/ 2 *hi + 1/   \\/ 2 *atan\\\\/ 2 *hi - 1/   \\/ 2 *atan\\\\/ 2 *hi + 1/\n- ----------------------------- + ----------------------------- + ------------------------ + ------------------------\n                8                               8                            4                          4            ', 0], 'latex': '- \\frac{\\sqrt{2} \\log{\\left(hi^{2} - \\sqrt{2} hi + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\log{\\left(hi^{2} + \\sqrt{2} hi + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} hi - 1 \\right)}}{4} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} hi + 1 \\right)}}{4}'}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_unicode(self):
        command = "calc_integ"
        params = ['1/(1+x**4)', 'x', '', '', False, 1, True, False, False, 10]
        solution = {'integ': ['        ⎛ 2           ⎞         ⎛ 2           ⎞                                        \n  √2⋅log⎝x  - √2⋅x + 1⎠   √2⋅log⎝x  + √2⋅x + 1⎠   √2⋅atan(√2⋅x - 1)   √2⋅atan(√2⋅x + 1)\n- ───────────────────── + ───────────────────── + ───────────────── + ─────────────────\n            8                       8                     4                   4        ', 0], 'latex': '- \\frac{\\sqrt{2} \\log{\\left(x^{2} - \\sqrt{2} x + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\log{\\left(x^{2} + \\sqrt{2} x + 1 \\right)}}{8} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} x - 1 \\right)}}{4} + \\frac{\\sqrt{2} \\operatorname{atan}{\\left(\\sqrt{2} x + 1 \\right)}}{4}'}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_accuracy(self):
        command = "calc_integ"
        params = ['1/sqrt(1-x**2)', 'x', '-1', '0', False, 1, False, False, False, 25]
        solution = {'integ': ['pi\n--\n2 ', '1.570796326794896619231322'], 'latex': '\\frac{\\pi}{2}'}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_scientific_notation(self):
        command = "calc_integ"
        params = ['1/sqrt(1-x**2)', 'x', '-1', '0', False, 1, False, False, 25, 10]
        solution = {'integ': ['pi\n--\n2 ', '1.570796326794896619231322*10**0'], 'latex': '\\frac{\\pi}{2}'}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_approximate_integral(self):
        command = "calc_integ"
        params = ['x**x', 'x', '-1', '0', True, 1, False, False, False, 10]
        solution = {'integ': ['0.04442317879 - 0.8573631716*I', '0.04442317879 - 0.8573631716*I'], 'latex': '0.04442317879 - 0.8573631716 i'}
        return command, params, solution

    @BaseTester.call_worker(IntegralWorker)
    def test_calc_integ_cant_evaluate(self):
        command = "calc_integ"
        params = ['x**x', 'x', '1', '2', False, 1, False, False, False, 10]
        solution = {'integ': ['Unable to evaluate integral:\n  2      \n  /      \n |       \n |   x   \n |  x  dx\n |       \n/        \n1        ', 'Integral(x**x, (x, 1, 2))'], 'latex': '\\int\\limits_{1}^{2} x^{x}\\, dx'}
        return command, params, solution

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = CalcIntegTester()
    tester.test_integ_calc()
    sys.exit(app.exec_())
