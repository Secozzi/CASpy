from PyQt5.QtWidgets import QDialog, QGridLayout
from PyQt5.QtGui import QIcon

from ..highlight import TextEdit
from .syntax_pars import PythonHighlighter


class StartCodeDialog(QDialog):
    def __init__(self, text: str, shell_widget: "ShellTab") -> None:
        super(StartCodeDialog, self).__init__()
        self.shell_widget = shell_widget

        self.setFixedSize(500, 400)
        self.setWindowTitle("CASPy - Edit Start Code")
        self.setWindowIcon(QIcon("assets/logo.png"))

        self.grid_layout = QGridLayout(self)
        self.text_dialog = TextEdit()

        self.text_dialog.document().setPlainText(text)
        self.text_dialog.setStyleSheet(
            "QPlainTextEdit{font: 8pt 'Courier New'; color: #383a42; background-color: #fafafa;}"
        )
        highlight = PythonHighlighter(self.text_dialog.document())

        self.grid_layout.addWidget(self.text_dialog, 0, 0, 1, 1)

        self.show()

    def closeEvent(self, event: "QtGui.QCloseEvent") -> None:
        text = self.text_dialog.toPlainText()
        self.shell_widget.update_start_code(text)
        event.accept()
