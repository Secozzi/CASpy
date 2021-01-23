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
    def __init__(self, parent=None):
        super(EditComboBox, self).__init__(parent)
        self._style = ProxyStyle(self.style())
        self.setStyle(self._style)
        self.editable_index = 99
        self.currentIndexChanged.connect(self.set_editable)

    def setEditableAfterIndex(self, index):
        self.editable_index = index

    def set_editable(self, index: int) -> None:
        if index >= self.editable_index:
            self.setEditable(True)
        else:
            self.setEditable(False)
        self.update()

    def paintEvent(self, event):
        painter = QStylePainter(self)
        painter.setPen(self.palette().color(QPalette.Text))

        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        opt.currentIcon = QIcon()
        opt.iconSize = QSize()

        painter.drawComplexControl(QStyle.CC_ComboBox, opt)
        painter.drawControl(QStyle.CE_ComboBoxLabel, opt)
