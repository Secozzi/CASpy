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

# Standard library
import typing as ty
import traceback

# Third party
from pyperclip import copy
import sympy as sy

# PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QRunnable


def catch_thread(func: ty.Callable[..., ty.Any]) -> ty.Callable[..., ty.Any]:
    """Decorator to catch error, fails only if something goes wrong in the source code"""
    def wrapper(*args, **kwargs) -> ty.Any:
        try:
            return func(*args, **kwargs)
        except:
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

    @pyqtSlot()
    def run(self) -> ty.Union[ty.Dict[str, ty.List[str]], None]:
        try:
            result = getattr(self, self.command)(*self.params)
        except:
            return {
                "error": [
                    f"Error calling function from worker thread: \n{traceback.format_exc()}"
                ]
            }

        # Copy output, for CLI
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
            else:
                copy(str(output))

        self.signals.output.emit(result)
        self.signals.finished.emit()

    @pyqtSlot()
    def to_scientific_notation(self, number: str, accuracy: int = 5) -> str:
        number = str(number)
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
            return f"{number:.{accuracy}E}".replace("E", "*10**")
        else:
            real = sy.re(sym_num)
            imag = sy.im(sym_num)

            real = self.to_scientific_notation(real, accuracy)
            imag = self.to_scientific_notation(imag, accuracy)

            output = real
            if sy.sympify(imag) < 0:
                output += f"-{imag[1:]}*I"
            else:
                output += f"+{imag}*I"
            return output
