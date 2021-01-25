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

# Standard library
import typing as ty

# PyQt5
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
)


class FieldsScrollArea(QScrollArea):
    def __init__(self, parent=None) -> None:
        super(FieldsScrollArea, self).__init__(parent)

        self.scroll_grid = QGridLayout(self)

    def updateFields(self, data: dict) -> None:
        for i in reversed(range(self.scroll_grid.count())):
            self.scroll_grid.itemAt(i).widget().setParent(None)

        for i, field in enumerate(data["fields"]):
            label = QLabel(self)
            label.setText(data[field]["label"])
            label.setObjectName(field + "label")
            label.setFont(QFont("Courier New", 8))

            qline = QLineEdit(self)
            qline.setFixedHeight(30)
            qline.setObjectName(field + "line")
            qline.setText(data[field]["default"])
            qline.setFont(QFont("Courier New", 8))

            label.setToolTip(data[field]["tooltip"])
            qline.setToolTip(data[field]["tooltip"])

            self.scroll_grid.addWidget(label, i, 0)
            self.scroll_grid.addWidget(qline, i, 1)

        self.scroll_grid.itemAtPosition(0, 1).widget().setFocus()

    def get_data(self) -> ty.List[str]:
        out = []
        for i in range(self.scroll_grid.rowCount()):
            out.append(self.scroll_grid.itemAtPosition(i, 1).widget().text())
        return out
