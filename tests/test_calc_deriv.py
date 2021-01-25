#
#    CASPy - A program that provides both a GUI and a CLI to SymPy.
#    Copyright (C) 2021 Folke Ishii
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

# Third party
from sympy import *
from sympy.abc import _clash2

# Relative
from caspy3.qt_assets.tabs.derivative import DerivativeWorker
from .utils import is_traceback, to_scientific_notation


def test_calc_deriv_no_expression(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["", "x", 1, "", 1, False, False, {}, 0, 10, ],
    )
    answer = {"error": ["Enter an expression"]}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_calc_deriv_invalid_expression(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["(", "x", 1, "", 1, False, False, {}, 0, 10, ],
    )

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args[0]["error"][0].startswith("Error: \nTraceback (most recent call last):")


def test_calc_deriv_no_variable(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["x**x", "", 1, "", 1, False, False, {}, 0, 10, ],
    )
    answer = {"error": ["Enter a variable"]}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_calc_deriv_invalid_variable(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["x**x", "(", 1, "", 1, False, False, {}, 0, 10, ],
    )

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert is_traceback(blocker)
    #assert blocker.args[0]["error"][0].startswith("Error: \nTraceback (most recent call last):")


def test_calc_deriv(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["x**x", "x", 1, "", 1, False, False, {}, 0, 10, ],
    )
    deriv = diff("x**x", "x")
    exact_ans = pretty(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_calc_deriv_latex(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["x**x", "x", 1, "", 2, False, False, {}, 0, 10, ],
    )
    deriv = diff("x**x", "x")
    exact_ans = latex(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_calc_deriv_normal(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["x**x", "x", 1, "", 3, False, False, {}, 0, 10, ],
    )
    deriv = diff("x**x", "x")
    exact_ans = str(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {
        "deriv": [exact_ans, approx_ans],
        "latex": latex_ans
    }

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_calc_deriv_order(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["x**x", "x", 4, "", 1, False, False, {}, 0, 10],
    )
    init_printing()
    deriv = diff("x**x", "x", 4)
    exact_ans = pretty(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {
        "deriv": [exact_ans, approx_ans],
        "latex": latex_ans
    }

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_calc_deriv_point(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["tan(a)", "a", 1, "pi/E", 1, False, False, {}, 0, 10],
    )
    init_printing()
    deriv = diff("tan(a)", "a", 1).subs("a", "pi/E")
    exact_ans = pretty(deriv)
    approx_ans = N(deriv, 10)
    latex_ans = latex(deriv)

    answer = {
        "deriv": [str(exact_ans), str(approx_ans)],
        "latex": latex_ans
    }

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert type(blocker.args[0]["deriv"][1]) == str
    assert blocker.args == [answer]


def test_calc_deriv_unicode(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["x**x", "x", 1, "", 1, True, False, {}, 0, 10, ],
    )
    init_printing(use_unicode=True)
    deriv = diff("x**x", "x")
    exact_ans = pretty(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_calc_deriv_line_wrap(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["sin(x**x)", "x", 5, "", 1, False, True, {}, 0, 10, ],
    )
    init_printing(use_unicode=False, wrap_line=True)
    deriv = diff("sin(x**x)", "x", 5)
    exact_ans = pretty(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_calc_deriv_accuracy(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["tan(a)", "a", 1, "pi/E", 1, False, False, {}, 0, 50],
    )
    init_printing(wrap_line=False)
    deriv = diff("tan(a)", "a", 1).subs("a", "pi/E")
    exact_ans = pretty(deriv)
    approx_ans = N(deriv, 50)
    latex_ans = latex(deriv)

    answer = {
        "deriv": [str(exact_ans), str(approx_ans)],
        "latex": latex_ans
    }

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_calc_deriv_scientific_notation(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["tan(a)", "a", 1, "pi/E", 1, False, False, {}, 20, 10],
    )
    deriv = diff("tan(a)", "a", 1).subs("a", "pi/E")
    exact_ans = pretty(deriv)
    approx_ans = N(deriv, 20)
    approx_ans = to_scientific_notation(str(approx_ans), 20)
    latex_ans = latex(deriv)

    answer = {
        "deriv": [str(exact_ans), str(approx_ans)],
        "latex": latex_ans
    }

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_deriv_clash(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["pi**pi", "pi", 1, "", 1, False, False, {}, 0, 10],
    )

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert is_traceback(blocker)


def test_deriv_avoid_clash(qtbot):
    app = DerivativeWorker(
        "calc_deriv",
        ["pi**pi", "pi", 1, "", 1, False, False, _clash2, 0, 10, ],
    )
    deriv = diff(
        parse_expr("pi**pi", local_dict=_clash2),
        parse_expr("pi", local_dict=_clash2)
    )
    exact_ans = pretty(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]
