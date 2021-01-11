from PyQt5.QtWidgets import QAction, QMainWindow, QTabWidget
class MainWindow(QMainWindow):
    action_accuracy: QAction
    action_copy_approximate_answer: QAction
    action_copy_exact_answer: QAction
    action_latex_fs: QAction
    action_linewrap: QAction
    action_next_tab: QAction
    action_previous_tab: QAction
    action_scientific_notation: QAction
    action_tab_list: QAction
    action_unicode: QAction
    action_use_latex: QAction
    tab_manager: QTabWidget
    testing: dict