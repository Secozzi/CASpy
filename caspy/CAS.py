# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))
os.chdir(CURRENT_DIR)

from Worker import CASWorker

from PyQt5.QtCore import (
    QCoreApplication,
    QMetaObject,
    QRect,
    QRegExp,
    QSize,
    Qt,
    QThreadPool,
    QUrl
)

from PyQt5.QtGui import (
    QCursor,
    QFont,
    QRegExpValidator,
    QTextCursor
)

from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QButtonGroup,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSpinBox,
    QStatusBar,
    QTabWidget,
    QTextBrowser,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget
)

from PyQt5.QtWebEngineWidgets import QWebEngineView

from pyperclip import copy
from sympy import Symbol
from sympy.abc import _clash1
from sympy.parsing.sympy_parser import parse_expr


class Ui_MainWindow(object):
    def __init__(self, *args, **kwargs):
        """
        Main Ui window. This class contains everything that is displayed.
        The function create_code_list is called on the Worker, this is because it is only needed to be called once.
        Variables used in program and how to print is initialzed
        """
        super(Ui_MainWindow, self).__init__(*args, **kwargs)
        CASWorker.create_code_list(CASWorker)

        self.exact_ans = ""
        self.approx_ans = 0

        self.use_unicode = False
        self.line_wrap = False
        self.use_scientific = False
        self.accuracy = 10

    def stop_thread(self):
        """
        Stop thread
        """
        pass

    def start_thread(self):
        """
        Start thread
        """
        self.threadpool = QThreadPool()

    def update_ui(self, inputDict):
        """
        Updates Ui with results returned from the worker thread

        :param inputDict: Dict
            The key stores what operation was called to tell what part of the Ui to update.
            The value is a list containing self.exact_ans and self.ApproxAns from the calculation. If an error is returned the value is a list containing only the error message.
        """

        first_key = list(inputDict.keys())[0]
        if first_key == "error":
            self.show_error_box(inputDict[first_key][0])
        else:
            self.exact_ans = str(inputDict[first_key][0])
            self.approx_ans = inputDict[first_key][1]

            if first_key == "deriv":
                self.DerivOut.setText(self.exact_ans)
                self.DerivApprox.setText(str(self.approx_ans))
            elif first_key == "integ":
                self.IntegOut.setText(self.exact_ans)
                self.IntegApprox.setText(str(self.approx_ans))
            elif first_key == "limit":
                self.LimOut.setText(self.exact_ans)
                self.LimApprox.setText(str(self.approx_ans))
            elif first_key == "eq":
                self.EqOut.setText(self.exact_ans)
                self.EqApprox.setText(str(self.approx_ans))
            elif first_key == "simp":
                self.SimpOut.setText(self.exact_ans)
            elif first_key == "exp":
                self.ExpOut.setText(self.exact_ans)
            elif first_key == "eval":
                self.EvalOut.setText(self.exact_ans)
                self.EvalApprox.setText(str(self.approx_ans))
            elif first_key == "pf":
                self.PfOut.setText(self.exact_ans)
            elif first_key == "formula":
                self.FormulaExact.setText(self.exact_ans)
                self.FormulaApprox.setText(str(self.approx_ans))
            elif first_key == "exec":
                self.consoleIn.insertPlainText(self.exact_ans + "\n>>> ")
                self.consoleIn.moveCursor(QTextCursor.End)
                self.current_code = self.consoleIn.toPlainText()

    def raise_error(self):
        # Used to debug
        assert False

    def show_error_box(self, message):
        """
        Show a message box containing an error

        :param message: str
            The message that is to be displayed by the message box
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def get_scientific_notation(self):
        number, confirmed = QInputDialog.getInt(self, "Get Scientific Notation", "Enter the accuracy for scientific notation", 5, 1, 999999, 1)
        if confirmed:
            self.use_scientific = number

    def get_accuracy(self):
        number, confirmed = QInputDialog.getInt(self, "Get Accuracy", "Enter the accuracy for evaluation", self.accuracy, 1, 999999, 1)
        if confirmed:
            self.accuracy = number

    def copy_exact_ans(self):
        # Copies self.exact_ans to clipboard.
        if type(self.exact_ans) == list:
            if len(self.exact_ans) == 1:
                copy(str(self.exact_ans[0]))
        else:
            copy(str(self.exact_ans))

    def copy_approx_ans(self):
        # Copies self.approx_ans to clipboard.
        if type(self.approx_ans) == list:
            if len(self.approx_ans) == 1:
                copy(str(self.approx_ans[0]))
        else:
            copy(str(self.approx_ans))

    def clear_shell(self):
        # Clears shell of written text, and previously initialized variables and functions.
        self.alreadyExecuted = []
        code = "This is a very simple shell using 'exec' commands, so it has some limitations.\n" \
                           "Every variable declared and function defined will be saved until the program is closed" \
                           " or when the 'clear commands' button in the menubar is pressed.\n" \
                           "It will automatically output to the shell, but it can't use 'print' commands. To copy" \
                           " output, press the 'copy exact answer' in the menubar\nTheses commands were executed:\n" \
                           "from __future__ import division\n" \
                           "from sympy import *\n" \
                           "from sympy.parsing.sympy_parser import parse_expr\n" \
                           "from sympy.abc import _clash1\nimport math as m\nx, y, z, t = symbols('x y z t')\n" \
                           "k, m, n = symbols('k m n', integer=True)\nf, g, h = symbols('f g h', cls=Function)\n\n>>> "
        self.consoleIn.clear()
        self.consoleIn.appendPlainText(code)
        self.WorkerCAS.clear_shell()

    def toggle_unicode(self, state):
        # Toggles whether or not to use unicode.
        if state:
            self.use_unicode = True
        else:
            self.use_unicode = False

    def toggle_line_wrap(self, state):
        # Toggles whether or not to wrap lines.
        if state:
            self.line_wrap = True
        else:
            self.line_wrap = False

    def toggle_use_scientific(self, state):
        # Toggles scientific notation, only works when calculating an approximation
        _translate = QCoreApplication.translate
        if state:
            self.get_scientific_notation()
            self.actionScientific.setText(_translate("MainWindow", f"Scientific Notation - {self.use_scientific}"))
        else:
            self.use_scientific = False
            self.actionScientific.setText(_translate("MainWindow", "Scientific Notation"))

    def change_accuracy(self, state):
        _translate = QCoreApplication.translate
        if state:
            self.get_accuracy()
            self.actionAccuracy.setText(_translate("MainWindow", f"Accuracy - {self.accuracy}"))
        else:
            self.actionAccuracy.setText(_translate("MainWindow", "Accuracy"))

    def next_tab(self):
        # Goes to next tab.
        if self.tabWidget.currentIndex() == 10:
            self.tabWidget.setCurrentIndex(0)
        else:
            self.tabWidget.setCurrentIndex(self.tabWidget.currentIndex() + 1)

    def previous_tab(self):
        # Goes to previous tab.
        if self.tabWidget.currentIndex() == 0:
            self.tabWidget.setCurrentIndex(10)
        else:
            self.tabWidget.setCurrentIndex(self.tabWidget.currentIndex() - 1)

    def prev_deriv(self):
        """
        Function to call the worker thread to preview the expression as a derivative.
        It checks what output type is selected.
        """
        if self.DerivPP.isChecked():
            output_type = 1
        elif self.DerivLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_deriv", [
            self.DerivExp.toPlainText(),
            self.DerivVar.text(),
            self.DerivOrder.value(),
            self.DerivPoint.text(),
            output_type,
            self.use_unicode,
            self.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def calc_deriv(self):
        """
        Function to call the worker thread to calculate the expression as a derivative.
        It checks what output type is selected.
        """
        if self.DerivPP.isChecked():
            output_type = 1
        elif self.DerivLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("calc_deriv", [
            self.DerivExp.toPlainText(),
            self.DerivVar.text(),
            self.DerivOrder.value(),
            self.DerivPoint.text(),
            output_type,
            self.use_unicode,
            self.line_wrap,
            self.use_scientific,
            self.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def prev_integ(self):
        """
        Function to call the worker thread to preview the expression as an integral.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """

        if self.IntegPP.isChecked():
            output_type = 1
        elif self.IntegLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_integ", [
            self.IntegExp.toPlainText(),
            self.IntegVar.text(),
            self.IntegLower.text(),
            self.IntegUpper.text(),
            output_type,
            self.use_unicode,
            self.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def calc_integ(self):
        """
        Function to call the worker thread to calculate the expression as an integral.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """
        if self.IntegPP.isChecked():
            output_type = 1
        elif self.IntegLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("calc_integ", [
            self.IntegExp.toPlainText(),
            self.IntegVar.text(),
            self.IntegLower.text(),
            self.IntegUpper.text(),
            output_type,
            self.use_unicode,
            self.line_wrap,
            self.use_scientific,
            self.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def prev_limit(self):
        """
        Function to call the worker thread to preview the expression as a limit.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """

        if self.LimPP.isChecked():
            output_type = 1
        elif self.LimLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        if self.LimSide.currentIndex() == 0:
            limit_side = "+-"
        elif self.LimSide.currentIndex() == 1:
            limit_side = "-"
        else:
            limit_side = "+"

        self.WorkerCAS = CASWorker("prev_limit", [
            self.LimExp.toPlainText(),
            self.LimVar.text(),
            self.LimApproach.text(),
            limit_side,
            output_type,
            self.use_unicode,
            self.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def calc_limit(self):
        """
        Function to call the worker thread to calculate the expression as a limit.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """

        if self.LimPP.isChecked():
            output_type = 1
        elif self.LimLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        if self.LimSide.currentIndex() == 0:
            limit_side = "+-"
        elif self.LimSide.currentIndex() == 1:
            limit_side = "-"
        else:
            limit_side = "+"

        self.WorkerCAS = CASWorker("calc_limit", [
            self.LimExp.toPlainText(),
            self.LimVar.text(),
            self.LimApproach.text(),
            limit_side,
            output_type,
            self.use_unicode,
            self.line_wrap,
            self.use_scientific,
            self.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def prev_eq(self):
        """
        Function to call the worker thread to preview the expressions as an equation.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """

        if self.EqPP.isChecked():
            output_type = 1
        elif self.EqLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_eq", [
            self.EqLeft.toPlainText(),
            self.EqRight.toPlainText(),
            self.EqVar.text(),
            self.EqOut.toPlainText(),
            output_type,
            self.use_unicode,
            self.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def calc_eq(self):
        """
        Function to call the worker thread to calculate the expressions as an equation.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """

        if self.EqPP.isChecked():
            output_type = 1
        elif self.EqLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        if self.EqSolve.isChecked():
            solve_type = 2
        if self.EqSolveSet.isChecked():
            solve_type = 1

        self.WorkerCAS = CASWorker("calc_eq", [
            self.EqLeft.toPlainText(),
            self.EqRight.toPlainText(),
            self.EqVar.text(),
            solve_type,
            output_type,
            self.use_unicode,
            self.line_wrap,
            self.use_scientific,
            self.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def prev_simp_eq(self):
        """
        Function to call the worker thread to preview the expression.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """

        if self.SimpPP.isChecked():
            output_type = 1
        elif self.SimpLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_simp_eq", [
            self.SimpExp.toPlainText(),
            output_type,
            self.use_unicode,
            self.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def simp_eq(self):
        """
        Function to call the worker thread to simplify the expression.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """

        if self.SimpPP.isChecked():
            output_type = 1
        elif self.SimpLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("simp_eq", [
            self.SimpExp.toPlainText(),
            output_type,
            self.use_unicode,
            self.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def prev_exp_eq(self):
        """
        Function to call the worker thread to preview the expression.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """

        if self.ExpPP.isChecked():
            output_type = 1
        elif self.ExpLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_exp_eq", [
            self.ExpExp.toPlainText(),
            output_type,
            self.use_unicode,
            self.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def exp_eq(self):
        """
        Function to call the worker thread to expand the expression.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """

        if self.ExpPP.isChecked():
            output_type = 1
        elif self.ExpLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("exp_eq", [
            self.ExpExp.toPlainText(),
            output_type,
            self.use_unicode,
            self.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def prev_eval_exp(self):
        """
        Function to call the worker thread to preview the expression.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """

        if self.EvalPP.isChecked():
            output_type = 1
        elif self.EvalLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("prev_eval_exp", [
            self.EvalExp.toPlainText(),
            output_type,
            self.use_unicode,
            self.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def eval_exp(self):
        """
        Function to call the worker thread to evaluate the expression.
        Checks for invalid expressions and variables then convert expression to selected output type.
        """

        if self.EvalPP.isChecked():
            output_type = 1
        elif self.EvalLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        self.WorkerCAS = CASWorker("eval_exp", [
            self.EvalExp.toPlainText(),
            output_type,
            self.use_unicode,
            self.line_wrap,
            self.use_scientific,
            self.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def calc_pf(self):
        """
        Function to call the worker thread to prime factorize the selected number.
        Checks for invalid expressions and variables then convert expression to selected output type.
        Output is a dict containing the key as the base and the value as the exponent.
        """

        self.WorkerCAS = CASWorker("calc_pf", [self.PfInput.value()])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def FormulaTreeSelected(self):
        """
        Retrieves formula and information about formula that user double clicked.
        Splits equation into left side of equals symbol and right side.
        Uses _i as imaginary unit instead of I and removes other similar functions so they can be used as variables in formula.
        """
        getSelected = self.FormulaTree.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            self.selectedTreeItem = baseNode.text(0)
            if "=" in self.selectedTreeItem:
                expr = self.selectedTreeItem.split("=")
                expr = list(map(lambda x: x.replace("_i", "(sqrt(-1))"), expr))
                self.FormulaSymbolsList = [str(i) for i in list(parse_expr(expr[0], _clash1).atoms(Symbol))]
                self.FormulaSymbolsList.extend((str(i) for i in list(parse_expr(expr[1], _clash1).atoms(Symbol))))
                self.FormulaSymbolsList = list(set(self.FormulaSymbolsList))
                self.FormulaSymbolsList.sort()
                self.FormulaUpdateVars()
                self.FormulaInfo = self.FormulaGetInfo(self.selectedTreeItem, self.FormulaTreeData)
                self.FormulaSetInfoText()

    def FormulaSetInfoText(self):
        """
        Sets StatusTip and TootTip to the info given by the json file
        """
        _translate = QCoreApplication.translate
        lines = [[self.FormulaScrollArea.findChild(QLineEdit, str(i) + "line"), i] for i in self.FormulaLabelNames]
        for line in lines:
            for i in self.FormulaInfo:
                FormulaInfoList = self.FormulaInfoDict[i].split("|")
                if FormulaInfoList[0] == line[1]:
                    line[0].setStatusTip(_translate("MainWindow", f"{FormulaInfoList[1]}, mäts i {FormulaInfoList[2]}"))
                    line[0].setToolTip(_translate("MainWindow", FormulaInfoList[1]))
                elif FormulaInfoList[0].split(";")[0] == line[1]:
                    line[0].setStatusTip(_translate("MainWindow", f"{FormulaInfoList[1]}, mäts i {FormulaInfoList[2]}"))
                    line[0].setToolTip(_translate("MainWindow", FormulaInfoList[1]))
                    line[0].setText(FormulaInfoList[0].split(";")[1])

    def FormulaUpdateVars(self):
        """
        Initalizes QLineEdits and QLabels based on the vars that is in the selected formula
        """
        for i in reversed(range(self.FormulaGrid2.count())):
            self.FormulaGrid2.itemAt(i).widget().setParent(None)
        self.FormulaLabelNames = self.FormulaSymbolsList
        self.FormulaLabelPos = [[i, 0] for i in range(len(self.FormulaLabelNames))]
        self.FormulaLinePos = [[i, 1] for i in range(len(self.FormulaLabelNames))]
        for self.FormulaNameLabel, FormulaPosLabel, FormulaPosLine in zip(self.FormulaLabelNames, self.FormulaLabelPos, self.FormulaLinePos):
            self.FormulaLabel = QLabel(self.FormulaScrollArea)
            self.FormulaLabel.setText(self.FormulaNameLabel)
            self.FormulaGrid2.addWidget(self.FormulaLabel, *FormulaPosLabel)
            self.FormulaQLine = QLineEdit(self.FormulaScrollArea)
            self.FormulaQLine.setObjectName(self.FormulaNameLabel + "line")
            self.FormulaGrid2.addWidget(self.FormulaQLine, *FormulaPosLine)

    def FormulaGetInfo(self, text, data):
        """
        Retrieves info that's correlated with given formula

        Parameters
        -------------
        text: string
            Formula whose information is requested.
        data: JSON file
            Data that stores formulas and respective information.

        Returns
        ------------
        formula[1]: string
            Information correlated to formula.
        """
        for branch in data:
            for subBranch in branch[1]:
                for formula in subBranch[1]:
                    if formula[0] == text:
                        return formula[1]

    def prev_formula(self):
        """
        Previews formula based on what variable to solve for. Checks for variable either if it's the only one without a values entered or 'var' as values.
        """

        if self.FormulaPP.isChecked():
            outputType = 1
        elif self.FormulaLatex.isChecked():
            outputType = 2
        else:
            outputType = 3

        try:
            lines = [[self.FormulaScrollArea.findChild(QLineEdit, str(i) + "line"), i] for i in self.FormulaLabelNames]
        except:
            self.show_error_box("Error: select a formula")

        values_string = self.selectedTreeItem.split("=")


        self.WorkerCAS = CASWorker("prev_formula", [lines, values_string, self.FormulaExact.toPlainText(), outputType, self.use_unicode, self.line_wrap])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def calc_formula(self):
        """
        Calculates formula based on what variable to solve for and entered values. Checks for variable either if it's the only one without a values inputted or 'var' as values.
        """
        if self.FormulaPP.isChecked():
            output_type = 1
        elif self.FormulaLatex.isChecked():
            output_type = 2
        else:
            output_type = 3

        if self.FormulaSolveSolve.isChecked():
            solve_type = 2
        if self.FormulaSolveSolveSet.isChecked():
            solve_type = 1

        try:
            lines = [[self.FormulaScrollArea.findChild(QLineEdit, str(i) + "line"), i] for i in self.FormulaLabelNames]
        except:
            self.show_error_box("Error: select a formula")

        values_string = self.selectedTreeItem.split("=")

        self.WorkerCAS = CASWorker("calc_formula", [
            lines,
            values_string,
            solve_type,
            output_type,
            self.use_unicode,
            self.line_wrap,
            self.use_scientific,
            self.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def execute_code(self):
        """
        Retrieves command(s) entered by user, seperates them from already existing code and '>>> ' and '... '. Creates a list of previously executed commands and executes all of them so user can reference them after they've been initalized.
        """

        self.new_code = self.consoleIn.toPlainText().replace(self.current_code, "")
        self.consoleIn.moveCursor(QTextCursor.End)

        self.WorkerCAS = CASWorker("execute_code", [self.new_code])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.threadpool.start(self.WorkerCAS)

    def updateWeb(self, action):
        """
        Updates web tab when user selects new website.

        Parameters
        ---------------
        action: QAction
            action.text() shows text of selected radiobutton
        """
        self.exact_ans = 0
        self.approx_ans = 0
        for i in self.WebList:
            for key in i:
                if action.text() == key:
                    self.web.load(QUrl(i[key]))

    def setupUi(self, MainWindow):
        """
        Setups UI, (mostly) generated by QtDesigner.
        Setups different things such as data, shell and regular expressions for variables.
        """

        """
        Reads json file and stores data into respective variables.
        FormulaTreeData[0]: Dictionary
            Stores all the information correlated to each symbol
        FormulaTreeData[1]: List
            Stores all formulae and their respective information
        FormulaTreeData[2]: Dictionary
            Stores websites and html files information
        """

        with open("assets/formulas.json", "r", encoding="utf8") as json_f:
            self.json_data = json_f.read()
            self.json_file = json.loads(self.json_data)

        lowerReg = QRegExp("[a-z]+")
        lowerVal = QRegExpValidator(lowerReg)
        textReg = QRegExp("[A-Za-z]+")
        textVal = QRegExpValidator(textReg)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1278, 806)
        MainWindow.setMinimumSize(QSize(400, 350))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setFont(QFont("Courier New"))
        MainWindow.setCursor(QCursor(Qt.ArrowCursor))

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QSize(400, 25))
        self.tabWidget.setMaximumSize(QSize(16777215, 16777215))
        self.tabWidget.setObjectName("tabWidget")

        self.Deriv = QWidget()
        self.Deriv.setObjectName("Deriv")
        self.gridLayout_2 = QGridLayout(self.Deriv)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.DerivPrev = QPushButton(self.Deriv)
        self.DerivPrev.setObjectName("DerivPrev")
        self.DerivPrev.clicked.connect(self.prev_deriv)
        self.gridLayout_2.addWidget(self.DerivPrev, 6, 0, 1, 2)
        self.DerivCalc = QPushButton(self.Deriv)
        self.DerivCalc.setObjectName("DerivCalc")
        self.DerivCalc.clicked.connect(self.calc_deriv)
        self.gridLayout_2.addWidget(self.DerivCalc, 7, 0, 1, 2)
        self.label_9 = QLabel(self.Deriv)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 4, 0, 1, 1)
        self.DerivExp = QTextEdit(self.Deriv)
        self.DerivExp.setMaximumSize(QSize(16777215, 16777215))
        self.DerivExp.setLineWrapMode(QTextEdit.NoWrap)
        self.DerivExp.setObjectName("DerivExp")
        self.gridLayout_2.addWidget(self.DerivExp, 0, 0, 3, 2)
        self.label = QLabel(self.Deriv)
        self.label.setMaximumSize(QSize(40, 16777215))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.DerivOutType = QLabel(self.Deriv)
        self.DerivOutType.setObjectName("DerivOutType")
        self.horizontalLayout.addWidget(self.DerivOutType)
        self.DerivPP = QRadioButton(self.Deriv)
        self.DerivPP.setChecked(True)
        self.DerivPP.setObjectName("DerivPP")
        self.horizontalLayout.addWidget(self.DerivPP)
        self.DerivLatex = QRadioButton(self.Deriv)
        self.DerivLatex.setObjectName("DerivLatex")
        self.horizontalLayout.addWidget(self.DerivLatex)
        self.DerivNormal = QRadioButton(self.Deriv)
        self.DerivNormal.setObjectName("DerivNormal")
        self.horizontalLayout.addWidget(self.DerivNormal)
        self.gridLayout_2.addLayout(self.horizontalLayout, 8, 0, 1, 2)
        self.DerivOrder = QSpinBox(self.Deriv)
        self.DerivOrder.setMinimumSize(QSize(0, 25))
        self.DerivOrder.setMaximumSize(QSize(16777215, 25))
        self.DerivOrder.setMinimum(1)
        self.DerivOrder.setMaximum(999)
        self.DerivOrder.setObjectName("DerivOrder")
        self.gridLayout_2.addWidget(self.DerivOrder, 3, 1, 1, 1)
        self.DerivVar = QLineEdit(self.Deriv)
        self.DerivVar.setMinimumSize(QSize(0, 25))
        self.DerivVar.setMaximumSize(QSize(16777215, 25))
        self.DerivVar.setObjectName("DerivVar")
        self.DerivVar.setValidator(lowerVal)
        self.DerivVar.setText("x")
        self.gridLayout_2.addWidget(self.DerivVar, 5, 1, 1, 1)
        self.DerivPoint = QLineEdit(self.Deriv)
        self.DerivPoint.setMinimumSize(QSize(0, 25))
        self.DerivPoint.setMaximumSize(QSize(16777215, 25))
        self.DerivPoint.setPlaceholderText("")
        self.DerivPoint.setObjectName("DerivPoint")
        self.gridLayout_2.addWidget(self.DerivPoint, 4, 1, 1, 1)
        self.label_3 = QLabel(self.Deriv)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 5, 0, 1, 1)
        self.DerivOut = QTextBrowser(self.Deriv)
        self.DerivOut.setMaximumSize(QSize(16777215, 16777215))
        self.DerivOut.setLineWrapMode(QTextEdit.NoWrap)
        self.DerivOut.setObjectName("DerivOut")
        self.gridLayout_2.addWidget(self.DerivOut, 0, 3, 8, 1)
        self.DerivApprox = QLineEdit(self.Deriv)
        self.DerivApprox.setReadOnly(True)
        self.DerivApprox.setMinimumSize(QSize(0, 25))
        self.DerivApprox.setMaximumSize(QSize(16777215, 25))
        font = QFont()
        font.setPointSize(8)
        self.DerivApprox.setFont(font)
        self.DerivApprox.setObjectName("DerivApprox")
        self.gridLayout_2.addWidget(self.DerivApprox, 8, 3, 1, 1)
        self.tabWidget.addTab(self.Deriv, "")

        self.Integ = QWidget()
        self.Integ.setObjectName("Integ")
        self.gridLayout_3 = QGridLayout(self.Integ)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.IntegExp = QTextEdit(self.Integ)
        self.IntegExp.setMaximumSize(QSize(16777215, 16777215))
        self.IntegExp.setLineWrapMode(QTextEdit.NoWrap)
        self.IntegExp.setObjectName("IntegExp")
        self.gridLayout_3.addWidget(self.IntegExp, 0, 0, 1, 2)
        self.IntegOut = QTextBrowser(self.Integ)
        self.IntegOut.setMaximumSize(QSize(16777215, 16777215))
        self.IntegOut.setLineWrapMode(QTextEdit.NoWrap)
        self.IntegOut.setObjectName("IntegOut")
        self.gridLayout_3.addWidget(self.IntegOut, 0, 2, 6, 1)
        self.label_2 = QLabel(self.Integ)
        self.label_2.setMaximumSize(QSize(40, 16777215))
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.IntegLower = QLineEdit(self.Integ)
        self.IntegLower.setMinimumSize(QSize(0, 25))
        self.IntegLower.setMaximumSize(QSize(16777215, 25))
        self.IntegLower.setPlaceholderText("")
        self.IntegLower.setObjectName("IntegLower")
        self.gridLayout_3.addWidget(self.IntegLower, 1, 1, 1, 1)
        self.label_5 = QLabel(self.Integ)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)
        self.IntegUpper = QLineEdit(self.Integ)
        self.IntegUpper.setMinimumSize(QSize(0, 25))
        self.IntegUpper.setMaximumSize(QSize(16777215, 25))
        self.IntegUpper.setObjectName("IntegUpper")
        self.gridLayout_3.addWidget(self.IntegUpper, 2, 1, 1, 1)
        self.label_4 = QLabel(self.Integ)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 3, 0, 1, 1)
        self.IntegVar = QLineEdit(self.Integ)
        self.IntegVar.setMinimumSize(QSize(0, 25))
        self.IntegVar.setMaximumSize(QSize(16777215, 25))
        self.IntegVar.setObjectName("IntegVar")
        self.IntegVar.setValidator(lowerVal)
        self.IntegVar.setText("x")
        self.gridLayout_3.addWidget(self.IntegVar, 3, 1, 1, 1)
        self.IntegPrev = QPushButton(self.Integ)
        self.IntegPrev.setObjectName("IntegPrev")
        self.IntegPrev.clicked.connect(self.prev_integ)
        self.gridLayout_3.addWidget(self.IntegPrev, 4, 0, 1, 2)
        self.IntegCalc = QPushButton(self.Integ)
        self.IntegCalc.setObjectName("IntegCalc")
        self.IntegCalc.clicked.connect(self.calc_integ)
        self.gridLayout_3.addWidget(self.IntegCalc, 5, 0, 1, 2)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.IntegOutType = QLabel(self.Integ)
        self.IntegOutType.setObjectName("IntegOutType")
        self.horizontalLayout_2.addWidget(self.IntegOutType)
        self.IntegPP = QRadioButton(self.Integ)
        self.IntegPP.setChecked(True)
        self.IntegPP.setObjectName("IntegPP")
        self.horizontalLayout_2.addWidget(self.IntegPP)
        self.IntegLatex = QRadioButton(self.Integ)
        self.IntegLatex.setObjectName("IntegLatex")
        self.horizontalLayout_2.addWidget(self.IntegLatex)
        self.IntegNormal = QRadioButton(self.Integ)
        self.IntegNormal.setObjectName("IntegNormal")
        self.horizontalLayout_2.addWidget(self.IntegNormal)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 6, 0, 1, 2)
        self.IntegApprox = QLineEdit(self.Integ)
        self.IntegApprox.setReadOnly(True)
        self.IntegApprox.setMinimumSize(QSize(0, 25))
        self.IntegApprox.setMaximumSize(QSize(16777215, 25))
        self.IntegApprox.setObjectName("IntegApprox")
        self.gridLayout_3.addWidget(self.IntegApprox, 6, 2, 1, 1)
        self.tabWidget.addTab(self.Integ, "")

        self.Lim = QWidget()
        self.Lim.setObjectName("Lim")
        self.gridLayout_4 = QGridLayout(self.Lim)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.LimExp = QTextEdit(self.Lim)
        self.LimExp.setMaximumSize(QSize(16777215, 16777215))
        self.LimExp.setLineWrapMode(QTextEdit.NoWrap)
        self.LimExp.setObjectName("LimExp")
        self.gridLayout_4.addWidget(self.LimExp, 0, 0, 1, 2)
        self.LimOut = QTextBrowser(self.Lim)
        self.LimOut.setMaximumSize(QSize(16777215, 16777215))
        self.LimOut.setLineWrapMode(QTextEdit.NoWrap)
        self.LimOut.setObjectName("LimOut")
        self.gridLayout_4.addWidget(self.LimOut, 0, 2, 6, 1)
        self.label_6 = QLabel(self.Lim)
        self.label_6.setMaximumSize(QSize(40, 16777215))
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 1, 0, 1, 1)
        self.LimSide = QComboBox(self.Lim)
        self.LimSide.setMinimumSize(QSize(0, 25))
        self.LimSide.setMaximumSize(QSize(16777215, 25))
        self.LimSide.setEditable(False)
        self.LimSide.setObjectName("LimSide")
        self.LimSide.addItem("")
        self.LimSide.addItem("")
        self.LimSide.addItem("")
        self.gridLayout_4.addWidget(self.LimSide, 1, 1, 1, 1)
        self.label_7 = QLabel(self.Lim)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 2, 0, 1, 1)
        self.LimVar = QLineEdit(self.Lim)
        self.LimVar.setMinimumSize(QSize(0, 25))
        self.LimVar.setMaximumSize(QSize(16777215, 25))
        self.LimVar.setObjectName("LimVar")
        self.LimVar.setText("x")
        self.LimVar.setValidator(lowerVal)
        self.gridLayout_4.addWidget(self.LimVar, 2, 1, 1, 1)
        self.label_8 = QLabel(self.Lim)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 3, 0, 1, 1)
        self.LimApproach = QLineEdit(self.Lim)
        self.LimApproach.setMinimumSize(QSize(0, 25))
        self.LimApproach.setMaximumSize(QSize(16777215, 25))
        self.LimApproach.setObjectName("LimApproach")
        self.LimApproach.setText("0")
        self.gridLayout_4.addWidget(self.LimApproach, 3, 1, 1, 1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.LimOutType = QLabel(self.Lim)
        self.LimOutType.setObjectName("LimOutType")
        self.horizontalLayout_3.addWidget(self.LimOutType)
        self.LimPP = QRadioButton(self.Lim)
        self.LimPP.setChecked(True)
        self.LimPP.setObjectName("LimPP")
        self.horizontalLayout_3.addWidget(self.LimPP)
        self.LimLatex = QRadioButton(self.Lim)
        self.LimLatex.setObjectName("LimLatex")
        self.horizontalLayout_3.addWidget(self.LimLatex)
        self.LimNormal = QRadioButton(self.Lim)
        self.LimNormal.setObjectName("LimNormal")
        self.horizontalLayout_3.addWidget(self.LimNormal)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 6, 0, 1, 2)
        self.LimApprox = QLineEdit(self.Lim)
        self.LimApprox.setReadOnly(True)
        self.LimApprox.setMinimumSize(QSize(0, 25))
        self.LimApprox.setMaximumSize(QSize(16777215, 25))
        self.LimApprox.setObjectName("LimApprox")
        self.gridLayout_4.addWidget(self.LimApprox, 6, 2, 1, 1)
        self.LimPrev = QPushButton(self.Lim)
        self.LimPrev.setObjectName("LimPrev")
        self.LimPrev.clicked.connect(self.prev_limit)
        self.gridLayout_4.addWidget(self.LimPrev, 4, 0, 1, 2)
        self.LimCalc = QPushButton(self.Lim)
        self.LimCalc.setObjectName("LimCalc")
        self.LimCalc.clicked.connect(self.calc_limit)
        self.gridLayout_4.addWidget(self.LimCalc, 5, 0, 1, 2)
        self.tabWidget.addTab(self.Lim, "")

        self.Eq = QWidget()
        self.Eq.setObjectName("Eq")
        self.gridLayout_5 = QGridLayout(self.Eq)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.EqOutType = QLabel(self.Eq)
        self.EqOutType.setObjectName("EqOutType")
        self.horizontalLayout_4.addWidget(self.EqOutType)
        self.EqPP = QRadioButton(self.Eq)
        self.EqPP.setChecked(True)
        self.EqPP.setObjectName("EqPP")
        self.OutTypeGroup = QButtonGroup(MainWindow)
        self.OutTypeGroup.setObjectName("OutTypeGroup")
        self.OutTypeGroup.addButton(self.EqPP)
        self.horizontalLayout_4.addWidget(self.EqPP)
        self.EqLatex = QRadioButton(self.Eq)
        self.EqLatex.setObjectName("EqLatex")
        self.OutTypeGroup.addButton(self.EqLatex)
        self.horizontalLayout_4.addWidget(self.EqLatex)
        self.EqNormal = QRadioButton(self.Eq)
        self.EqNormal.setObjectName("EqNormal")
        self.OutTypeGroup.addButton(self.EqNormal)
        self.horizontalLayout_4.addWidget(self.EqNormal)
        self.gridLayout_5.addLayout(self.horizontalLayout_4, 6, 0, 1, 2)
        self.EqApprox = QTextBrowser(self.Eq)
        self.EqApprox.setMinimumSize(QSize(0, 25))
        self.EqApprox.setMaximumSize(QSize(16777215, 25))
        self.EqApprox.setObjectName("EqApprox")
        self.gridLayout_5.addWidget(self.EqApprox, 6, 2, 1, 1)
        self.EqLeft = QTextEdit(self.Eq)
        self.EqLeft.setMaximumSize(QSize(16777215, 16777215))
        self.EqLeft.setLineWrapMode(QTextEdit.NoWrap)
        self.EqLeft.setObjectName("EqLeft")
        self.gridLayout_5.addWidget(self.EqLeft, 0, 0, 1, 2)
        self.EqCalc = QPushButton(self.Eq)
        self.EqCalc.setObjectName("EqCalc")
        self.EqCalc.clicked.connect(self.calc_eq)
        self.gridLayout_5.addWidget(self.EqCalc, 5, 0, 1, 2)
        self.EqRight = QTextEdit(self.Eq)
        self.EqRight.setLineWrapMode(QTextEdit.NoWrap)
        self.EqRight.setObjectName("EqRight")
        self.gridLayout_5.addWidget(self.EqRight, 1, 0, 1, 2)
        self.EqPrev = QPushButton(self.Eq)
        self.EqPrev.setObjectName("EqPrev")
        self.EqPrev.clicked.connect(self.prev_eq)
        self.gridLayout_5.addWidget(self.EqPrev, 4, 0, 1, 2)
        self.EqOut = QTextBrowser(self.Eq)
        self.EqOut.setMaximumSize(QSize(16777215, 16777215))
        self.EqOut.setLineWrapMode(QTextEdit.NoWrap)
        self.EqOut.setObjectName("EqOut")
        self.gridLayout_5.addWidget(self.EqOut, 0, 2, 6, 1)
        self.horizontalLayoutEq = QHBoxLayout()
        self.horizontalLayoutEq.setObjectName("horizontalLayoutEq")
        self.EqSolve = QRadioButton(self.Eq)
        self.EqSolve.setChecked(True)
        self.EqSolve.setObjectName("EqSolve")
        self.horizontalLayoutEq.addWidget(self.EqSolve)
        self.EqSolveSet = QRadioButton(self.Eq)
        self.EqSolveSet.setObjectName("EqSolveSet")
        self.horizontalLayoutEq.addWidget(self.EqSolveSet)
        self.gridLayout_5.addLayout(self.horizontalLayoutEq, 3, 0, 1, 1)
        self.EqVar = QLineEdit(self.Eq)
        self.EqVar.setObjectName("EqVar")
        self.EqVar.setText("x")
        self.EqVar.setValidator(textVal)
        self.gridLayout_5.addWidget(self.EqVar, 2, 0, 1, 1)
        self.tabWidget.addTab(self.Eq, "")

        self.Simp = QWidget()
        self.Simp.setObjectName("Simp")
        self.gridLayout_6 = QGridLayout(self.Simp)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.SimpOutType = QLabel(self.Simp)
        self.SimpOutType.setMinimumSize(QSize(0, 25))
        self.SimpOutType.setMaximumSize(QSize(16777215, 25))
        self.SimpOutType.setObjectName("SimpOutType")
        self.horizontalLayout_5.addWidget(self.SimpOutType)
        self.SimpPP = QRadioButton(self.Simp)
        self.SimpPP.setChecked(True)
        self.SimpPP.setObjectName("SimpPP")
        self.horizontalLayout_5.addWidget(self.SimpPP)
        self.SimpLatex = QRadioButton(self.Simp)
        self.SimpLatex.setObjectName("SimpLatex")
        self.horizontalLayout_5.addWidget(self.SimpLatex)
        self.SimpNormal = QRadioButton(self.Simp)
        self.SimpNormal.setObjectName("SimpNormal")
        self.horizontalLayout_5.addWidget(self.SimpNormal)
        self.gridLayout_6.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)
        self.SimpCalc = QPushButton(self.Simp)
        self.SimpCalc.setObjectName("SimpCalc")
        self.SimpCalc.clicked.connect(self.simp_eq)
        self.gridLayout_6.addWidget(self.SimpCalc, 2, 0, 1, 1)
        self.SimpExp = QTextEdit(self.Simp)
        self.SimpExp.setMaximumSize(QSize(16777215, 16777215))
        self.SimpExp.setLineWrapMode(QTextEdit.NoWrap)
        self.SimpExp.setObjectName("SimpExp")
        self.gridLayout_6.addWidget(self.SimpExp, 0, 0, 1, 1)
        self.SimpPrev = QPushButton(self.Simp)
        self.SimpPrev.setObjectName("SimpPrev")
        self.SimpPrev.clicked.connect(self.prev_simp_eq)
        self.gridLayout_6.addWidget(self.SimpPrev, 1, 0, 1, 1)
        self.SimpOut = QTextBrowser(self.Simp)
        self.SimpOut.setEnabled(True)
        self.SimpOut.setMinimumSize(QSize(0, 0))
        self.SimpOut.setMaximumSize(QSize(16777215, 16777215))
        self.SimpOut.setLineWrapMode(QTextEdit.NoWrap)
        self.SimpOut.setObjectName("SimpOut")
        self.gridLayout_6.addWidget(self.SimpOut, 0, 1, 4, 1)
        self.tabWidget.addTab(self.Simp, "")

        self.Exp = QWidget()
        self.Exp.setObjectName("Exp")
        self.gridLayout_13 = QGridLayout(self.Exp)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.ExpExp = QTextEdit(self.Exp)
        self.ExpExp.setMaximumSize(QSize(16777215, 16777215))
        self.ExpExp.setLineWrapMode(QTextEdit.NoWrap)
        self.ExpExp.setObjectName("ExpExp")
        self.gridLayout_13.addWidget(self.ExpExp, 0, 0, 1, 1)
        self.ExpOut = QTextBrowser(self.Exp)
        self.ExpOut.setEnabled(True)
        self.ExpOut.setMinimumSize(QSize(0, 0))
        self.ExpOut.setMaximumSize(QSize(16777215, 16777215))
        self.ExpOut.setLineWrapMode(QTextEdit.NoWrap)
        self.ExpOut.setObjectName("ExpOut")
        self.gridLayout_13.addWidget(self.ExpOut, 0, 1, 4, 1)
        self.ExpPrev = QPushButton(self.Exp)
        self.ExpPrev.setObjectName("ExpPrev")
        self.ExpPrev.clicked.connect(self.prev_exp_eq)
        self.gridLayout_13.addWidget(self.ExpPrev, 1, 0, 1, 1)
        self.ExpCalc = QPushButton(self.Exp)
        self.ExpCalc.setObjectName("ExpCalc")
        self.ExpCalc.clicked.connect(self.exp_eq)
        self.gridLayout_13.addWidget(self.ExpCalc, 2, 0, 1, 1)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.ExpOutType = QLabel(self.Exp)
        self.ExpOutType.setMinimumSize(QSize(0, 25))
        self.ExpOutType.setMaximumSize(QSize(16777215, 25))
        self.ExpOutType.setObjectName("ExpOutType")
        self.horizontalLayout_11.addWidget(self.ExpOutType)
        self.ExpPP = QRadioButton(self.Exp)
        self.ExpPP.setChecked(True)
        self.ExpPP.setObjectName("ExpPP")
        self.horizontalLayout_11.addWidget(self.ExpPP)
        self.ExpLatex = QRadioButton(self.Exp)
        self.ExpLatex.setObjectName("ExpLatex")
        self.horizontalLayout_11.addWidget(self.ExpLatex)
        self.ExpNormal = QRadioButton(self.Exp)
        self.ExpNormal.setObjectName("ExpNormal")
        self.horizontalLayout_11.addWidget(self.ExpNormal)
        self.gridLayout_13.addLayout(self.horizontalLayout_11, 3, 0, 1, 1)
        self.tabWidget.addTab(self.Exp, "")

        self.Eval = QWidget()
        self.Eval.setObjectName("Eval")
        self.gridLayout_14 = QGridLayout(self.Eval)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.EvalExp = QTextEdit(self.Eval)
        self.EvalExp.setMaximumSize(QSize(16777215, 16777215))
        self.EvalExp.setLineWrapMode(QTextEdit.NoWrap)
        self.EvalExp.setObjectName("EvalExp")
        self.gridLayout_14.addWidget(self.EvalExp, 0, 0, 1, 1)
        self.EvalOut = QTextBrowser(self.Eval)
        self.EvalOut.setEnabled(True)
        self.EvalOut.setMinimumSize(QSize(0, 0))
        self.EvalOut.setMaximumSize(QSize(16777215, 16777215))
        self.EvalOut.setLineWrapMode(QTextEdit.NoWrap)
        self.EvalOut.setObjectName("EvalOut")
        self.gridLayout_14.addWidget(self.EvalOut, 0, 1, 4, 1)
        self.EvalPrev = QPushButton(self.Eval)
        self.EvalPrev.setObjectName("EvalPrev")
        self.EvalPrev.clicked.connect(self.prev_eval_exp)
        self.gridLayout_14.addWidget(self.EvalPrev, 1, 0, 1, 1)
        self.EvalCalc = QPushButton(self.Eval)
        self.EvalCalc.setObjectName("EvalCalc")
        self.EvalCalc.clicked.connect(self.eval_exp)
        self.gridLayout_14.addWidget(self.EvalCalc, 2, 0, 1, 1)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.EvalOutType = QLabel(self.Eval)
        self.EvalOutType.setObjectName("EvalOutType")
        self.horizontalLayout_13.addWidget(self.EvalOutType)
        self.EvalPP = QRadioButton(self.Eval)
        self.EvalPP.setChecked(True)
        self.EvalPP.setObjectName("EvalPP")
        self.horizontalLayout_13.addWidget(self.EvalPP)
        self.EvalLatex = QRadioButton(self.Eval)
        self.EvalLatex.setObjectName("EvalLatex")
        self.horizontalLayout_13.addWidget(self.EvalLatex)
        self.EvalNormal = QRadioButton(self.Eval)
        self.EvalNormal.setObjectName("EvalNormal")
        self.horizontalLayout_13.addWidget(self.EvalNormal)
        self.gridLayout_14.addLayout(self.horizontalLayout_13, 4, 0, 1, 1)
        self.EvalApprox = QTextBrowser(self.Eval)
        self.EvalApprox.setMinimumSize(QSize(0, 25))
        self.EvalApprox.setMaximumSize(QSize(16777215, 25))
        self.EvalApprox.setObjectName("EvalApprox")
        self.gridLayout_14.addWidget(self.EvalApprox, 4, 1, 1, 1)
        self.tabWidget.addTab(self.Eval, "")

        self.Pf = QWidget()
        self.Pf.setObjectName("Pf")
        self.gridLayout_15 = QGridLayout(self.Pf)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_32 = QLabel(self.Pf)
        self.label_32.setMinimumSize(QSize(40, 0))
        self.label_32.setMaximumSize(QSize(40, 16777215))
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_14.addWidget(self.label_32)
        self.PfInput = QSpinBox(self.Pf)
        self.PfInput.setMinimum(1)
        self.PfInput.setMaximum(999999999)
        self.PfInput.setObjectName("PfInput")
        self.horizontalLayout_14.addWidget(self.PfInput)
        self.verticalLayout.addLayout(self.horizontalLayout_14)
        self.PfCalc = QPushButton(self.Pf)
        self.PfCalc.setObjectName("PfCalc")
        self.PfCalc.clicked.connect(self.calc_pf)
        self.verticalLayout.addWidget(self.PfCalc)
        self.PfOut = QTextBrowser(self.Pf)
        self.PfOut.setPlaceholderText("")
        self.PfOut.setObjectName("PfOut")
        self.verticalLayout.addWidget(self.PfOut)
        self.gridLayout_15.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.tabWidget.addTab(self.Pf, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.Web = QWidget()
        self.Web.setObjectName("Web")
        self.gridWeb = QGridLayout(self.Web)
        self.gridWeb.setObjectName("gridWeb")
        self.web = QWebEngineView()

        self.web.load(QUrl("https://www.desmos.com/calculator"))
        self.gridWeb.addWidget(self.web, 0, 0, 1, 1)
        self.tabWidget.addTab(self.Web, "")

        self.Formula = QWidget()
        self.Formula.setObjectName("Formula")
        self.FormulaGrid = QGridLayout(self.Formula)
        self.FormulaGrid.setObjectName("FormulaGrid")
        self.FormulaOutputLayout = QVBoxLayout()
        self.FormulaOutputLayout.setObjectName("FormulaOutputLayout")
        self.FormulaSolveGroup = QButtonGroup(MainWindow)
        self.FormulaSolveGroup.setObjectName("FormulaSolveGroup")
        self.FormulaSolveLayout = QHBoxLayout()
        self.FormulaSolveLayout.setObjectName("FormulaSolveLayout")
        self.FormulaSolveSolve = QRadioButton(self.Formula)
        self.FormulaSolveSolve.setObjectName("FormulaSolveSolve")
        self.FormulaSolveSolve.setChecked(True)
        self.FormulaSolveGroup.addButton(self.FormulaSolveSolve)
        self.FormulaSolveLayout.addWidget(self.FormulaSolveSolve)
        self.FormulaSolveSolveSet = QRadioButton(self.Formula)
        self.FormulaSolveSolveSet.setObjectName("FormulaSolveSolveSet")
        self.FormulaSolveGroup.addButton(self.FormulaSolveSolveSet)
        self.FormulaSolveLayout.addWidget(self.FormulaSolveSolveSet)
        self.FormulaOutputLayout.addLayout(self.FormulaSolveLayout)
        self.FormulaPreview = QPushButton(self.Formula)
        self.FormulaPreview.setObjectName("FormulaPreview")
        self.FormulaPreview.clicked.connect(self.prev_formula)
        self.FormulaOutputLayout.addWidget(self.FormulaPreview)
        self.FormulaCalculate = QPushButton(self.Formula)
        self.FormulaCalculate.setObjectName("FormulaCalculate")
        self.FormulaCalculate.clicked.connect(self.calc_formula)
        self.FormulaOutputLayout.addWidget(self.FormulaCalculate)
        self.FormulaOutTypeLayout = QHBoxLayout()
        self.FormulaOutTypeLayout.setObjectName("FormulaOutTypeLayout")
        self.FormulaOutTypeLabel = QLabel(self.Formula)
        self.FormulaOutTypeLabel.setObjectName("FormulaOutTypeLabel")
        self.FormulaOutTypeLayout.addWidget(self.FormulaOutTypeLabel)
        self.FormulaPP = QRadioButton(self.Formula)
        self.FormulaPP.setChecked(True)
        self.FormulaPP.setObjectName("FormulaPP")
        self.FormulaOutTypeLayout.addWidget(self.FormulaPP)
        self.FormulaLatex = QRadioButton(self.Formula)
        self.FormulaLatex.setObjectName("FormulaLatex")
        self.FormulaOutTypeLayout.addWidget(self.FormulaLatex)
        self.FormulaNormal = QRadioButton(self.Formula)
        self.FormulaNormal.setObjectName("FormulaNormal")
        self.FormulaOutTypeLayout.addWidget(self.FormulaNormal)
        self.FormulaOutputLayout.addLayout(self.FormulaOutTypeLayout)
        self.FormulaExact = QTextBrowser(self.Formula)
        self.FormulaExact.setObjectName("FomulaExact")
        self.FormulaOutputLayout.addWidget(self.FormulaExact)
        self.FormulaApprox = QLineEdit(self.Formula)
        self.FormulaApprox.setReadOnly(True)
        self.FormulaApprox.setObjectName("FomulaApprox")
        self.FormulaOutputLayout.addWidget(self.FormulaApprox)
        self.FormulaGrid.addLayout(self.FormulaOutputLayout, 0, 1, 1, 1)
        self.FormulaViewerLayout = QVBoxLayout()
        self.FormulaViewerLayout.setObjectName("FormulaViewerLayout")
        self.FormulaTree = QTreeWidget(self.Formula)
        self.FormulaTree.setObjectName("FormulaTree")
        self.FormulaTree.itemDoubleClicked.connect(self.FormulaTreeSelected)
        self.FormulaTreeData = self.json_file
        self.FormulaInfoDict = self.FormulaTreeData[0]
        self.FormulaTreeData = self.FormulaTreeData[1]

        for branch in self.FormulaTreeData:
            parent = QTreeWidgetItem(self.FormulaTree)
            parent.setText(0, str(branch[0]))
            for subBranch in branch[1]:
                child = QTreeWidgetItem(parent)
                child.setText(0, str(subBranch[0]))
                for formula in subBranch[1]:
                    formulaChild = QTreeWidgetItem(child)
                    formulaChild.setText(0, formula[0])

        self.FormulaViewerLayout.addWidget(self.FormulaTree)
        self.FormulaLine = QFrame(self.Formula)
        self.FormulaLine.setFrameShape(QFrame.HLine)
        self.FormulaLine.setFrameShadow(QFrame.Sunken)
        self.FormulaLine.setObjectName("FormulaLine")
        self.FormulaViewerLayout.addWidget(self.FormulaLine)
        self.FormulaScroll = QScrollArea(self.Formula)
        self.FormulaScroll.setEnabled(True)
        self.FormulaScroll.setWidgetResizable(True)
        self.FormulaScroll.setObjectName("FormulaScroll")
        self.FormulaScrollArea = QWidget()
        self.FormulaScrollArea.setGeometry(QRect(0, 0, 372, 364))
        self.FormulaScrollArea.setObjectName("FormulaScrollArea")
        self.FormulaGrid2 = QGridLayout(self.FormulaScrollArea)
        self.FormulaGrid2.setObjectName("FormulaGrid2")
        self.FormulaScroll.setWidget(self.FormulaScrollArea)
        self.FormulaViewerLayout.addWidget(self.FormulaScroll)
        self.FormulaGrid.addLayout(self.FormulaViewerLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.Formula, "")

        self.Shell = QWidget()
        self.Shell.setObjectName("Shell")
        """
        Setups variables and information.
        """
        self.current_code = "This is a very simple shell using 'exec' commands, so it has some limitations.\n" \
                           "Every variable declared and function defined will be saved until the program is closed" \
                           " or when the 'clear commands' button in the menubar is pressed.\n" \
                           "It will automatically output to the shell, but it can't use 'print' commands. To copy" \
                           " output, press the 'copy exact answer' in the menubar\nTheses commands were executed:\n" \
                           "from __future__ import division\n" \
                           "from sympy import *\n" \
                           "from sympy.parsing.sympy_parser import parse_expr\n" \
                           "from sympy.abc import _clash1\nimport math as m\nx, y, z, t = symbols('x y z t')\n" \
                           "k, m, n = symbols('k m n', integer=True)\nf, g, h = symbols('f g h', cls=Function)\n\n>>> "
        self.ShellGrid = QGridLayout(self.Shell)
        self.ShellGrid.setObjectName("ShellGrid")
        self.consoleIn = QPlainTextEdit(self.centralwidget)
        self.consoleIn.setObjectName("consoleIn")
        self.consoleIn.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.consoleIn.insertPlainText(self.current_code)
        self.consoleIn.setTabStopWidth(40)
        self.consoleIn.setTabStopDistance(40.0)
        self.ShellGrid.addWidget(self.consoleIn, 0, 0, 1, 1)
        self.ShellRun = QPushButton(self.centralwidget)
        self.ShellRun.setObjectName("ShellRun")
        self.ShellRun.clicked.connect(self.execute_code)
        self.ShellGrid.addWidget(self.ShellRun, 1, 0, 1, 1)
        self.tabWidget.addTab(self.Shell, "")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 678, 21))
        self.menubar.setObjectName("menubar")
        self.menuCopy = QMenu(self.menubar)
        self.menuCopy.setObjectName("menuCopy")
        self.menuTab = QMenu(self.menubar)
        self.menuTab.setObjectName("menuTab")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuWeb = QMenu(self.menubar)
        self.menuWeb.setObjectName("menuWeb")

        self.WebList = self.json_file[2]
        webGroup = QActionGroup(self.menuWeb)
        for i in self.WebList:
            for key in i:
                webAction = QAction(key, self.menuWeb, checkable=True)
                if webAction.text() == "Desmos":
                    webAction.setChecked(True)
                self.menuWeb.addAction(webAction)
                webGroup.addAction(webAction)
        webGroup.setExclusive(True)
        webGroup.triggered.connect(self.updateWeb)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionCopy_exact_answer = QAction(MainWindow)
        self.actionCopy_exact_answer.setObjectName("actionCopy_exact_answer")
        self.actionCopy_approximate_answer = QAction(MainWindow)
        self.actionCopy_approximate_answer.setObjectName("actionCopy_approximate_answer")
        self.actionNext_Tab = QAction(MainWindow)
        self.actionNext_Tab.setObjectName("actionNext_Tab")
        self.actionPrevious_Tab = QAction(MainWindow)
        self.actionPrevious_Tab.setObjectName("actionPrevious_Tab")
        self.actionUse_Unicode = QAction(MainWindow)
        self.actionUse_Unicode.setCheckable(True)
        self.actionUse_Unicode.setObjectName("actionUse_Unicode")
        self.actionLine_Wrap = QAction(MainWindow)
        self.actionLine_Wrap.setCheckable(True)
        self.actionLine_Wrap.setObjectName("actionLine-Wrap")
        self.actionScientific = QAction(MainWindow)
        self.actionScientific.setCheckable(True)
        self.actionScientific.setObjectName("actionScientific")
        self.actionAccuracy = QAction(MainWindow)
        self.actionAccuracy.setCheckable(True)
        self.actionAccuracy.setObjectName("actionAccuracy")
        self.clearShell = QAction(MainWindow)
        self.clearShell.setObjectName("clearShell")
        self.menuSettings.addAction(self.actionUse_Unicode)
        self.menuSettings.addAction(self.actionLine_Wrap)
        self.menuSettings.addAction(self.actionScientific)
        self.menuSettings.addAction(self.actionAccuracy)
        self.menuSettings.addAction(self.clearShell)
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuCopy.addAction(self.actionCopy_exact_answer)
        self.menuCopy.addAction(self.actionCopy_approximate_answer)
        self.menuTab.addAction(self.actionNext_Tab)
        self.menuTab.addAction(self.actionPrevious_Tab)
        self.menubar.addAction(self.menuCopy.menuAction())
        self.menubar.addAction(self.menuTab.menuAction())
        self.menubar.addAction(self.menuWeb.menuAction())
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Code generated by QtDesigner
        """
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calculus"))
        self.tabWidget.setToolTip(_translate("MainWindow", "Tabs"))
        self.tabWidget.setStatusTip(_translate("MainWindow", "Tabs for actions"))
        self.tabWidget.setWhatsThis(_translate("MainWindow", "Tabs for actions"))
        self.Deriv.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.DerivPrev.setToolTip(_translate("MainWindow", "Preview"))
        self.DerivPrev.setStatusTip(_translate("MainWindow", "Preview the expression"))
        self.DerivPrev.setWhatsThis(_translate("MainWindow", "Preview"))
        self.DerivPrev.setText(_translate("MainWindow", "Preview"))
        self.DerivCalc.setToolTip(_translate("MainWindow", "Calculate"))
        self.DerivCalc.setStatusTip(_translate("MainWindow", "Calculate the derivative"))
        self.DerivCalc.setWhatsThis(_translate("MainWindow", "Calculate"))
        self.DerivCalc.setText(_translate("MainWindow", "Calculate"))
        self.label_9.setText(_translate("MainWindow", "At point"))
        self.DerivExp.setToolTip(_translate("MainWindow", "Your expression"))
        self.DerivExp.setStatusTip(_translate("MainWindow", "Type in your expression here"))
        self.DerivExp.setWhatsThis(_translate("MainWindow", "Input expression"))
        self.DerivExp.setPlaceholderText(_translate("MainWindow", "Expression"))
        self.label.setText(_translate("MainWindow", "Order"))
        self.DerivOutType.setText(_translate("MainWindow", "Output type"))
        self.DerivPP.setToolTip(_translate("MainWindow", "Pretty print"))
        self.DerivPP.setStatusTip(_translate("MainWindow", "Pretty print"))
        self.DerivPP.setWhatsThis(_translate("MainWindow", "Pretty print"))
        self.DerivPP.setText(_translate("MainWindow", "Pretty"))
        self.DerivLatex.setToolTip(_translate("MainWindow", "Latex"))
        self.DerivLatex.setStatusTip(_translate("MainWindow", "Latex"))
        self.DerivLatex.setWhatsThis(_translate("MainWindow", "Latex"))
        self.DerivLatex.setText(_translate("MainWindow", "Latex"))
        self.DerivNormal.setToolTip(_translate("MainWindow", "Normal"))
        self.DerivNormal.setStatusTip(_translate("MainWindow", "Normal"))
        self.DerivNormal.setWhatsThis(_translate("MainWindow", "Normal"))
        self.DerivNormal.setText(_translate("MainWindow", "Normal"))
        self.DerivOrder.setToolTip(_translate("MainWindow", "The order of the derivative"))
        self.DerivOrder.setStatusTip(_translate("MainWindow", "The order of the derivative, default is 1, max is 999"))
        self.DerivOrder.setWhatsThis(_translate("MainWindow", "The order of the derivative"))
        self.DerivVar.setToolTip(_translate("MainWindow", "Variable"))
        self.DerivVar.setStatusTip(_translate("MainWindow", "Derivative with respect to variable"))
        self.DerivVar.setWhatsThis(_translate("MainWindow", "Variable"))
        self.DerivPoint.setToolTip(_translate("MainWindow", "Calculate the derivative at a point"))
        self.DerivPoint.setStatusTip(
            _translate("MainWindow", "Calculate the derivative at a point, leave blank for at point x"))
        self.DerivPoint.setWhatsThis(_translate("MainWindow", "Calculate the derivative at a point"))
        self.label_3.setText(_translate("MainWindow", "Variable"))
        self.DerivOut.setToolTip(_translate("MainWindow", "Output"))
        self.DerivOut.setStatusTip(_translate("MainWindow", "Output in exact form"))
        self.DerivOut.setWhatsThis(_translate("MainWindow", "Output in exact form"))
        self.DerivApprox.setToolTip(_translate("MainWindow", "Output"))
        self.DerivApprox.setStatusTip(_translate("MainWindow",
                                                 "Output in approximate form, will only show when the derivative is calculated at a certain point"))
        self.DerivApprox.setWhatsThis(_translate("MainWindow", "Output in approximate form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Deriv), _translate("MainWindow", "Derivative"))
        self.IntegExp.setToolTip(_translate("MainWindow", "Your expression"))
        self.IntegExp.setStatusTip(_translate("MainWindow", "Type in your expression here"))
        self.IntegExp.setWhatsThis(_translate("MainWindow", "Input expression"))
        self.IntegExp.setPlaceholderText(_translate("MainWindow", "Expression"))
        self.IntegOut.setToolTip(_translate("MainWindow", "Output"))
        self.IntegOut.setStatusTip(_translate("MainWindow", "Output in exact form"))
        self.IntegOut.setWhatsThis(_translate("MainWindow", "Output in exact form"))
        self.label_2.setText(_translate("MainWindow", "From"))
        self.IntegLower.setToolTip(_translate("MainWindow", "Lower boundry"))
        self.IntegLower.setStatusTip(
            _translate("MainWindow", "Lower boundry, infinity is \"oo\", leave empty for indefinite integral"))
        self.IntegLower.setWhatsThis(_translate("MainWindow", "Lower boundry"))
        self.label_5.setText(_translate("MainWindow", "To"))
        self.IntegUpper.setToolTip(_translate("MainWindow", "Upper boundry"))
        self.IntegUpper.setStatusTip(
            _translate("MainWindow", "Upper boundry, infinity is \"oo\", leave empty for indefinite integral"))
        self.IntegUpper.setWhatsThis(_translate("MainWindow", "Upper boundry"))
        self.label_4.setText(_translate("MainWindow", "Variable"))
        self.IntegVar.setToolTip(_translate("MainWindow", "Variable"))
        self.IntegVar.setStatusTip(_translate("MainWindow", "Integral with respect to variable"))
        self.IntegVar.setWhatsThis(_translate("MainWindow", "Variable"))
        self.IntegPrev.setText(_translate("MainWindow", "Preview"))
        self.IntegCalc.setToolTip(_translate("MainWindow", "Calculate"))
        self.IntegCalc.setStatusTip(_translate("MainWindow", "Calculate the integral"))
        self.IntegCalc.setWhatsThis(_translate("MainWindow", "Calculate"))
        self.IntegCalc.setText(_translate("MainWindow", "Calculate"))
        self.IntegOutType.setText(_translate("MainWindow", "Output type"))
        self.IntegPP.setToolTip(_translate("MainWindow", "Pretty print"))
        self.IntegPP.setStatusTip(_translate("MainWindow", "Pretty print"))
        self.IntegPP.setWhatsThis(_translate("MainWindow", "Pretty print"))
        self.IntegPP.setText(_translate("MainWindow", "Pretty"))
        self.IntegLatex.setToolTip(_translate("MainWindow", "Latex"))
        self.IntegLatex.setStatusTip(_translate("MainWindow", "Latex"))
        self.IntegLatex.setWhatsThis(_translate("MainWindow", "Latex"))
        self.IntegLatex.setText(_translate("MainWindow", "Latex"))
        self.IntegNormal.setToolTip(_translate("MainWindow", "Normal"))
        self.IntegNormal.setStatusTip(_translate("MainWindow", "Normal"))
        self.IntegNormal.setWhatsThis(_translate("MainWindow", "Normal"))
        self.IntegNormal.setText(_translate("MainWindow", "Normal"))
        self.IntegApprox.setToolTip(_translate("MainWindow", "Output"))
        self.IntegApprox.setStatusTip(_translate("MainWindow",
                                                 "Output in approximate form, will only show when a definite integral is calculated"))
        self.IntegApprox.setWhatsThis(_translate("MainWindow", "Output in approximate form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Integ), _translate("MainWindow", "Integral"))
        self.LimExp.setToolTip(_translate("MainWindow", "Your expression"))
        self.LimExp.setStatusTip(_translate("MainWindow", "Type in your expression here"))
        self.LimExp.setWhatsThis(_translate("MainWindow", "Input expression"))
        self.LimExp.setPlaceholderText(_translate("MainWindow", "Expression"))
        self.LimOut.setToolTip(_translate("MainWindow", "Output"))
        self.LimOut.setStatusTip(_translate("MainWindow", "Output in exact form"))
        self.LimOut.setWhatsThis(_translate("MainWindow", "Output in exact form"))
        self.label_6.setText(_translate("MainWindow", "Side"))
        self.LimSide.setItemText(0, _translate("MainWindow", "Both sides"))
        self.LimSide.setItemText(1, _translate("MainWindow", "Left"))
        self.LimSide.setItemText(2, _translate("MainWindow", "Right"))
        self.label_7.setText(_translate("MainWindow", "Variable"))
        self.LimVar.setToolTip(_translate("MainWindow", "Variable"))
        self.LimVar.setStatusTip(_translate("MainWindow", "Limit with respect to variable"))
        self.LimVar.setWhatsThis(_translate("MainWindow", "Variable"))
        self.label_8.setText(_translate("MainWindow", "As variable approaches"))
        self.LimOutType.setText(_translate("MainWindow", "Output type"))
        self.LimPP.setText(_translate("MainWindow", "Pretty"))
        self.LimLatex.setToolTip(_translate("MainWindow", "Latex"))
        self.LimLatex.setStatusTip(_translate("MainWindow", "Latex"))
        self.LimLatex.setWhatsThis(_translate("MainWindow", "Latex"))
        self.LimLatex.setText(_translate("MainWindow", "Latex"))
        self.LimNormal.setToolTip(_translate("MainWindow", "Normal"))
        self.LimNormal.setStatusTip(_translate("MainWindow", "Normal"))
        self.LimNormal.setWhatsThis(_translate("MainWindow", "Normal"))
        self.LimNormal.setText(_translate("MainWindow", "Normal"))
        self.LimApprox.setToolTip(_translate("MainWindow", "Output"))
        self.LimApprox.setStatusTip(_translate("MainWindow", "Output in approximate form"))
        self.LimApprox.setWhatsThis(_translate("MainWindow", "Output in approximate form"))
        self.LimPrev.setText(_translate("MainWindow", "Preview"))
        self.LimCalc.setToolTip(_translate("MainWindow", "Calculate"))
        self.LimCalc.setStatusTip(_translate("MainWindow", "Calculate the limit"))
        self.LimCalc.setWhatsThis(_translate("MainWindow", "Calculate"))
        self.LimCalc.setText(_translate("MainWindow", "Calculate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Lim), _translate("MainWindow", "Limit"))
        self.EqOutType.setText(_translate("MainWindow", "Output type"))
        self.EqPP.setText(_translate("MainWindow", "Pretty"))
        self.EqSolve.setText(_translate("MainWindow", "Solve"))
        self.EqSolve.setToolTip(_translate("MainWindow", "Solve"))
        self.EqSolve.setStatusTip(_translate("MainWindow", "See Sympy Solve vs Solveset"))
        self.EqSolve.setWhatsThis(_translate("MainWindow", "See Sympy Solve vs Solveset"))
        self.EqSolveSet.setText(_translate("MainWindow", "Solveset"))
        self.EqSolveSet.setToolTip(_translate("MainWindow", "Solveset"))
        self.EqSolveSet.setStatusTip(_translate("MainWindow", "See Sympy Solve vs Solveset"))
        self.EqSolveSet.setWhatsThis(_translate("MainWindow", "See Sympy Solve vs Solveset"))
        self.EqLatex.setToolTip(_translate("MainWindow", "Latex"))
        self.EqLatex.setStatusTip(_translate("MainWindow", "Latex"))
        self.EqLatex.setWhatsThis(_translate("MainWindow", "Latex"))
        self.EqLatex.setText(_translate("MainWindow", "Latex"))
        self.EqNormal.setToolTip(_translate("MainWindow", "Normal"))
        self.EqNormal.setStatusTip(_translate("MainWindow", "Normal"))
        self.EqNormal.setWhatsThis(_translate("MainWindow", "Normal"))
        self.EqNormal.setText(_translate("MainWindow", "Normal"))
        self.EqApprox.setToolTip(_translate("MainWindow", "Output"))
        self.EqApprox.setStatusTip(_translate("MainWindow", "Output in approximate form"))
        self.EqApprox.setWhatsThis(_translate("MainWindow", "Output in approximate form"))
        self.EqLeft.setToolTip(_translate("MainWindow", "Left side "))
        self.EqLeft.setStatusTip(_translate("MainWindow", "Left side of your expression"))
        self.EqLeft.setWhatsThis(_translate("MainWindow", "Left side"))
        self.EqLeft.setPlaceholderText(_translate("MainWindow", "Left side"))
        self.EqCalc.setToolTip(_translate("MainWindow", "Calculate"))
        self.EqCalc.setStatusTip(_translate("MainWindow", "Calculate the equation"))
        self.EqCalc.setWhatsThis(_translate("MainWindow", "Calculate"))
        self.EqCalc.setText(_translate("MainWindow", "Calculate"))
        self.EqRight.setToolTip(_translate("MainWindow", "Right side"))
        self.EqRight.setStatusTip(_translate("MainWindow", "Right side of your expression"))
        self.EqRight.setWhatsThis(_translate("MainWindow", "Right side"))
        self.EqRight.setPlaceholderText(_translate("MainWindow", "Right side"))
        self.EqPrev.setText(_translate("MainWindow", "Preview"))
        self.EqOut.setToolTip(_translate("MainWindow", "Output"))
        self.EqOut.setStatusTip(_translate("MainWindow", "Output in exact form"))
        self.EqOut.setWhatsThis(_translate("MainWindow", "Output in exact form"))
        self.EqVar.setToolTip(_translate("MainWindow", "Variable"))
        self.EqVar.setStatusTip(_translate("MainWindow", "Solve for variable"))
        self.EqVar.setWhatsThis(_translate("MainWindow", "Solve for variable"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Eq), _translate("MainWindow", "Equation Solver"))
        self.SimpOutType.setText(_translate("MainWindow", "Output type"))
        self.SimpPP.setToolTip(_translate("MainWindow", "Pretty print"))
        self.SimpPP.setStatusTip(_translate("MainWindow", "Pretty print"))
        self.SimpPP.setWhatsThis(_translate("MainWindow", "Pretty print"))
        self.SimpPP.setText(_translate("MainWindow", "Pretty"))
        self.SimpLatex.setToolTip(_translate("MainWindow", "Latex"))
        self.SimpLatex.setStatusTip(_translate("MainWindow", "Latex"))
        self.SimpLatex.setWhatsThis(_translate("MainWindow", "Latex"))
        self.SimpLatex.setText(_translate("MainWindow", "Latex"))
        self.SimpNormal.setToolTip(_translate("MainWindow", "Normal"))
        self.SimpNormal.setStatusTip(_translate("MainWindow", "Normal"))
        self.SimpNormal.setWhatsThis(_translate("MainWindow", "Normal"))
        self.SimpNormal.setText(_translate("MainWindow", "Normal"))
        self.SimpCalc.setToolTip(_translate("MainWindow", "Simplify"))
        self.SimpCalc.setStatusTip(_translate("MainWindow", "Simplify the expression"))
        self.SimpCalc.setWhatsThis(_translate("MainWindow", "Simplify the expression"))
        self.SimpCalc.setText(_translate("MainWindow", "Simplify"))
        self.SimpExp.setToolTip(_translate("MainWindow", "Your expression"))
        self.SimpExp.setStatusTip(_translate("MainWindow", "Type in your expression here"))
        self.SimpExp.setWhatsThis(_translate("MainWindow", "Input expression"))
        self.SimpExp.setPlaceholderText(_translate("MainWindow", "Expression"))
        self.SimpPrev.setToolTip(_translate("MainWindow", "Preview"))
        self.SimpPrev.setStatusTip(_translate("MainWindow", "Preview the expression"))
        self.SimpPrev.setWhatsThis(_translate("MainWindow", "Preview"))
        self.SimpPrev.setText(_translate("MainWindow", "Preview"))
        self.SimpOut.setToolTip(_translate("MainWindow", "Output"))
        self.SimpOut.setStatusTip(_translate("MainWindow", "Output"))
        self.SimpOut.setWhatsThis(_translate("MainWindow", "Output"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Simp), _translate("MainWindow", "Simplify"))
        self.ExpExp.setToolTip(_translate("MainWindow", "Your expression"))
        self.ExpExp.setStatusTip(_translate("MainWindow", "Type in your expression here"))
        self.ExpExp.setWhatsThis(_translate("MainWindow", "Input expression"))
        self.ExpExp.setPlaceholderText(_translate("MainWindow", "Expression"))
        self.ExpOut.setToolTip(_translate("MainWindow", "Output"))
        self.ExpOut.setStatusTip(_translate("MainWindow", "Output"))
        self.ExpOut.setWhatsThis(_translate("MainWindow", "Output"))
        self.ExpPrev.setToolTip(_translate("MainWindow", "Preview"))
        self.ExpPrev.setStatusTip(_translate("MainWindow", "Preview the expression"))
        self.ExpPrev.setWhatsThis(_translate("MainWindow", "Preview the expression"))
        self.ExpPrev.setText(_translate("MainWindow", "Preview"))
        self.ExpCalc.setToolTip(_translate("MainWindow", "Expand"))
        self.ExpCalc.setStatusTip(_translate("MainWindow", "Expand the expression"))
        self.ExpCalc.setWhatsThis(_translate("MainWindow", "Expand the expression"))
        self.ExpCalc.setText(_translate("MainWindow", "Expand"))
        self.ExpOutType.setText(_translate("MainWindow", "Output type"))
        self.ExpPP.setToolTip(_translate("MainWindow", "Pretty print"))
        self.ExpPP.setStatusTip(_translate("MainWindow", "Pretty print"))
        self.ExpPP.setWhatsThis(_translate("MainWindow", "Pretty print"))
        self.ExpPP.setText(_translate("MainWindow", "Pretty"))
        self.ExpLatex.setToolTip(_translate("MainWindow", "Latex"))
        self.ExpLatex.setStatusTip(_translate("MainWindow", "Latex"))
        self.ExpLatex.setWhatsThis(_translate("MainWindow", "Latex"))
        self.ExpLatex.setText(_translate("MainWindow", "Latex"))
        self.ExpNormal.setToolTip(_translate("MainWindow", "Normal"))
        self.ExpNormal.setStatusTip(_translate("MainWindow", "Normal"))
        self.ExpNormal.setWhatsThis(_translate("MainWindow", "Normal"))
        self.ExpNormal.setText(_translate("MainWindow", "Normal"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Exp), _translate("MainWindow", "Expand"))
        self.EvalExp.setToolTip(_translate("MainWindow", "Your expression"))
        self.EvalExp.setStatusTip(_translate("MainWindow", "Type in your expression here"))
        self.EvalExp.setWhatsThis(_translate("MainWindow", "Input expression"))
        self.EvalExp.setPlaceholderText(_translate("MainWindow", "Expression"))
        self.EvalOut.setToolTip(_translate("MainWindow", "Output"))
        self.EvalOut.setStatusTip(_translate("MainWindow", "Output"))
        self.EvalOut.setWhatsThis(_translate("MainWindow", "Output"))
        self.EvalPrev.setToolTip(_translate("MainWindow", "Preview"))
        self.EvalPrev.setStatusTip(_translate("MainWindow", "Preview the expression"))
        self.EvalPrev.setWhatsThis(_translate("MainWindow", "Preview"))
        self.EvalPrev.setText(_translate("MainWindow", "Preview"))
        self.EvalCalc.setToolTip(_translate("MainWindow", "Evaluate"))
        self.EvalCalc.setStatusTip(_translate("MainWindow", "Evaluate the expression"))
        self.EvalCalc.setWhatsThis(_translate("MainWindow", "Evaluate"))
        self.EvalCalc.setText(_translate("MainWindow", "Evaluate"))
        self.EvalOutType.setText(_translate("MainWindow", "Output type"))
        self.EvalPP.setToolTip(_translate("MainWindow", "Pretty print"))
        self.EvalPP.setStatusTip(_translate("MainWindow", "Pretty print"))
        self.EvalPP.setWhatsThis(_translate("MainWindow", "Pretty print"))
        self.EvalPP.setText(_translate("MainWindow", "Pretty"))
        self.EvalLatex.setToolTip(_translate("MainWindow", "Latex"))
        self.EvalLatex.setStatusTip(_translate("MainWindow", "Latex"))
        self.EvalLatex.setWhatsThis(_translate("MainWindow", "Latex"))
        self.EvalLatex.setText(_translate("MainWindow", "Latex"))
        self.EvalNormal.setToolTip(_translate("MainWindow", "Normal"))
        self.EvalNormal.setStatusTip(_translate("MainWindow", "Normal"))
        self.EvalNormal.setWhatsThis(_translate("MainWindow", "Normal"))
        self.EvalNormal.setText(_translate("MainWindow", "Normal"))
        self.PfCalc.setToolTip(_translate("MainWindow", "Calculate"))
        self.PfCalc.setWhatsThis(_translate("MainWindow", "Calculate"))
        self.PfCalc.setWhatsThis(_translate("MainWindow", "Calculate"))
        self.PfCalc.setText(_translate("MainWindow", "Calculate"))
        self.FormulaPreview.setText(_translate("MainWindow", "Preview"))
        self.FormulaCalculate.setText(_translate("MainWindow", "Calculate"))
        self.FormulaOutTypeLabel.setText(_translate("MainWindow", "Output type"))
        self.FormulaSolveSolve.setText(_translate("MainWindow", "Solve"))
        self.FormulaSolveSolve.setStatusTip(_translate("MainWindow", "See Sympy Solve vs Solveset"))
        self.FormulaSolveSolve.setWhatsThis(_translate("MainWindow", "See Sympy Solve vs Solveset"))
        self.FormulaSolveSolveSet.setText(_translate("MainWindow", "Solveset"))
        self.FormulaSolveSolveSet.setStatusTip(_translate("MainWindow", "See Sympy Solve vs Solveset"))
        self.FormulaSolveSolveSet.setWhatsThis(_translate("MainWindow", "See Sympy Solve vs Solveset"))
        self.FormulaPP.setText(_translate("MainWindow", "PP"))
        self.FormulaLatex.setText(_translate("MainWindow", "Latex"))
        self.FormulaNormal.setText(_translate("MainWindow", "Normal"))
        self.FormulaTree.headerItem().setText(0, _translate("MainWindow", "Formulas"))
        self.FormulaTree.setSortingEnabled(True)
        self.FormulaTree.sortByColumn(0, Qt.AscendingOrder)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Eval), _translate("MainWindow", "Evaluate"))
        self.label_32.setText(_translate("MainWindow", "Number"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Pf), _translate("MainWindow", "Prime Factors"))
        self.ShellRun.setText(_translate("MainWindow", "Run"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Shell), _translate("MainWindow", "Shell"))
        self.menuCopy.setTitle(_translate("MainWindow", "Copy"))
        self.menuTab.setTitle(_translate("MainWindow", "Tab"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Web), _translate("MainWindow", "Web"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Formula), _translate("MainWindow", "Formulas"))
        self.actionCopy_exact_answer.setText(_translate("MainWindow", "Copy exact answer"))
        self.actionCopy_exact_answer.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionCopy_exact_answer.triggered.connect(self.copy_exact_ans)
        self.actionCopy_approximate_answer.setText(_translate("MainWindow", "Copy approximate answer"))
        self.actionCopy_approximate_answer.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionCopy_approximate_answer.triggered.connect(self.copy_approx_ans)
        self.actionNext_Tab.setText(_translate("MainWindow", "Next Tab"))
        self.actionNext_Tab.setShortcut(_translate("MainWindow", "Alt+Right"))
        self.actionNext_Tab.triggered.connect(self.next_tab)
        self.actionPrevious_Tab.setText(_translate("MainWindow", "Previous Tab"))
        self.actionPrevious_Tab.setShortcut(_translate("MainWindow", "Alt+Left"))
        self.actionPrevious_Tab.triggered.connect(self.previous_tab)
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionUse_Unicode.setText(_translate("MainWindow", "Use Unicode"))
        self.actionUse_Unicode.setShortcut(_translate("MainWindow", "Ctrl+U"))
        self.actionUse_Unicode.triggered.connect(self.toggle_unicode)
        self.actionLine_Wrap.setText(_translate("MainWindow", "Line Wrap"))
        self.actionLine_Wrap.setShortcut(_translate("Mainwindow", "Ctrl+L"))
        self.actionLine_Wrap.triggered.connect(self.toggle_line_wrap)
        self.actionScientific.setText(_translate("MainWindow", "Scientific Notation"))
        self.actionScientific.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionScientific.triggered.connect(self.toggle_use_scientific)
        self.actionAccuracy.setText(_translate("MainWindow", "Accuracy"))
        self.actionAccuracy.setShortcut(_translate("MainWindow", "Ctrl+Shift+A"))
        self.actionAccuracy.triggered.connect(self.change_accuracy)

        self.clearShell.setText(_translate("MainWindow", "Clear shell"))
        self.clearShell.setStatusTip(_translate("MainWIndow", "Ctrl+Shift+C"))
        self.clearShell.triggered.connect(self.clear_shell)
        self.menuWeb.setTitle(_translate("MainWindow", "Web"))

"""
if __name__ == "__main__":
    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("error catched!:")
        print("error message:\n", tb)
        QApplication.quit()
    sys.excepthook = excepthook
    e = Ui_MainWindow()
    print("Debug mode")
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
"""