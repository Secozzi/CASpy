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

import traceback

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from pathlib import Path
import sys, os

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))
os.chdir(CURRENT_DIR)

from CAS import Ui_MainWindow
from qt_assets.main import CASpyGUI


class MainWindow(QMainWindow, CASpyGUI):
    def __init__(self, *args, **kwargs):
        """
        Setups and install eventFilters on QPlainTextEdit that user types expression into
        """
        super().__init__(*args, **kwargs)

        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setupUi(self)
        for i in [
            self.consoleIn,
            self.DerivExp,
            self.IntegExp,
            self.LimExp,
            self.EqLeft,
            self.EqRight,
            self.SimpExp,
            self.ExpExp,
            self.EvalExp,
            self.PfInput,
        ]:
            i.installEventFilter(self)

    def eventFilter(self, obj, event):
        """
        Creates list of modifires that were pressed on keypress. Setups eventFilters.

        Parameters
        --------------
        obj: object
            Object of QPlainTextEdit that user types into.
        event: QEvent
            QEvent.
        """
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append("shift")

        """
        Executs code when enter is pressed. Goes to new line and enters '... ' when shift+enter is pressed (doesn't execute code)
        """
        if obj is self.consoleIn and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.consoleIn.appendPlainText("... ")
                        return True
                else:
                    self.execute_code()
                    return True

        """
        Calculates when shift+enter is pressed.
        """
        if obj is self.DerivExp and event.type() == QEvent.KeyPress:
            if modifiers:
                if modifiers[0] == "shift":
                    if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                        self.calc_deriv()
                        return True

        if obj is self.IntegExp and event.type() == QEvent.KeyPress:
            if modifiers:
                if modifiers[0] == "shift":
                    if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                        self.calc_integ()
                        return True

        if obj is self.LimExp and event.type() == QEvent.KeyPress:
            if modifiers:
                if modifiers[0] == "shift":
                    if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                        self.calc_limit()
                        return True

        if (obj is self.EqLeft and event.type() == QEvent.KeyPress) or (
            obj is self.EqRight and event.type() == QEvent.KeyPress
        ):
            if modifiers:
                if modifiers[0] == "shift":
                    if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                        self.calc_eq()
                        return True

        if obj is self.SimpExp and event.type() == QEvent.KeyPress:
            if modifiers:
                if modifiers[0] == "shift":
                    if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                        self.simp_eq()
                        return True

        if obj is self.ExpExp and event.type() == QEvent.KeyPress:
            if modifiers:
                if modifiers[0] == "shift":
                    if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                        self.exp_eq()
                        return True

        if obj is self.EvalExp and event.type() == QEvent.KeyPress:
            if modifiers:
                if modifiers[0] == "shift":
                    if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                        self.eval_exp()
                        return True

        if obj is self.PfInput and event.type() == QEvent.KeyPress:
            if modifiers:
                if modifiers[0] == "shift":
                    if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                        self.calc_pf()
                        return True

        return super(MainWindow, self).eventFilter(obj, event)


def main():
    """
    Runs program. Catches errors and prints them to console.
    """
    import sys

    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)
        QApplication.quit()

    sys.excepthook = excepthook
    e = CASpyGUI()
    app = QApplication(sys.argv)
    cas = MainWindow()
    cas.start_thread()
    cas.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
