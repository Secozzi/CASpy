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

# Third party
from pkg_resources import resource_filename

# PyQt5
from PyQt5.QtWidgets import (
    QComboBox,
    QProxyStyle,
    QStyle,
    QStyleOptionComboBox,
    QStyleOptionComplex,
    QStylePainter,
    QWidget,
)
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import QRect, QSize


class ProxyStyle(QProxyStyle):
    def subControlRect(
        self,
        control: QStyle.ComplexControl,
        option: QStyleOptionComplex,
        subControl: QStyle.SubControl,
        widget: QWidget = None,
    ) -> QRect:
        r = super().subControlRect(control, option, subControl, widget)
        if control == QStyle.CC_ComboBox and subControl == QStyle.SC_ComboBoxEditField:
            if widget.isEditable():
                widget.lineEdit().setGeometry(r)
        return r


class EditComboBox(QComboBox):
    """
    A QComboBox derived widget with the ability
    to add QIcons to provide the user whether the
    item is editable or not.

    Add an item via the `addItemEdit` method and then call the
    `setEditableAfterIndex` function with given index.
    """
    def __init__(self, parent=None) -> None:
        super(EditComboBox, self).__init__(parent)
        self.edit_ico = QIcon(resource_filename("caspy3", "images/edit.png"))
        self.empty_ico = QIcon(resource_filename("caspy3", "images/empty.png"))
        self._style = ProxyStyle(self.style())
        self.setStyle(self._style)
        self.editable_index = 99
        self.currentIndexChanged.connect(self._set_editable)

    def setEditableAfterIndex(self, index: int) -> None:
        """
        Sets the item to be editable if its index is after the
        index given to this function.
        """
        self.editable_index = index

    def _set_editable(self, index: int) -> None:
        if index >= self.editable_index:
            self.setEditable(True)
        else:
            self.setEditable(False)
        self.update()

    def paintEvent(self, event) -> None:
        painter = QStylePainter(self)
        painter.setPen(self.palette().color(QPalette.Text))

        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        opt.currentIcon = QIcon()
        opt.iconSize = QSize()

        painter.drawComplexControl(QStyle.CC_ComboBox, opt)
        painter.drawControl(QStyle.CE_ComboBoxLabel, opt)

    def addItemEdit(self, text: str, editable: bool = False) -> None:
        """Add an item"""
        if editable:
            self.addItem(self.edit_ico, text)
        else:
            self.addItem(self.empty_ico, text)
