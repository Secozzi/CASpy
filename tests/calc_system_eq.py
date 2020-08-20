from PyQt5.QtWidgets import QApplication
from base_tester import BaseTester


class CalcSystemEqTester(BaseTester):
    """This one might fail sometimes, but that's because SymPy likes to reorder variables sometimes.
    Rerun it if it fails until it doesn't"""
    def __init__(self):
        super().__init__()

    def test_system_eq_calc(self):
        self.test_calc_system_eq_no_expression()
        self.test_calc_system_eq_one_expression()
        self.test_calc_system_eq_too_many_equal()
        self.test_calc_system_eq_invalid_expression()
        self.test_calc_system_eq_no_variable()
        self.test_calc_system_eq_invalid_varaible()
        self.test_calc_system_eq_one_eq()
        self.test_calc_system_eq_system_1()
        self.test_calc_system_eq_system_2()
        self.test_calc_system_eq_latex()
        self.test_calc_system_eq_normal()
        self.test_calc_system_eq_unicode()
        self.test_calc_system_eq_accuracy()
        self.test_calc_system_eq_scientific_notation()
        self.test_calc_system_eq_verify_domain()

    @BaseTester.call_worker
    def test_calc_system_eq_no_expression(self):
        command = "calc_system_eq"
        params = [[''], '', 'Complexes', 1, False, False, False, 10, True]
        solution = {'error': ["Error: \nEnter only one '=' on line 1"]}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_one_expression(self):
        command = "calc_system_eq"
        params = [['x + y = 5', ''], 'x y', 'Complexes', 1, False, False, False, 10, True]
        solution = {'error': ["Error: \nEnter only one '=' on line 2"]}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_too_many_equal(self):
        command = "calc_system_eq"
        params = [['x + y = 5', 'x**2+y**2 = 17 = 2'], 'x y', 'Complexes', 1, False, False, False, 10, True]
        solution = {'error': ["Error: \nEnter only one '=' on line 2"]}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_invalid_expression(self):
        command = "calc_system_eq"
        params = [['x+y = 5(', 'x**2+y**2 = 17'], 'x y', 'Complexes', 1, False, False, False, 10, True]
        solution = {'error': ['Error: \nEquation number 1 is invalid']}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_no_variable(self):
        command = "calc_system_eq"
        params = [['x+y = 5', 'x**2+y**2 = 17'], '', 'Complexes', 1, False, False, False, 10, True]
        solution = {'error': ['Error: \nPlease enter at least one variable']}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_invalid_varaible(self):
        command = "calc_system_eq"
        params = [['x+y = 5', 'x**2+y**2 = 17 '], 'hello', 'Complexes', 1, False, False, False, 10, True]
        solution = {'error': ['Invalid variables']}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_one_eq(self):
        command = "calc_system_eq"
        params = [['y = x'], 'y', 'Complexes', 1, False, False, False, 10, True]
        solution = {'eq': ['[y = x]\n\n', ['y = x']], 'latex': '\\left[ y = x\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_system_1(self):
        command = "calc_system_eq"
        params = [['x+y = 5', 'x**2+y**2 = 17'], 'x y', 'Complexes', 1, False, False, False, 10, True]
        solution = {'eq': ['[x = 4, y = 1]\n\n[x = 1, y = 4]\n\n', [['x = 4.000000000', 'y = 1.000000000'], ['x = 1.000000000', 'y = 4.000000000']]], 'latex': '\\left[ x = 4, \\  y = 1\\right] \\\\ \\left[ x = 1, \\  y = 4\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_system_2(self):
        command = "calc_system_eq"
        params = [['2*x**2+y+z_1 = 1', 'x+2*y+z_1 = z_2', '-2*x+y = -z_1'], 'x y z_1', 'Complexes', 1, False, False, False, 10, True]
        solution = {'eq': ['             ___                ___                           ___ \n       1   \\/ 3             3*\\/ 3    3               5   5*\\/ 3  \n[x = - - + -----, y = z_2 - ------- + -, z_1 = -z_2 - - + -------]\n       2     2                 2      2               2      2    \n\n         ___                        ___                   ___     \n       \\/ 3    1            3   3*\\/ 3                5*\\/ 3    5 \n[x = - ----- - -, y = z_2 + - + -------, z_1 = -z_2 - ------- - -]\n         2     2            2      2                     2      2 \n\n', [['x = 0.3660254038', 'y = z_2 - 1.098076211', 'z_1 = 1.830127019 - z_2'], ['x = -1.366025404', 'y = z_2 + 4.098076211', 'z_1 = -z_2 - 6.830127019']]], 'latex': '\\left[ x = - \\frac{1}{2} + \\frac{\\sqrt{3}}{2}, \\  y = z_{2} - \\frac{3 \\sqrt{3}}{2} + \\frac{3}{2}, \\  z_{1} = - z_{2} - \\frac{5}{2} + \\frac{5 \\sqrt{3}}{2}\\right] \\\\ \\left[ x = - \\frac{\\sqrt{3}}{2} - \\frac{1}{2}, \\  y = z_{2} + \\frac{3}{2} + \\frac{3 \\sqrt{3}}{2}, \\  z_{1} = - z_{2} - \\frac{5 \\sqrt{3}}{2} - \\frac{5}{2}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_latex(self):
        command = "calc_system_eq"
        params = [['2*x**2+y+z_1 = 1', 'x+2*y+z_1 = z_2', '-2*x+y = -z_1'], 'x y z_1', 'Complexes', 2, False, False, False, 10, True]
        solution = {'eq': ['\\left[ x = - \\frac{1}{2} + \\frac{\\sqrt{3}}{2}, \\  y = z_{2} - \\frac{3 \\sqrt{3}}{2} + \\frac{3}{2}, \\  z_{1} = - z_{2} - \\frac{5}{2} + \\frac{5 \\sqrt{3}}{2}\\right] \\\\ \\left[ x = - \\frac{\\sqrt{3}}{2} - \\frac{1}{2}, \\  y = z_{2} + \\frac{3}{2} + \\frac{3 \\sqrt{3}}{2}, \\  z_{1} = - z_{2} - \\frac{5 \\sqrt{3}}{2} - \\frac{5}{2}\\right] \\\\ ', [['x = 0.3660254038', 'y = z_2 - 1.098076211', 'z_1 = 1.830127019 - z_2'], ['x = -1.366025404', 'y = z_2 + 4.098076211', 'z_1 = -z_2 - 6.830127019']]], 'latex': '\\left[ x = - \\frac{1}{2} + \\frac{\\sqrt{3}}{2}, \\  y = z_{2} - \\frac{3 \\sqrt{3}}{2} + \\frac{3}{2}, \\  z_{1} = - z_{2} - \\frac{5}{2} + \\frac{5 \\sqrt{3}}{2}\\right] \\\\ \\left[ x = - \\frac{\\sqrt{3}}{2} - \\frac{1}{2}, \\  y = z_{2} + \\frac{3}{2} + \\frac{3 \\sqrt{3}}{2}, \\  z_{1} = - z_{2} - \\frac{5 \\sqrt{3}}{2} - \\frac{5}{2}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_normal(self):
        command = "calc_system_eq"
        params = [['2*x**2+y+z_1 = 1', 'x+2*y+z_1 = z_2', '-2*x+y = -z_1'], 'x y z_1', 'Complexes', 3, False, False, False, 10, True]
        solution = {'eq': ['[[Eq(x, -1/2 + sqrt(3)/2), Eq(y, z_2 - 3*sqrt(3)/2 + 3/2), Eq(z_1, -z_2 - 5/2 + 5*sqrt(3)/2)], [Eq(x, -sqrt(3)/2 - 1/2), Eq(y, z_2 + 3/2 + 3*sqrt(3)/2), Eq(z_1, -z_2 - 5*sqrt(3)/2 - 5/2)]]', [['x = 0.3660254038', 'y = z_2 - 1.098076211', 'z_1 = 1.830127019 - z_2'], ['x = -1.366025404', 'y = z_2 + 4.098076211', 'z_1 = -z_2 - 6.830127019']]], 'latex': '\\left[ x = - \\frac{1}{2} + \\frac{\\sqrt{3}}{2}, \\  y = z_{2} - \\frac{3 \\sqrt{3}}{2} + \\frac{3}{2}, \\  z_{1} = - z_{2} - \\frac{5}{2} + \\frac{5 \\sqrt{3}}{2}\\right] \\\\ \\left[ x = - \\frac{\\sqrt{3}}{2} - \\frac{1}{2}, \\  y = z_{2} + \\frac{3}{2} + \\frac{3 \\sqrt{3}}{2}, \\  z_{1} = - z_{2} - \\frac{5 \\sqrt{3}}{2} - \\frac{5}{2}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_unicode(self):
        command = "calc_system_eq"
        params = [['2*x**2+y+z_1 = 1', 'x+2*y+z_1 = z_2', '-2*x+y = -z_1'], 'x y z_1', 'Complexes', 1, True, False, False, 10, True]
        solution = {'eq': ['⎡      1   √3           3⋅√3   3             5   5⋅√3⎤\n⎢x = - ─ + ──, y = z₂ - ──── + ─, z₁ = -z₂ - ─ + ────⎥\n⎣      2   2             2     2             2    2  ⎦\n\n⎡      √3   1           3   3⋅√3             5⋅√3   5⎤\n⎢x = - ── - ─, y = z₂ + ─ + ────, z₁ = -z₂ - ──── - ─⎥\n⎣      2    2           2    2                2     2⎦\n\n', [['x = 0.3660254038', 'y = z_2 - 1.098076211', 'z_1 = 1.830127019 - z_2'], ['x = -1.366025404', 'y = z_2 + 4.098076211', 'z_1 = -z_2 - 6.830127019']]], 'latex': '\\left[ x = - \\frac{1}{2} + \\frac{\\sqrt{3}}{2}, \\  y = z_{2} - \\frac{3 \\sqrt{3}}{2} + \\frac{3}{2}, \\  z_{1} = - z_{2} - \\frac{5}{2} + \\frac{5 \\sqrt{3}}{2}\\right] \\\\ \\left[ x = - \\frac{\\sqrt{3}}{2} - \\frac{1}{2}, \\  y = z_{2} + \\frac{3}{2} + \\frac{3 \\sqrt{3}}{2}, \\  z_{1} = - z_{2} - \\frac{5 \\sqrt{3}}{2} - \\frac{5}{2}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_accuracy(self):
        command = "calc_system_eq"
        params = [['2*x**2+y+z_1 = 1', 'x+2*y+z_1 = z_2', '-2*x+y = -z_1'], 'x y z_1', 'Complexes', 1, False, False, False, 25, True]
        solution = {'eq': ['             ___                ___                           ___ \n       1   \\/ 3             3*\\/ 3    3               5   5*\\/ 3  \n[x = - - + -----, y = z_2 - ------- + -, z_1 = -z_2 - - + -------]\n       2     2                 2      2               2      2    \n\n         ___                        ___                   ___     \n       \\/ 3    1            3   3*\\/ 3                5*\\/ 3    5 \n[x = - ----- - -, y = z_2 + - + -------, z_1 = -z_2 - ------- - -]\n         2     2            2      2                     2      2 \n\n', [['x = 0.3660254037844386467637232', 'y = z_2 - 1.098076211353315940291169', 'z_1 = 1.830127018922193233818616 - z_2'], ['x = -1.366025403784438646763723', 'y = z_2 + 4.098076211353315940291169', 'z_1 = -z_2 - 6.830127018922193233818616']]], 'latex': '\\left[ x = - \\frac{1}{2} + \\frac{\\sqrt{3}}{2}, \\  y = z_{2} - \\frac{3 \\sqrt{3}}{2} + \\frac{3}{2}, \\  z_{1} = - z_{2} - \\frac{5}{2} + \\frac{5 \\sqrt{3}}{2}\\right] \\\\ \\left[ x = - \\frac{\\sqrt{3}}{2} - \\frac{1}{2}, \\  y = z_{2} + \\frac{3}{2} + \\frac{3 \\sqrt{3}}{2}, \\  z_{1} = - z_{2} - \\frac{5 \\sqrt{3}}{2} - \\frac{5}{2}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_scientific_notation(self):
        command = "calc_system_eq"
        params = [['2*x**2+y+z_1 = 1', 'x+2*y+z_1 = z_2', '-2*x+y = -z_1'], 'x y z_1', 'Complexes', 1, False, False, 25, 10, True]
        solution = {'eq': ['             ___                ___                           ___ \n       1   \\/ 3             3*\\/ 3    3               5   5*\\/ 3  \n[x = - - + -----, y = z_2 - ------- + -, z_1 = -z_2 - - + -------]\n       2     2                 2      2               2      2    \n\n         ___                        ___                   ___     \n       \\/ 3    1            3   3*\\/ 3                5*\\/ 3    5 \n[x = - ----- - -, y = z_2 + - + -------, z_1 = -z_2 - ------- - -]\n         2     2            2      2                     2      2 \n\n', [['x = 3.660254037844386467637232*10**(-1)', 'y = z_2 - 1.098076211353315940291169', 'z_1 = 1.830127018922193233818616 - z_2'], ['x = -1.366025403784438646763723*10**0', 'y = z_2 + 4.098076211353315940291169', 'z_1 = -z_2 - 6.830127018922193233818616']]], 'latex': '\\left[ x = - \\frac{1}{2} + \\frac{\\sqrt{3}}{2}, \\  y = z_{2} - \\frac{3 \\sqrt{3}}{2} + \\frac{3}{2}, \\  z_{1} = - z_{2} - \\frac{5}{2} + \\frac{5 \\sqrt{3}}{2}\\right] \\\\ \\left[ x = - \\frac{\\sqrt{3}}{2} - \\frac{1}{2}, \\  y = z_{2} + \\frac{3}{2} + \\frac{3 \\sqrt{3}}{2}, \\  z_{1} = - z_{2} - \\frac{5 \\sqrt{3}}{2} - \\frac{5}{2}\\right]'}
        return command, params, solution

    @BaseTester.call_worker
    def test_calc_system_eq_verify_domain(self):
        command = "calc_system_eq"
        params = [['a*1000000**b = 119', 'a*1000**b = 450'], 'a b', 'Reals', 1, False, False, 25, 10, True]
        solution = {'eq': ['                    /         1    \\ \n                    |     ---------| \n                    |     3*log(10)| \n     202500         |/119\\         | \n[a = ------, b = log||---|         |]\n      119           \\\\450/         / \n\n', ['a = 1.701680672268907563025210*10**3', 'b = -1.925551841276043067079769*10**(-1)']], 'latex': '\\left[ a = \\frac{202500}{119}, \\  b = \\log{\\left(\\left(\\frac{119}{450}\\right)^{\\frac{1}{3 \\log{\\left(10 \\right)}}} \\right)}\\right]'}
        return command, params, solution


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    tester = CalcSystemEqTester()
    tester.test_system_eq_calc()
    sys.exit(app.exec_())
