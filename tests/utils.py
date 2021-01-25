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

# Third library
import sympy as sy


def is_traceback(blocker):
    """Checks if the worker caught the exception"""
    return blocker.args[0]["error"][0].startswith("Error: \nTraceback (most recent call last):")


def to_scientific_notation(number: str, accuracy: int = 5) -> str:
    sym_num = sy.sympify(number)

    if not sym_num.is_complex:
        return number

    if type(accuracy) != int:
        print("Accuracy must be an integer over 1, defaulting to 5")
        accuracy = 5

    if accuracy < 1:
        print("Accuracy must be an integer over 1, defaulting to 5")
        accuracy = 5

    if sym_num.is_real:
        return f"{sym_num:.{accuracy}E}".replace("E", "*10**")
    else:
        real = sy.re(sym_num)
        imag = sy.im(sym_num)

        real = to_scientific_notation(real, accuracy)
        imag = to_scientific_notation(imag, accuracy)

        output = real
        if sy.sympify(imag) < 0:
            output += f"-{imag[1:]}*I"
        else:
            output += f"+{imag}*I"
        return output
