import json

# Everything that my IDE says aren't used doesn't need to be imported, and I have no idea why but im keeping it here anyways.
# I'm not importing it from anywhere else, so it should raise an error but it doesn't.
from PyQt5.QtCore import (
    QCoreApplication,
    QEvent,
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
    QIcon,
    QRegExpValidator,
    QTextCursor
)

from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QApplication,
    QButtonGroup,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
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
from PyQt5.uic import loadUi

from Worker import CASWorker

class DerivativeTab(QWidget):

    display_name = "Derivative"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/derivative.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.DerivExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        """
        Add modifiers and if shift + enter or shift + return is pressed, run calc_deriv()
        """
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.calc_deriv()
                        return True

        return super(DerivativeTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.DerivPrev.clicked.connect(self.prev_deriv)
        self.DerivCalc.clicked.connect(self.calc_deriv)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.DerivOut.setText(self.main_window.exact_ans)
            self.DerivApprox.setText(str(self.main_window.approx_ans))

    def prev_deriv(self):
        self.WorkerCAS = CASWorker("prev_deriv", [
            self.DerivExp.toPlainText(),
            self.DerivVar.text(),
            self.DerivOrder.value(),
            self.DerivPoint.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def calc_deriv(self):
        self.WorkerCAS = CASWorker("calc_deriv", [
            self.DerivExp.toPlainText(),
            self.DerivVar.text(),
            self.DerivOrder.value(),
            self.DerivPoint.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class IntegralTab(QWidget):

    display_name = "Integral"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/integral.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.IntegExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.calc_integ()
                        return True

        return super(IntegralTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.IntegPrev.clicked.connect(self.prev_integ)
        self.IntegCalc.clicked.connect(self.calc_integ)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.IntegOut.setText(self.main_window.exact_ans)
            self.IntegApprox.setText(str(self.main_window.approx_ans))

    def prev_integ(self):
        self.WorkerCAS = CASWorker("prev_integ", [
            self.IntegExp.toPlainText(),
            self.IntegVar.text(),
            self.IntegOrder.value(),
            self.IntegPoint.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def calc_integ(self):
        self.WorkerCAS = CASWorker("calc_integ", [
            self.IntegExp.toPlainText(),
            self.IntegVar.text(),
            self.IntegLower.text(),
            self.IntegUpper.text(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class LimitTab(QWidget):

    display_name = "Limit"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/limit.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.LimExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.calc_limit()
                        return True

        return super(LimitTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.LimPrev.clicked.connect(self.prev_limit)
        self.LimCalc.clicked.connect(self.calc_limit)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.LimOut.setText(self.main_window.exact_ans)
            self.LimApprox.setText(str(self.main_window.approx_ans))

    def prev_limit(self):
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
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def calc_limit(self):
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
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class SimplifyTab(QWidget):
    display_name = "Simplify"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/simplify.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.SimpExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.simp_exp()
                        return True

        return super(SimplifyTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.SimpPrev.clicked.connect(self.prev_simp_exp)
        self.SimpCalc.clicked.connect(self.simp_exp)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.SimpOut.setText(self.main_window.exact_ans)

    def prev_simp_exp(self):
        self.WorkerCAS = CASWorker("prev_simp_eq", [
            self.SimpExp.toPlainText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def simp_exp(self):
        self.WorkerCAS = CASWorker("prev_simp_eq", [
            self.SimpExp.toPlainText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class ExpandTab(QWidget):
    display_name = "Expand"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/expand.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.ExpExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.exp_exp()
                        return True

        return super(ExpandTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.ExpPrev.clicked.connect(self.prev_exp_exp)
        self.ExpCalc.clicked.connect(self.exp_exp)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.ExpOut.setText(self.main_window.exact_ans)

    def prev_exp_exp(self):
        self.WorkerCAS = CASWorker("prev_exp_eq", [
            self.ExpExp.toPlainText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def exp_exp(self):
        self.WorkerCAS = CASWorker("prev_exp_eq", [
            self.ExpExp.toPlainText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class EvaluateTab(QWidget):
    display_name = "Evaluate"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/evaluate.ui", self)
        self.main_window = main_window
        self.install_event_filters()
        self.init_bindings()

    def install_event_filters(self):
        self.EvalExp.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.eval_exp()
                        return True

        return super(EvaluateTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.EvalPrev.clicked.connect(self.prev_eval_exp)
        self.EvalCalc.clicked.connect(self.eval_exp)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.EvalOut.setText(self.main_window.exact_ans)
            self.EvalApprox.setText(self.main_window.approx_ans)

    def prev_eval_exp(self):
        self.WorkerCAS = CASWorker("prev_eval_exp", [
            self.EvalExp.toPlainText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def eval_exp(self):
        self.WorkerCAS = CASWorker("eval_exp", [
            self.EvalExp.toPlainText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class PfTab(QWidget):
    display_name = "Prime Factors"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/pf.ui", self)
        self.main_window = main_window
        self.init_bindings()

    def init_bindings(self):
        self.PfCalc.clicked.connect(self.calc_pf)

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.PfOut.setText(self.main_window.exact_ans)
            self.PfApprox.setText(self.main_window.approx_ans)

    def calc_pf(self):
        self.WorkerCAS = CASWorker("calc_pf", [self.PfInput.value()])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

class WebTab(QWidget):

    display_name = "Web"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/web.ui", self)
        self.main_window = main_window
        self.init_web_menu()
        self.web.load(QUrl("https://www.desmos.com/calculator"))

    def init_web_menu(self):
        self.menuWeb = self.main_window.menubar.addMenu("Web")
        self.set_actions()

    def set_actions(self):
        self.menuWeb.clear()
        self.web_list = self.main_window.json_file[2]
        self.web_menu_action_group = QActionGroup(self.menuWeb)

        for i in self.web_list:
            for key in i:
                webAction = QAction(key, self.menuWeb, checkable=True)
                if webAction.text() == "Desmos":
                    webAction.setChecked(True)
                self.menuWeb.addAction(webAction)
                self.web_menu_action_group.addAction(webAction)

        self.web_menu_action_group.setExclusive(True)

        self.add_website = QAction("Add Website", self)
        self.remove_website = QAction("Remove Website", self)
        self.menuWeb.addSeparator()
        self.menuWeb.addAction(self.add_website)
        self.menuWeb.addAction(self.remove_website)
        self.add_website.triggered.connect(self.add_website_window)
        self.remove_website.triggered.connect(self.remove_website_window)

        self.web_menu_action_group.triggered.connect(self.updateWeb)

    def updateWeb(self, action):
        """
        Updates web tab when user selects new website.

        Parameters
        ---------------
        action: QAction
            action.text() shows text of selected radiobutton
        """
        for i in self.web_list:
            for key in i:
                if action.text() == key:
                    self.web.load(QUrl(i[key]))

    def add_website_window(self):
        self.website_window_add = Add_Website(self.main_window, self)

    def remove_website_window(self):
        self.website_window_remove = Remove_Website(self.main_window, self)

class Add_Website(QDialog):
    def __init__(self, main_window, web_tab ,parent=None):
        super(Add_Website, self).__init__(parent=None)
        self.main_window = main_window
        self.web_list = self.main_window.json_file[2]
        self.web_tab = web_tab

        loadUi("qt_assets/tabs/web_add.ui", self)

        self.add_button_box.accepted.connect(self.add_website)
        self.add_button_box.rejected.connect(self.close)

        self.show()

    def add_website(self):
        self.main_window.json_file[2].append({self.display_line.text(): self.url_line.text()})

        with open("assets/formulas.json", "w", encoding="utf-8") as json_f:
            json.dump(self.main_window.json_file, json_f, ensure_ascii=False, indent=4, sort_keys=True)

        # Reload json file reading
        self.main_window.load_json()
        self.web_tab.set_actions()

        self.close()

class Remove_Website(QDialog):
    def __init__(self, main_window, web_tab, parent=None):
        super(Remove_Website, self).__init__(parent=None)
        self.main_window = main_window
        self.web_list = self.main_window.json_file[2]
        self.web_tab = web_tab

        loadUi("qt_assets/tabs/web_remove.ui", self)
        for i in self.web_list:
            self.remove_combo.addItem(list(i.keys())[0])

        self.remove_button_box.accepted.connect(self.remove_website)
        self.remove_button_box.rejected.connect(self.close)

        self.show()

    def remove_website(self):
        """
        Gets selected item, removes it from the list of websites and writes it to the file.
        """
        selected_key = self.web_list[self.remove_combo.currentIndex()]
        self.main_window.json_file[2].remove(selected_key)
        with open("assets/formulas.json", "w", encoding="utf-8") as json_f:
            json.dump(self.main_window.json_file, json_f, ensure_ascii=False, indent=4, sort_keys=True)

        # Reload json file reading
        self.main_window.load_json()
        self.web_tab.set_actions()

        self.close()


class FormulaTab(QWidget):

    from sympy import Symbol, S
    from sympy.abc import _clash1

    display_name = "Formulas"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/formulas.ui", self)
        self.init_ui()
        self.main_window = main_window

        self.install_event_filter()
        self.init_bindings()
        self.add_formulas()

    def init_ui(self):
        self.FormulaTree.sortByColumn(0, Qt.AscendingOrder)
        self.grid_scroll_area = QGridLayout(self.FormulaScrollArea)
        self.grid_scroll_area.setObjectName("grid_scroll_area")

    def install_event_filter(self):
        self.FormulaScrollArea.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.calc_formula()
                        return True

        return super(FormulaTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.FormulaTree.itemDoubleClicked.connect(self.formula_tree_selected)
        self.FormulaPreview.clicked.connect(self.prev_formula)
        self.FormulaCalculate.clicked.connect(self.calc_formula)

    def add_formulas(self):
        self.formula_info_dict = self.main_window.json_file[0]
        self.formula_tree_data = self.main_window.json_file[1]

        for branch in self.formula_tree_data:
            parent = QTreeWidgetItem(self.FormulaTree)
            branch_name = str(list(branch.keys())[0])
            parent.setText(0, branch_name)

            for sub_branch in list(branch[branch_name].keys()):
                child = QTreeWidgetItem(parent)
                child.setText(0, sub_branch)

                for formula in branch[branch_name][sub_branch]:
                    formula_child = QTreeWidgetItem(child)
                    formula_child.setText(0, formula)

        #for branch in self.formula_tree_data:
        #    parent = QTreeWidgetItem(self.FormulaTree)
        #    parent.setText(0, str(branch[0]))
        #
        #    for sub_branch in branch[1]:
        #        child = QTreeWidgetItem(parent)
        #        child.setText(0, str(sub_branch[0]))
        #
        #        for formula in sub_branch[1]:
        #            formula_child = QTreeWidgetItem(child)
        #            formula_child.setText(0, formula[0])

    def formula_tree_selected(self):
        """
        Retrieves formula and information about formula that user double clicked.
        Splits equation into left side of equals symbol and right side.
        Uses _i as imaginary unit instead of I and removes other similar functions/variables so they can be used as variables in formula.
        """

        get_selected = self.FormulaTree.selectedItems()
        if get_selected:
            base_node = get_selected[0]
            self.selected_tree_item = base_node.text(0)
            if "=" in self.selected_tree_item:
                expr = self.selected_tree_item.split("=")
                expr = list(map(lambda x: x.replace("_i", "(sqrt(-1))"), expr))
                self.formula_symbols_list = [str(i) for i in list(self.S(expr[0], locals=self._clash1).atoms(self.Symbol))]
                self.formula_symbols_list.extend((str(i) for i in list(self.S(expr[1], locals=self._clash1).atoms(self.Symbol))))
                self.formula_symbols_list = list(set(self.formula_symbols_list))
                self.formula_symbols_list.sort()

                self.formula_update_vars()
                self.formula_info = self.formula_get_info(self.selected_tree_item, self.formula_tree_data)
                print(self.formula_info)
                #self.formula_set_tool_tip()

    def formula_update_vars(self):
        for i in reversed(range(self.grid_scroll_area.count())):
            self.grid_scroll_area.itemAt(i).widget().setParent(None)
        self.formula_label_names = self.formula_symbols_list
        self.formula_label_pos = [[i, 0] for i in range(len(self.formula_label_names))]
        self.formula_line_pos = [[i, 1] for i in range(len(self.formula_label_names))]
        for self.formula_name_label, formula_pos_label, formula_pos_line in zip(self.formula_label_names, self.formula_label_pos, self.formula_line_pos):
            self.formula_label = QLabel(self.FormulaScrollArea)
            self.formula_label.setText(self.formula_name_label)
            self.formula_label.setObjectName(self.formula_name_label + "line")
            self.grid_scroll_area.addWidget(self.formula_label, *formula_pos_label)
            self.formula_QLine = QLineEdit(self.FormulaScrollArea)
            self.formula_QLine.setObjectName(self.formula_name_label + "line")
            self.grid_scroll_area.addWidget(self.formula_QLine, *formula_pos_line)

    def formula_set_tool_tip(self):
        _translate = QCoreApplication.translate

        lines = []
        for name in self.formula_label_names:
            lines.append([self.FormulaScrollArea.findChild(QLineEdit, str(name) + "line"), name])

        info_dict_keys = list(self.formula_info_dict.keys())


        print(self.formula_info)

    # def formula_set_tool_tip(self):
    #     """
    #     Sets ToolTip to the info given by the json file.
    #     """
    #     _translate = QCoreApplication.translate
    #     lines = [[self.FormulaScrollArea.findChild(QLineEdit, str(i) + "line"), i] for i in self.formula_label_names]
    #     labels = [[self.FormulaScrollArea.findChild(QLabel, str(i) + "line"), i] for i in self.formula_label_names]
    #     for line, label in zip(lines, labels):
    #         for i in self.formula_info:
    #             if i in list(self.formula_info_dict.keys()):
    #                 FormulaInfoList = self.formula_info_dict[i].split("|")
    #             else:
    #                 FormulaInfoList = [i, "No info", "No info"]
    #
    #             if FormulaInfoList[0] == line[1]:
    #                 # This is in Swedish, change 'mäts i' to 'measured in' for english
    #                 line[0].setToolTip(_translate("MainWindow", f"{FormulaInfoList[1]}, mäts i {FormulaInfoList[2]}"))
    #                 label[0].setToolTip(_translate("MainWindow", f"{FormulaInfoList[1]}, mäts i {FormulaInfoList[2]}"))
    #             elif FormulaInfoList[0].split(";")[0] == line[1]:
    #                 line[0].setToolTip(_translate("MainWindow", f"{FormulaInfoList[1]}, mäts i {FormulaInfoList[2]}"))
    #                 label[0].setToolTip(_translate("MainWindow", f"{FormulaInfoList[1]}, mäts i {FormulaInfoList[2]}"))
    #                 line[0].setText(FormulaInfoList[0].split(";")[1])

    def formula_get_info(self, text, data):
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
            branch_name = str(list(branch.keys())[0])
            for sub_branch in list(branch[branch_name].keys()):
                if text in list(branch[branch_name][sub_branch].keys()):
                    return branch[branch_name][sub_branch][text]

        #for branch in data:
        #    for subBranch in branch[1]:
        #        for formula in subBranch[1]:
        #            if formula[0] == text:
        #                return formula[1]

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.FormulaExact.setText(str(self.main_window.exact_ans))
            self.FormulaApprox.setText(str(self.main_window.approx_ans))

    def prev_formula(self):
        try:
            lines = [[self.FormulaScrollArea.findChild(QLineEdit, str(i) + "line"), i] for i in self.formula_label_names]
        except:
            self.main_window.show_error_box("Error: select a formula")

        values_string = self.selected_tree_item.split("=")

        self.WorkerCAS = CASWorker("prev_formula", [
            lines,
            values_string,
            self.FormulaExact.toPlainText(),
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)

    def calc_formula(self):
        if self.FormulaSolveSolve.isChecked():
            solve_type = 2
        if self.FormulaSolveSolveSet.isChecked():
            solve_type = 1

        try:
            lines = [[self.FormulaScrollArea.findChild(QLineEdit, str(i) + "line"), i] for i in self.formula_label_names]
        except:
            self.main_window.show_error_box("Error: select a formula")

        values_string = self.selected_tree_item.split("=")

        self.WorkerCAS = CASWorker("calc_formula", [
            lines,
            values_string,
            solve_type,
            self.main_window.output_type,
            self.main_window.use_unicode,
            self.main_window.line_wrap,
            self.main_window.use_scientific,
            self.main_window.accuracy
        ])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)


class ShellTab(QWidget):
    display_name = "Shell"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/shell.ui", self)
        self.main_window = main_window
        self.current_code = self.consoleIn.toPlainText()
        self.previous_code_list = []

        self.install_event_filter()
        self.init_bindings()
        self.add_to_menu()

    def install_event_filter(self):
        self.consoleIn.installEventFilter(self)

    def eventFilter(self, obj, event):
        QModifiers = QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
            modifiers.append('shift')

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if modifiers:
                    if modifiers[0] == "shift":
                        self.consoleIn.appendPlainText("... ")
                        return True
                else:
                    self.execute_code()
                    return True

        return super(ShellTab, self).eventFilter(obj, event)

    def init_bindings(self):
        self.ShellRun.clicked.connect(self.execute_code)

    def add_to_menu(self):
        _translate = QCoreApplication.translate
        self.clear_shell_action = QAction("Clear Shell", self)
        self.clear_shell_action.setShortcut(_translate("MainWindow", "Ctrl+Shift+C"))
        self.main_window.menuSettings.addSeparator()
        self.main_window.menuSettings.addAction(self.clear_shell_action)
        self.clear_shell_action.triggered.connect(self.clear_shell)

    def clear_shell(self):
        # Clears shell of written text, and previously initialized variables and functions.
        self.previous_code_list = []
        code = "This is a very simple shell using 'exec' commands, so it has some limitations. Every variable declared and function defined will be saved until the program is closed or when the 'clear commands' button in the menubar is pressed. It will automatically output to the shell, but it can't use 'print' commands. To copy output, press the 'copy exact answer' in the menubar.\nTheses commands were executed:\nfrom __future__ import division\n\nfrom sympy import *\nfrom sympy.parsing.sympy_parser import parse_expr\nfrom sympy.abc import _clash1\n\nimport math as m\nimport cmath as cm\n\nx, y, z, t = symbols('x y z t')\nk, m, n = symbols('k m n', integer=True)\nf, g, h = symbols('f g h', cls=Function)\n\n>>> "
        self.consoleIn.clear()
        self.consoleIn.appendPlainText(code)
        self.current_code = code

    def stop_thread(self):
        pass

    def update_ui(self, input_dict):
        if "list" in list(input_dict.keys()):
            self.previous_code_list = input_dict["list"]
        else:
            self.previous_code_list = []

        first_key = list(input_dict.keys())[0]
        if first_key == "error":
            self.main_window.show_error_box(input_dict[first_key][0])
        else:
            self.main_window.exact_ans = str(input_dict[first_key][0])
            self.main_window.approx_ans = input_dict[first_key][1]

            self.consoleIn.insertPlainText(self.main_window.exact_ans + "\n>>> ")
            self.consoleIn.moveCursor(QTextCursor.End)
            self.current_code = self.consoleIn.toPlainText()

    def execute_code(self):
        self.new_code = self.consoleIn.toPlainText().replace(self.current_code, "")
        self.consoleIn.moveCursor(QTextCursor.End)

        self.WorkerCAS = CASWorker("execute_code", [self.new_code, self.previous_code_list])
        self.WorkerCAS.signals.output.connect(self.update_ui)
        self.WorkerCAS.signals.finished.connect(self.stop_thread)

        self.main_window.threadpool.start(self.WorkerCAS)