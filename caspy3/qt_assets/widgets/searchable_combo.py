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

# PyQt5
from PyQt5.QtWidgets import QComboBox, QCompleter, QLineEdit
from PyQt5.QtCore import Qt


class FocusLine(QLineEdit):
    def __init__(self, parent=None) -> None:
        super(FocusLine, self).__init__(parent)

    def mousePressEvent(self, a0) -> None:
        self.selectAll()


class SearchableComboBox(QComboBox):
    """
    A QComboBox derived widget that can be searched through.
    """
    def __init__(self, parent=None) -> None:
        super(SearchableComboBox, self).__init__(parent)

        self.setLineEdit(FocusLine())
        self.setEditable(True)
        self.setMaxVisibleItems(12)
        self.completer().setMaxVisibleItems(12)
        self.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.completer().setFilterMode(Qt.MatchContains)
        self.setInsertPolicy(QComboBox.NoInsert)
