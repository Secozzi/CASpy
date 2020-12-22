#
#    CASPy - A program that provides both a GUI and a CLI to SymPy.
#    Copyright (C) 2020 Folke Ishii
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

from __future__ import division

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable

from sympy import *
from sympy.parsing.sympy_parser import parse_expr

import typing as ty

from pyperclip import copy
import traceback


def catch_thread(func: ty.Callable[..., ty.Any]):
    """Decorator to catch any errors of a slot. This decorator shouldn't be called under normal circumstances"""

    def wrapper(*s, **gs):
        try:
            result = func(*s, **gs)
            return result
        except Exception:
            return {"error": [f"ERROR IN SOURCE CODE: \n\n{traceback.format_exc()}"]}

    return wrapper


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    output = pyqtSignal(dict)


class BaseWorker(QRunnable):
    def __init__(
        self, command: str, params: list, copy_output: ty.Union[int, None] = None
    ) -> None:
        super(BaseWorker, self).__init__()

        self.command = command
        self.params = params
        self.copy_output = copy_output

        self.signals = WorkerSignals()

    @staticmethod
    def catch_error(func: ty.Callable[..., ty.Any]):
        """Decorator for debugging. It will print params and copy result"""

        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
            except Exception:
                return {
                    "error": [f"ERROR IN SOURCE CODE: \n\n{traceback.format_exc()}"]
                }

            return result

        return wrapper

    @pyqtSlot()
    def run(self) -> ty.Union[ty.Dict[str, ty.List[str]], None]:
        try:
            result = getattr(self, self.command)(*self.params)
        except Exception:
            return {
                "error": [
                    f"Error calling function from worker thread: \n{traceback.format_exc()}"
                ]
            }

        # For tests
        if type(result) == list:
            if self.result[0] == "running":
                self.signals.output.emit({"running": result[1]})
                self.signals.finished.emit()
                return
        if type(result) == str:
            self.signals.output.emit({"answer": result})
            self.signals.finished.emit()
            return

        if self.copy_output:
            output = list(result.values())[0]
            if self.copy_output == 1:
                exact_ans = output[0]
                if type(exact_ans) == list:
                    if len(exact_ans) == 1:
                        copy(str(exact_ans[0]))
                else:
                    copy(str(exact_ans))
            elif self.copy_output == 2:
                approx_ans = output[1]
                if type(approx_ans) == list:
                    if len(approx_ans) == 1:
                        copy(str(approx_ans[0]))
                else:
                    copy(str(approx_ans))
            elif self.copy_output == 3:
                copy(str(output))
            else:
                pass

        self.signals.output.emit(result)
        self.signals.finished.emit()

    @catch_thread
    @pyqtSlot()
    def to_scientific_notation(self, number: str, accuracy: int = 5) -> str:
        """
        Converts number into the string "a*x**b" where a is a float and b is an integer unless it's not a number in the
        complex plane, such as infinity.
        For Complex numbers, a+b*i becomes c*10**d + e*10**f*I

        :param number: str
            number to be converted into
        :param accuracy: int
            accuracy of scientific notation
        :return: str
            scientific notation of number in string
        """

        # Is "a+b*i -> c*10**d + e*10**f*I" even a thing?
        # Can't find anything on internet but I'm implementing it like this for now

        number = str(number)
        sym_num = sympify(number)

        if not sym_num.is_complex:
            return number

        if type(accuracy) != int:
            print("Accuracy must be an integer over 1, defaulting to 5")
            accuracy = 5

        if accuracy < 1:
            print("Accuracy must be an integer over 1, defaulting to 5")
            accuracy = 5

        if sym_num.is_real:

            if sym_num < 0:
                negative = "-"
                number = number[1:]
                sym_num = sympify(number)
            else:
                negative = ""

            int_part = number.split(".")[0]
            no_decimal = number.replace(".", "")

            # convert it into 0.number, round it then convert it back into number
            output = str(sympify("0." + no_decimal).round(accuracy))[2:]
            if accuracy != 1:
                output = output[:2] + "." + output[2:]

            if sym_num < 1:
                zero_count = 0
                while zero_count < len(no_decimal) and no_decimal[zero_count] == "0":
                    zero_count += 1

                output = no_decimal[zero_count:]
                output = str(sympify("0." + output).round(accuracy))[2:]

                if accuracy != 1:
                    output = output[:1] + "." + output[1:]

                output += f"*10**(-{zero_count})"
                return negative + output
            else:
                output = str(sympify("0." + no_decimal).round(accuracy))[2:]
                if accuracy != 1:
                    output = output[:1] + "." + output[1:]

                output += "*10**" + str(len(int_part.replace("-", "")) - 1)
                return negative + output
        else:
            real = re(sym_num)
            imag = im(sym_num)

            real = self.to_scientific_notation(real, accuracy)
            imag = self.to_scientific_notation(imag, accuracy)

            output = real
            if sympify(imag) < 0:
                output += f" - {imag[1:]}*I"
            else:
                output += f" + {imag}*I"
            return output

    @catch_thread
    @pyqtSlot()
    def prev_normal_eq(
        self,
        left_expression: str,
        right_expression: str,
        input_variable: str,
        domain: str,
        output_type: int,
        use_unicode: bool,
        line_wrap: bool,
    ) -> ty.Dict[str, ty.List[str]]:
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if "=" in left_expression:
            if left_expression.count("=") > 1:
                return {"error": ["Enter only one equals sign"]}
            else:
                eq = left_expression.split("=")
                left_expression = eq[0]
                right_expression = eq[1]
        else:
            if not left_expression or not right_expression:
                return {"error": ["Enter an expression both in left and right side"]}

        if not input_variable:
            return {"error": ["Enter a variable"]}

        try:
            _ = parse_expr(input_variable)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        try:
            full_equation = Eq(
                parse_expr(left_expression), parse_expr(right_expression)
            )
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        self.latex_answer = str(latex(full_equation))

        if output_type == 1:
            self.exact_ans = str(pretty(full_equation))
        elif output_type == 2:
            self.exact_ans = self.latex_answer
        else:
            self.exact_ans = self.eq_to_text(full_equation)

        self.exact_ans += f"\nDomain: {domain}"

        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @catch_thread
    @pyqtSlot()
    def calc_normal_eq(
        self,
        left_expression: str,
        right_expression: str,
        input_variable: str,
        solve_type: int,
        domain: str,
        output_type: int,
        use_unicode: bool,
        line_wrap: bool,
        use_scientific: ty.Union[int, None],
        accuracy: int,
        verify_domain: bool,
        approximate: ty.Union[str, None] = None,
    ) -> ty.Dict[str, ty.List[str]]:
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if approximate == "":
            return {"error": ["Enter starting vector"]}

        try:
            domain = parse_expr(domain)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        if "=" in left_expression:
            if left_expression.count("=") > 1:
                return {"error": ["Enter only one equals sign"]}
            else:
                eq = left_expression.split("=")
                left_expression = eq[0]
                right_expression = eq[1]
        else:
            if not left_expression or not right_expression:
                return {"error": ["Enter an expression both in left and right side"]}

        if not input_variable:
            return {"error": ["Enter a variable"]}

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if approximate:
            try:
                _startv = parse_expr(approximate)
                self.exact_ans = nsolve(
                    Eq(parse_expr(left_expression), parse_expr(right_expression)),
                    parse_expr(input_variable),
                    _startv,
                    prec=accuracy
                )
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

            self.exact_ans = str(self.exact_ans)
            self.approx_ans = self.exact_ans
            self.latex_answer = str(latex(self.exact_ans))

            return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

        if solve_type == 1:
            try:
                self.exact_ans = solveset(
                    Eq(parse_expr(left_expression), parse_expr(right_expression)),
                    parse_expr(input_variable),
                    domain=domain,
                )
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

        else:
            try:
                self.exact_ans = solve(
                    Eq(parse_expr(left_expression), parse_expr(right_expression)),
                    parse_expr(input_variable),
                    domain=domain,
                    rational=True,
                )
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

            if verify_domain:
                self.exact_ans = self.verify_domain(self.exact_ans, domain)

            if type(self.exact_ans) != list:
                return self.exact_ans

            approx_list = [str(N(i, accuracy)) for i in self.exact_ans]

            if use_scientific:
                approx_list = [
                    self.to_scientific_notation(str(i), use_scientific)
                    for i in approx_list
                ]

            self.approx_ans = approx_list[0] if len(approx_list) == 1 else approx_list

        self.latex_answer = str(latex(self.exact_ans))
        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = [str(i) for i in self.exact_ans]

        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @catch_thread
    @pyqtSlot()
    def verify_domain(
        self, input_values: ty.List[Expr], domain: ty.Union[Set, Interval]
    ) -> ty.List[Expr]:
        output = []

        for value in input_values:

            if len(value.free_symbols) != 0:
                output.append(value)
            else:
                if type(domain.contains(value)) == Contains or not domain.contains(
                    value
                ):
                    pass
                else:
                    output.append(value)

        return output

    @catch_thread
    @pyqtSlot()
    def eq_to_text(self, equation: Eq) -> str:
        return f"{equation.lhs} = {equation.rhs}"
