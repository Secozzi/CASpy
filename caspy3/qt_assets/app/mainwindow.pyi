from PyQt5.QtWidgets import (
    QApplication,
    QAction,
    QActionGroup,
    QMainWindow,
    QTabWidget,
    QWidget
)
from PyQt5.QtGui import QCloseEvent, QFont
from PyQt5.QtCore import QSettings, QThreadPool
import typing as ty
class MainWindow(QMainWindow):
    action_accuracy: QAction = ...
    action_clash1: QAction = ...
    action_clash2: QAction = ...
    action_copy_approximate_answer: QAction = ...
    action_copy_exact_answer: QAction = ...
    action_latex_fs: QAction = ...
    action_linewrap: QAction = ...
    action_next_tab: QAction = ...
    action_previous_tab: QAction = ...
    action_scientific_notation: QAction = ...
    action_tab_list: QAction = ...
    action_unicode: QAction = ...
    action_use_latex: QAction = ...
    tab_manager: QTabWidget = ...
    tabs_font: QFont = ...

    approx_ans: str = ...
    clashes: dict = {}
    exact_ans: str = ...
    latex_ans: str = ...
    output_type: int = ...
    use_unicode: bool = ...
    line_wrap: bool = ...
    use_scientific: int = ...
    accuracy: int = ...
    use_latex: bool = ...
    latex_fs: int = ...
    settings: QSettings = ...
    qapp: QApplication = ...
    threadpool: QThreadPool = ...
    tab_list: ty.List[QWidget] = ...
    output_type_group: QActionGroup = ...

    def __init__(self) -> None: ...
    @staticmethod
    def get_resource(relative_path: str) -> str: ...
    @staticmethod
    def show_error_box(message: str) -> None: ...
    def read_settings(self) -> None: ...
    def write_settings(self) -> None: ...
    def init_ui(self) -> None: ...
    def init_menu(self) -> None: ...
    def change_output_type(self, action: QAction) -> None: ...
    def toggle_unicode(self, state: bool) -> None: ...
    def toggle_line_wrap(self, state: bool) -> None: ...
    def toggle_clash1(self, state: bool) -> None: ...
    def toggle_clash2(self, state: bool) -> None: ...
    def get_scientific_notation(self) -> int: ...
    def toggle_use_scientific(self, state: bool) -> None: ...
    def get_accuracy(self) -> int: ...
    def change_accuracy(self) -> None: ...
    def toggle_use_latex(self, state: bool) -> None: ...
    def get_latex_fs(self) -> int: ...
    def change_latex_fs(self) -> None: ...
    def copy_exact_ans(self) -> None: ...
    def copy_approx_ans(self) -> None: ...
    def goto_next_tab(self) -> None: ...
    def goto_previous_tab(self) -> None: ...
    def open_tab_list(self) -> None: ...
    def init_tabs(self) -> None: ...
    def init_shortcuts(self) -> None: ...
    def goto_tab(self, tab: int) -> None: ...
    def closeEvent(self, event: QCloseEvent) -> None: ...
    def update_clashes(self) -> None:
