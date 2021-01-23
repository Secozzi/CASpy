from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
)


class FieldsScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super(FieldsScrollArea, self).__init__(parent)

        self.scroll_grid = QGridLayout(self)

    def updateFields(self, data):
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
            qline.setFont(QFont("Courier New", 8))

            label.setToolTip(data[field]["tooltip"])
            qline.setToolTip(data[field]["tooltip"])

            self.scroll_grid.addWidget(label, i, 0)
            self.scroll_grid.addWidget(qline, i, 1)

        self.scroll_grid.itemAtPosition(0, 1).widget().setFocus()

    def get_data(self):
        out = []
        for i in range(self.scroll_grid.rowCount()):
            out.append(self.scroll_grid.itemAtPosition(i, 1).widget().text())
        return out
