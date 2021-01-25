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


def test_prev_deriv_no_expression(qtbot):
    app = DerivativeWorker(
        "prev_deriv",
        ["", "x", 1, "", 1, False, False, {}],
    )
    answer = {"error": ["Enter an expression"]}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_prev_deriv_invalid_expression(qtbot):
    app = DerivativeWorker(
        "prev_deriv",
        ["(", "x", 1, "", 1, False, False, {}],
    )

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert is_traceback(blocker)


def test_prev_deriv_no_variable(qtbot):
    app = DerivativeWorker(
        "prev_deriv",
        ["x**x", "", 1, "", 1, False, False, {}],
    )
    answer = {"error": ["Enter a variable"]}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_prev_deriv_invalid_variable(qtbot):
    app = DerivativeWorker(
        "prev_deriv",
        ["x**x", "(", 1, "", 1, False, False, {}],
    )

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert is_traceback(blocker)


def test_prev_deriv(qtbot):
    app = DerivativeWorker(
        "prev_deriv",
        ["x**x", "x", 1, "", 1, False, False, {}],
    )
    deriv = Derivative("x**x", "x")
    exact_ans = pretty(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_prev_deriv_latex(qtbot):
    app = DerivativeWorker(
        "prev_deriv",
        ["x**x", "x", 1, "", 2, False, False, {}],
    )
    deriv = Derivative("x**x", "x")
    exact_ans = latex(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_prev_deriv_normal(qtbot):
    app = DerivativeWorker(
        "prev_deriv",
        ["x**x", "x", 1, "", 3, False, False, {}],
    )
    deriv = Derivative("x**x", "x")
    exact_ans = str(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_prev_deriv_order(qtbot):
    app = DerivativeWorker(
        "prev_deriv",
        ["x**x", "x", 2, "", 1, False, False, {}],
    )
    deriv = Derivative("x**x", "x", 2)
    exact_ans = pretty(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_prev_deriv_point(qtbot):
    app = DerivativeWorker(
        "prev_deriv",
        ["x**x", "x", 1, "pi", 1, False, False, {}],
    )
    deriv = Derivative("x**x", "x")
    exact_ans = "At x = pi\n"
    exact_ans += pretty(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_prev_deriv_var(qtbot):
    app = DerivativeWorker(
        "prev_deriv",
        ["g**g", "g", 1, "", 1, False, False, {}],
    )
    deriv = Derivative("g**g", "g")
    exact_ans = pretty(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]


def test_prev_deriv_unicode(qtbot):
    app = DerivativeWorker(
        "prev_deriv",
        ["x**x", "x", 1, "", 1, True, False, {}],
    )
    init_printing(use_unicode=True)
    deriv = Derivative("x**x", "x")
    exact_ans = pretty(deriv)
    approx_ans = "..."
    latex_ans = latex(deriv)

    answer = {"deriv": [exact_ans, approx_ans], "latex": latex_ans}

    with qtbot.waitSignal(app.signals.finished, raising=False) as blocker:
        blocker.connect(app.signals.output)
        app.run()

    assert blocker.args == [answer]

