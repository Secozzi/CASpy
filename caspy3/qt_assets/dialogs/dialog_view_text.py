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
