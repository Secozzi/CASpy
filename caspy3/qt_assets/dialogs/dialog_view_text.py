from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

import pkg_resources


class ViewText(QDialog):
    def __init__(self, text, parent=None):
        """
        Opens a QDialog and show text and a rendered latex text of exact answer

        :param text: string
            The text that is shown in the QTextBrowser

        The UI file is loaded and set the text to the QTextBrowser
        """
        super(ViewText, self).__init__(parent=None)
        loadUi(pkg_resources.resource_filename('caspy3', "qt_assets/dialogs/main_view_a.ui"), self)
        self.approx_text.setText(text)
        self.show()
