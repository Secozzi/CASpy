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
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QSplitter,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Third party
from pkg_resources import resource_filename

# Relative
from caspy3.qt_assets.widgets.focus_line import FocusLine


class SplitterEditor(QWidget):
    def __init__(self, parent) -> None:
        super(SplitterEditor, self).__init__()
        self.parent = parent
        self.resize(600, 400)
        self.setWindowTitle(f"{self.parent.display_name} QSplitter Editor")
        self.setWindowIcon(QIcon(resource_filename("caspy3", "images/logo.png")))
        self.setWindowModality(Qt.ApplicationModal)

        self.v_layout = QVBoxLayout(self)

        # Setup Splitter
        self.preview_splitter = QSplitter(self)
        self.preview_splitter.splitterMoved.connect(lambda x, y: self.update_splitter())

        # Setup combobox
        self.splitter_combo = QComboBox(self)
        self.splitter_combo.currentIndexChanged.connect(self.update_splitter_area)
        for splitter in self.parent.splitters:
            self.splitter_combo.addItem(splitter.objectName())

        #self.update_splitter_area(0)

        # Setup buttons
        self.button_layout = QHBoxLayout()
        self.preview = QPushButton("Preview")
        self.preview.clicked.connect(self.preview_split)
        self.ok = QPushButton("Ok")
        self.cancel = QPushButton("Cancel")
        self.button_layout.addWidget(self.preview)
        self.button_layout.addWidget(self.ok)
        self.button_layout.addWidget(self.cancel)

        self.v_layout.addWidget(self.splitter_combo)
        self.v_layout.addWidget(self.preview_splitter)
        self.v_layout.addLayout(self.button_layout)

        self.setLayout(self.v_layout)

    def update_splitter_area(self, index) -> None:
        for i in reversed(range(self.preview_splitter.count())):
            self.preview_splitter.widget(i).setParent(None)

        splitter = self.parent.splitters[index]
        for i in range(splitter.count()):
            lineedit = FocusLine(self)
            lineedit.setInputMask("99.99%")
            self.preview_splitter.addWidget(lineedit)

        self.update_splitter()
        self.preview_splitter.setOrientation(splitter.orientation())

    def resizeEvent(self, event) -> None:
        self.update_splitter()

    def get_data(self) -> list:
        per_list = []
        for i in range(self.preview_splitter.count()):
            per_list.append(
                float(
                    f'0.{self.preview_splitter.widget(i).text().replace(".", "").replace("%", "")}'
                )
            )
        return per_list

    def preview_split(self):
        per_list = []
        for i in range(self.preview_splitter.count()):
            per_list.append(
                float(
                    f'0.{self.preview_splitter.widget(i).text().replace(".", "").replace("%", "")}'
                )
            )

        if self.preview_splitter.orientation() == Qt.Horizontal:
           _max = self.preview_splitter.width()
        else:
           _max = self.preview_splitter.height()
        _max -= self.preview_splitter.handleWidth() * (self.preview_splitter.count() - 1)
        self.preview_splitter.setSizes([int(i*_max) for i in per_list])

    def update_splitter(self):
        if self.preview_splitter.orientation() == Qt.Horizontal:
            _max = self.preview_splitter.width()
        else:
            _max = self.preview_splitter.height()
        _max -= self.preview_splitter.handleWidth() * (
            self.preview_splitter.count() - 1
        )
        _sizes = self.preview_splitter.sizes()
        for j in range(self.preview_splitter.count()):
            self.preview_splitter.widget(j).setText(f"{(_sizes[j]/_max * 100):.2f}%")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    window = SplitterEditor("s")
    window.resize(600, 400)
    window.show()
    window.update_splitter()

    app.exec_()
