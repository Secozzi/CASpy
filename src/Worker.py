from __future__ import division

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable
from sympy import *
from sympy.abc import _clash1
from sympy.parsing.sympy_parser import parse_expr
from pyperclip import copy

x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)

import traceback

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    output = pyqtSignal(dict)

class CASWorker(QRunnable):
    def __init__(self, type, params, copy=None):
        super(CASWorker, self).__init__()

        self.type = type
        self.params = params
        self.copy = copy

        self.signals = WorkerSignals()

    def create_code_list(self):
        self.previous_code_list = []

    @pyqtSlot()
    def run(self):
        try:
            result = getattr(self, self.type)(*self.params)
        except:
            return({"error": f"Error calling function from worker thread: \n{traceback.format_exc()}"})

        output = list(result.values())[0]
        if self.copy == 1:
            exact_ans = output[0]
            if type(exact_ans) == list:
                if len(exact_ans) == 1:
                    copy(str(exact_ans[0]))
            else:
                copy(str(exact_ans))
        elif self.copy == 2:
            approx_ans = output[1]
            if type(approx_ans) == list:
                if len(approx_ans) == 1:
                    copy(str(approx_ans[0]))
            else:
                copy(str(approx_ans))
        elif self.copy == 3:
            copy(str(output))
        else:
            pass

        self.signals.output.emit(result)
        self.signals.finished.emit()

    # OUTPUTTYPE: 1: PRETTY; 2: LATEX; 3: NORMAL
    # SOLVETYPE: 1: SOLVESET; 2: SOLVE

    @pyqtSlot()
    def to_scientific_notation(self, number, accuracy=5):
        """
        Converts number into the string "a*x**b" where a is a float and b is an integer unless it's not a number in the complex plane, such as infinity
        For Complex numbers, a+b*i becomes c*10**d + e*10**f*I

        :param number: number
            number to be converted into
        :param accuracy: int
            accuracy of scientific notation
        :return: str
            scientific notation of number in string
        """

        number = str(number)
        sym_num = sympify(number)

        if not sym_num.is_complex:
            return number

        if accuracy < 1 or type(accuracy) != int:
            print("Accuracy must be integer over 1, defaulting to 5")
            accuracy = 5

        if sym_num.is_real:
            if sym_num < 0:
                negative = "-"
                number = number[1:]
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
            real = str(re(sym_num))
            imag = str(im(sym_num))

            real = self.to_scientific_notation(real, accuracy)
            imag = self.to_scientific_notation(imag, accuracy)

            output = real
            if sympify(imag) < 0:
                output += f" - {imag[1:]}*I"
            else:
                output += f" + {imag}*I"
            return output

    @pyqtSlot()
    def prev_deriv(self, input_expression, input_variable, input_order, input_point, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        if not input_expression:
            return({"error": ["Enter an expression"]})
        if not input_variable:
            return({"error": ["Enter a variable"]})

        try:
            derivative = Derivative(str(input_expression), input_variable, input_order)
        except Exception:
            return({"error": [f"Error: \n{traceback.format_exc()}"]})
        if input_point:
            self.exact_ans = f"At x = {input_point}\n"
        if output_type == 1:
            self.exact_ans += str(pretty(derivative))
        elif output_type == 2:
            self.exact_ans += str(latex(derivative))
        else:
            self.exact_ans += str(derivative)
        return({"deriv": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def calc_deriv(self, input_expression, input_variable, input_order, input_point, output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not input_expression:
            return ({"error": ["Enter an expression"]})
        if not input_variable:
            return({"error": ["Enter a variable"]})

        try:
            self.exact_ans = diff(parse_expr(input_expression), parse_expr(input_variable), input_order)
        except Exception:
            return({"error": [f"Error: \n{traceback.format_exc()}"]})

        if input_point:
            calc_deriv_point = str(self.exact_ans).replace(input_variable, f"({input_point})")
            if use_scientific:
                self.approx_ans = self.to_scientific_notation(str(N(calc_deriv_point, accuracy)), use_scientific)
            else:
                self.approx_ans = str(N(calc_deriv_point, accuracy))
            if output_type == 1:
                self.exact_ans = str(pretty(simplify(calc_deriv_point)))
            elif output_type == 2:
                self.exact_ans = str(latex(simplify(calc_deriv_point)))
            else:
                self.exact_ans = str(simplify(calc_deriv_point))
        else:
            if output_type == 1:
                self.exact_ans = str(pretty(self.exact_ans))
            elif output_type == 2:
                self.exact_ans = str(latex(self.exact_ans))
            else:
                self.exact_ans = str(self.exact_ans)
        return({"deriv": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def prev_integ(self, input_expression, input_variable, input_lower, input_upper, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        if not input_expression:
            return({"error": ["Enter an expression"]})
        if not input_variable:
            return ({"error": ["Enter a variable"]})
        if (input_lower and not input_upper) or (not input_lower and input_upper):
            return({"error": ["Enter both upper and lower bound"]})

        if input_lower:
            try:
                self.exact_ans = Integral(parse_expr(input_expression), (
                parse_expr(input_variable), input_lower, input_upper))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
        else:
            try:
                self.exact_ans = Integral(parse_expr(input_expression), parse_expr(input_variable))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)
        return({"integ": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def calc_integ(self, input_expression, input_variable, input_lower, input_upper, output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not input_expression:
            return({"error": ["Enter an expression"]})
        if not input_variable:
            return ({"error": ["Enter a variable"]})
        if (input_lower and not input_upper) or (not input_lower and input_upper):
            return({"error": ["Enter both upper and lower bound"]})

        if input_lower:
            try:
                self.exact_ans = integrate(parse_expr(input_expression), (parse_expr(input_variable), input_lower, input_upper))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})

            try:
                if use_scientific:
                    self.approx_ans = self.to_scientific_notation(str(N(self.exact_ans, accuracy)), use_scientific)
                else:
                    self.approx_ans = str(simplify(N(self.exact_ans, accuracy)))
            except Exception:
                self.approx_ans = 0
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
            else:
                if use_scientific:
                    self.approx_ans = self.to_scientific_notation(str(N(self.exact_ans, accuracy)), use_scientific)
                else:
                    self.approx_ans = str(N(self.exact_ans, accuracy))
        else:
            try:
                self.exact_ans = integrate(parse_expr(input_expression), parse_expr(input_variable))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)
        return({"integ": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def prev_limit(self, input_expression, input_variable, input_approach, input_side, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        if not input_expression:
            return({"error": ["Enter an expression"]})
        if not input_approach:
            return ({"error": ["Enter value that the variable approaches"]})
        if not input_variable:
            return({"error": ["Enter a variable"]})

        try:
            self.exact_ans = Limit(parse_expr(input_expression), parse_expr(input_variable), input_approach, input_side)
        except Exception:
            return({"error": [f"Error: \n{traceback.format_exc()}"]})

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return({"limit": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def calc_limit(self, input_expression, input_variable, input_approach, input_side, output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not input_expression:
            return({"error": ["Enter an expression"]})
        if not input_approach:
            return ({"error": ["Enter value that the variable approaches"]})
        if not input_variable:
            return({"error": ["Enter a variable"]})

        try:
            self.exact_ans = limit(parse_expr(input_expression), parse_expr(input_variable), input_approach, input_side)
        except Exception:
            return({"error": [f"Error: \n{traceback.format_exc()}"]})

        if use_scientific:
            self.approx_ans = self.to_scientific_notation(str(N(self.exact_ans, accuracy)), use_scientific)
        else:
            self.approx_ans = str(N(self.exact_ans, accuracy))

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return({"limit": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def prev_eq(self, left_expression, right_expression, input_variable, outputText, output_type, use_unicode, line_wrap, cli=False):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""

        if not left_expression or not right_expression:
            return ({"error": ["Enter an expression both in left and right side"]})

        if not input_variable:
            return({"error": ["Enter a variable"]})

        if output_type == 1:
            """
            Since Pretty will be multiline, left and right side is broken up to not mess up equals symbol.
            Toggles between
            """
            if cli:
                eq_to_out = "Left side:\n\n"
                try:
                    eq_to_out += str(pretty(parse_expr(left_expression)))
                except Exception:
                    return ({"error": [f"Error: \n{traceback.format_exc()}"]})
                eq_to_out += "\n\nRight Side:\n\n"
                try:
                    eq_to_out += str(pretty(parse_expr(right_expression)))
                except Exception:
                    return ({"error": [f"Error: \n{traceback.format_exc()}"]})
                self.exact_ans = eq_to_out

            else:
                if outputText == "" or outputText[0:10] == "Right side":
                    eq_to_out = "Left side, click again for right side\n"
                    try:
                        eq_to_out += str(pretty(parse_expr(left_expression)))
                    except Exception:
                        return({"error": [f"Error: \n{traceback.format_exc()}"]})
                    self.exact_ans = eq_to_out
                else:
                    eq_to_out = "Right side, click again for left side\n"
                    try:
                        eq_to_out += str(pretty(parse_expr(right_expression)))
                    except Exception:
                        return({"error": [f"Error: \n{traceback.format_exc()}"]})
                    self.exact_ans = eq_to_out

        elif output_type == 2:
            try:
                self.exact_ans = str(latex(parse_expr(left_expression))) + " = " + str(latex(parse_expr(right_expression)))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
        else:
            self.exact_ans = str(left_expression) + " = " + str(right_expression)

        return({"eq": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def calc_eq(self, left_expression, right_expression, input_variable, solve_type, output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not left_expression or not right_expression:
            return ({"error": ["Enter an expression both in left and right side"]})

        if not input_variable:
            return ({"error": ["Enter a variable"]})

        if solve_type == 1: # 1: solveset, 2: solve
            try:
                self.exact_ans = solveset(Eq(parse_expr(left_expression), parse_expr(right_expression)), parse_expr(input_variable))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
            self.approx_ans = 0
        else:
            try:
                self.exact_ans = solve(Eq(parse_expr(left_expression), parse_expr(right_expression)), parse_expr(input_variable))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
            approx_list = [N(i, accuracy) for i in self.exact_ans]
            if use_scientific:
                approx_list = [self.to_scientific_notation(str(i), use_scientific) for i in approx_list]

            self.approx_ans = approx_list[0] if len(approx_list) == 1 else approx_list

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return({"eq": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def prev_simp_eq(self, expression, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""

        if not expression:
            return({"error": ["Enter an expression"]})

        if output_type == 1:
            try:
                self.exact_ans = str(pretty(parse_expr(expression, evaluate=False)))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
        elif output_type == 2:
            try:
                self.exact_ans = str(latex(parse_expr(expression, evaluate=False)))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
        else:
            self.exact_ans = str(expression)

        return({"simp": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def simp_eq(self, expression, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""

        if not expression:
            return({"error": ["Enter an expression"]})

        try:
            self.exact_ans = simplify(expression)
        except Exception:
            return({"error": [f"Error: \n{traceback.format_exc()}"]})

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return({"simp": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def prev_exp_eq(self, expression, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""

        if not expression:
            return({"error": ["Enter an expression"]})

        if output_type == 1:
            try:
                self.exact_ans = str(pretty(parse_expr(expression, evaluate=False)))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
        elif output_type == 2:
            try:
                self.exact_ans = str(latex(parse_expr(expression, evaluate=False)))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
        else:
            self.exact_ans = str(expression)

        return({"exp": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def exp_eq(self, expression, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""

        if not expression:
            return({"error": ["Enter an expressiobn"]})

        try:
            self.exact_ans = expand(expression)
        except Exception:
            return({"error": [f"Error: \n{traceback.format_exc()}"]})

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return({"exp": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def prev_eval_exp(self, expression, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""

        if not expression:
            return({"error": ["Enter an expression"]})

        if output_type == 1:
            try:
                self.exact_ans = str(pretty(parse_expr(expression, evaluate=False)))
            except Exception:

                return({"error": [f"Error: \n{traceback.format_exc()}"]})
        elif output_type == 2:
            try:
                self.exact_ans = str(latex(parse_expr(expression, evaluate=False)))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
        else:
            self.exact_ans = str(expression)

        return({"eval": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def eval_exp(self, expression, output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not expression:
            return({"error": ["Enter an expression"]})

        try:
            self.exact_ans = simplify(parse_expr(expression))
            if use_scientific:
                self.approx_ans = self.to_scientific_notation(str(N(self.exact_ans, accuracy)), use_scientific)
            else:
                self.approx_ans = str(N(self.exact_ans, accuracy))
        except Exception:
            return({"error": [f"Error: \n{traceback.format_exc()}"]})

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return({"eval": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def calc_pf(self, input_number):
        self.approx_ans = ""

        try:
            input_number = int(input_number)
        except:
            return({"error": [f"Error: {input_number} is not an integer."]})

        if input_number < 1:
            return ({"error": [f"Error: {input_number} is lower than 1, only number 1 and above is accepted."]})

        try:
            self.exact_ans = factorint(input_number)
        except Exception:
            return({"error": [f"Error: \n{traceback.format_exc()}"]})

        for base in self.exact_ans:
            self.approx_ans += f"({base}**{self.exact_ans[base]})*"

        return({"pf": [self.exact_ans, self.approx_ans[0:-1]]})

    @pyqtSlot()
    def clear_shell(self):
        self.previous_code_list = []
        self.signals.finished.emit()

    @pyqtSlot()
    def execute_code(self, new_code):
        self.approx_ans = 0
        self.output_code = ""
        if new_code:
            if new_code[0] == "\n":
                new_code = new_code[1:]
            if new_code[0:4] == ">>> ":
                new_code = new_code[4:]
        new_code = new_code.replace("... ", "")
        to_execute = ""
        for i in self.previous_code_list:
            to_execute += f"{i}\n"
        to_execute += new_code
        to_execute = to_execute.replace("\n\t", "|")
        for command in to_execute.split("\n"):
            new_to_exec = command.replace("|", "\n\t")
            try:
                exec(f"print({new_to_exec})")
            except:
                try:
                    exec(new_to_exec)
                except Exception:
                    self.output_code += f"\nError: {traceback.format_exc()}"
                    return({"exec": [self.output_code, 0]})
                else:
                    if new_to_exec not in self.previous_code_list:
                        self.previous_code_list.append(new_to_exec)
            else:
                self.output_code += "\n"
                exec(f"self.output_code += str({new_to_exec})")
                exec(f"self.exact_ans = str({new_to_exec})")

        return({"exec": [self.output_code, 0]})

    @pyqtSlot()
    def formula_get_info(self, text, data):
        for branch in data:
            for sub_branch in branch[1]:
                for formula in sub_branch[1]:
                    if formula[0] == text:
                        return({"formula_info", [formula[1]]})

    @pyqtSlot()
    def prev_formula(self, lines, value_string, output_text, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        empty_var_list, var_list, values = [], [], []

        for line in lines:
            if line[0].text() == "":
                empty_var_list.append(line[1])
            elif line[0].text() == "var":
                var_list.append(line[1])
            else:
                values.append([line[0].text(), line[1]])

        if len(empty_var_list) > 1 and len(var_list) != 1:
            return({"error": ["Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"]})

        if len(var_list) == 1:
            final_var = var_list[0]
        else:
            final_var = empty_var_list[0]

        left_side = value_string[0]
        right_side = value_string[1]

        self.exact_ans = solve(Eq(parse_expr(left_side, _clash1), parse_expr(right_side, _clash1)),parse_expr(final_var, _clash1))
        self.approx_ans = 0

        if output_type == 1:
            if output_text == "" or output_text[0:10] == "Right side":
                self.exact_ans = "Left side, click again for right side\n" + str(pretty(parse_expr(final_var, _clash1)))
            else:
                self.exact_ans = "Right side, click again for left side\n" + str(pretty(self.exact_ans))
        elif output_type == 2:
            try:
                self.exact_ans = str(latex(parse_expr(final_var, _clash1))) + " = " + str(latex(parse_expr(self.exact_ans)))
            except TypeError as e:
                return({"error": [f"Error: \n{e}\nUnable to preview formulas with multiple answers"]})
        else:
            self.exact_ans = str(final_var) + " = " + str(self.exact_ans)

        return({"formula": [self.exact_ans, self.approx_ans]})

    @pyqtSlot()
    def calc_formula(self, lines, value_string, solve_type, output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        empty_var_list, var_list, values = [], [], []
        self.exact_ans = ""
        self.approx_ans = 0
        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        for line in lines:
            if line[0].text() == "":
                empty_var_list.append(line[1])
            elif line[0].text() == "var":
                var_list.append(line[1])
            else:
                values.append([line[0].text(), line[1]])

        if len(empty_var_list) > 1 and len(var_list) != 1:
            return({"error": ["Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"]})

        if len(var_list) == 1:
            final_var = var_list[0]
        else:
            final_var = empty_var_list[0]

        left_side = parse_expr(value_string[0])
        right_side = parse_expr(value_string[1])

        for i in values:
            left_side = left_side.subs(parse_expr(i[1]), i[0])
            right_side = right_side.subs(parse_expr(i[1]), i[0])

        left_side = str(left_side).replace("_i", "(sqrt(-1))")
        right_side = str(right_side).replace("_i", "(sqrt(-1))")

        if solve_type == 2:
            try:
                self.exact_ans = solve(Eq(parse_expr(left_side, _clash1), parse_expr(right_side, _clash1)), parse_expr(final_var, _clash1))
            except:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})

            self.approx_ans = list(map(lambda x: N(x, accuracy), self.exact_ans))
            if len(self.approx_ans) == 1:
                self.approx_ans = self.approx_ans[0]

            if use_scientific:
                if type(self.approx_ans) == 'list':
                    self.approx_ans = list(map(lambda x: self.to_scientific_notation(str(x), use_scientific), self.approx_ans))
                else:
                    self.approx_ans = self.to_scientific_notation(str(self.approx_ans), use_scientific)

        else:
            try:
                self.exact_ans = solveset(Eq(parse_expr(left_side, _clash1), parse_expr(right_side, _clash1)), parse_expr(final_var, _clash1))
            except:
                return ({"error": [f"Error: \n{traceback.format_exc()}"]})

            self.approx_ans = 0

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return({"formula": [self.exact_ans, self.approx_ans]})