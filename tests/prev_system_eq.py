from PyQt5.QtWidgets import QApplication

from .base_tester import BaseTester
from caspy3.qt_assets.tabs.equations import EquationsWorker


class PrevSystemEqTester(BaseTester):
    """This one might fail sometimes, but that's because SymPy likes to reorder variables sometimes.
    Rerun it if it fails until it doesn't"""

    def __init__(self):
        super().__init__()

    def test_system_eq_prev(self):
        self.test_prev_system_eq_no_expression()
        self.test_prev_system_eq_one_expression()
        self.test_prev_system_eq_too_many_equal()
        self.test_prev_system_eq_invalid_expression()
        self.test_prev_system_eq_one_eq()
        self.test_prev_system_eq_system_1()
        self.test_prev_system_eq_ode()
        self.test_prev_system_eq_latex()
        self.test_prev_system_eq_normal()
        self.test_prev_system_eq_unicode()

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_system_eq_no_expression(self):
        command = "prev_system_eq"
        params = [[""], "", "Complexes", 1, 1, False, False]
        solution = {"error": ["Error: \nEnter only one '=' on line 1"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_system_eq_one_expression(self):
        command = "prev_system_eq"
        params = [["x+y = 5", ""], "x y", "Complexes", 1, 1, False, False]
        solution = {"error": ["Error: \nEnter only one '=' on line 2"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_system_eq_too_many_equal(self):
        command = "prev_system_eq"
        params = [
            ["x+y = 5", "x**2+y**2 = 17 = 2"],
            "x y",
            "Complexes",
            1,
            1,
            False,
            False,
        ]
        solution = {"error": ["Error: \nEnter only one '=' on line 2"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_system_eq_invalid_expression(self):
        command = "prev_system_eq"
        params = [
            ["x+y = 5(", "x**2+y**2 = 17"],
            "x y",
            "Complexes",
            1,
            1,
            False,
            False,
        ]
        solution = {"error": ["Error: \nEquation number 1 is invalid"]}
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_system_eq_one_eq(self):
        command = "prev_system_eq"
        params = [["y = x"], "y", "Complexes", 1, 1, False, False]
        solution = {
            "eq": ["Domain: S.Complexes\n\ny = x\n\nVariables to solve for: [y]", 0],
            "latex": "y = x",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_system_eq_system_1(self):
        command = "prev_system_eq"
        params = [["x+y = 5", "x**2+y**2 = 17"], "x y", "Complexes", 1, 1, False, False]
        solution = {
            "eq": [
                "Domain: S.Complexes\n\nx + y = 5\n\n 2    2     \nx  + y  = 17\n\nVariables to solve for: [x, y]",
                0,
            ],
            "latex": "x + y = 5 \\ x^{2} + y^{2} = 17",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_system_eq_ode(self):
        command = "prev_system_eq"
        params = [
            ["f'(x) = f(x)*g(x)*sin(x)", "g'(x) = g(x)**2*sin(x)"],
            "f(x) g(x)",
            "Complexes",
            2,
            1,
            False,
            False,
        ]
        solution = {
            "eq": [
                "Domain: S.Complexes\n\nd                          \n--(f(x)) = f(x)*g(x)*sin(x)\ndx                         \n\nd           2          \n--(g(x)) = g (x)*sin(x)\ndx                     \n\nVariables to solve for: [f(x), g(x)]",
                0,
            ],
            "latex": "\\frac{d}{d x} f{\\left(x \\right)} = f{\\left(x \\right)} g{\\left(x \\right)} \\sin{\\left(x \\right)} \\ \\frac{d}{d x} g{\\left(x \\right)} = g^{2}{\\left(x \\right)} \\sin{\\left(x \\right)}",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_system_eq_latex(self):
        command = "prev_system_eq"
        params = [["x+y = 5", "x**2+y**2 = 17"], "x y", "Complexes", 1, 2, False, False]
        solution = {
            "eq": [
                "Domain: S.Complexes\n\nx + y = 5\n\nx^{2} + y^{2} = 17\n\nVariables to solve for: [x, y]",
                0,
            ],
            "latex": "x + y = 5 \\ x^{2} + y^{2} = 17",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_system_eq_normal(self):
        command = "prev_system_eq"
        params = [["x+y = 5", "x**2+y**2 = 17"], "x y", "Complexes", 1, 3, False, False]
        solution = {
            "eq": [
                "Domain: S.Complexes\n\nx + y = 5\n\nx**2 + y**2 = 17\n\nVariables to solve for: [x, y]",
                0,
            ],
            "latex": "x + y = 5 \\ x^{2} + y^{2} = 17",
        }
        return command, params, solution

    @BaseTester.call_worker(EquationsWorker)
    def test_prev_system_eq_unicode(self):
        command = "prev_system_eq"
        params = [
            ["exp(x-y) = 2", "x**2+y**2 = 17"],
            "x y",
            "Complexes",
            1,
            1,
            True,
            False,
        ]
        solution = {
            "eq": [
                "Domain: S.Complexes\n\n x - y    \nℯ      = 2\n\n 2    2     \nx  + y  = 17\n\nVariables to solve for: [x, y]",
                0,
            ],
            "latex": "e^{x - y} = 2 \\ x^{2} + y^{2} = 17",
        }
        return command, params, solution


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tester = PrevSystemEqTester()
    tester.test_system_eq_prev()
    sys.exit(app.exec_())
