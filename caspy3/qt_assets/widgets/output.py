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

from PyQt5.QtWidgets import QTextBrowser, QWidget
from PyQt5.QtGui import QCursor, QFocusEvent, QMouseEvent
from PyQt5.QtCore import Qt


class OutputWidget(QTextBrowser):
    def __init__(self, parent: QWidget, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.setFont(parent.font())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Select all text"""
        self.selectAll()

    def focusOutEvent(self, event: QFocusEvent) -> None:
        """Deselect all text"""
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)

    def set_cursor(self, cursor: Qt.CursorShape) -> None:
        self.viewport().setProperty("cursor", QCursor(cursor))
