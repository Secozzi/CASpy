from PyQt5.QtWidgets import QApplication, QLabel, QMenu
from PyQt5.QtCore import QMimeData, Qt, QTemporaryDir, QUrl
from PyQt5.QtGui import QDrag, QPixmapCache

from sympy.parsing import parse_expr
from sympy import Eq, latex
import string
import random

from .latex import mathTex_to_QPixmap


class DragLabel(QLabel):
    """
    Custom QLabel class that allows for draggable QImages.
    Creates a LaTeX based on formula and MainWindow's LaTeX resolution,
    then saves it into a temporary directory and loads the path into
    QMimeData, and then the QDrag copies it.
    """
    def __init__(self, parent, formula):
        super(DragLabel, self).__init__(parent)
        self.parent = parent
        self.formula = formula
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect (lambda pos: self.customMenuEvent(self, pos))

    def customMenuEvent(self, child, eventPosition):
        contextMenu = QMenu(self)
        copy = contextMenu.addAction("Copy")
        copy_fs = contextMenu.addAction("Copy with font-size")
        save = contextMenu.addAction("Save image")

        action = contextMenu.exec_(child.mapToGlobal(eventPosition))

        if action == copy:
            QApplication.clipboard().setPixmap(child.pixmap())
        elif action == copy_fs:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            QApplication.clipboard().setPixmap(self.get_latex_pixmap(self.formula))
            QApplication.restoreOverrideCursor()

    def get_latex_pixmap(self, formula):
        expr = formula.split("=")

        left = parse_expr(expr[0], evaluate=False)
        right = parse_expr(expr[1], evaluate=False)

        pixmap = mathTex_to_QPixmap(
            f"${latex(Eq(left, right))}$",
            self.parent.main_window.latex_fs,
            fig=self.parent.fig,
        )
        return pixmap

    def mouseMoveEvent(self, ev: "QtGui.QMouseEvent") -> None:
        if ev.button() == Qt.LeftButton and self.geometry().contains(ev.pos()):
            drag = QDrag(self)
            mimeData = QMimeData()
            QApplication.setOverrideCursor(Qt.WaitCursor)

            rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            td = QTemporaryDir()
            path = td.path() + rand + ".png"

            pixmap = self.get_latex_pixmap(self.formula)
            qimage = pixmap.toImage()
            qimage.save(path, "PNG")

            mimeData.setImageData(qimage)
            mimeData.setUrls([QUrl.fromLocalFile(path)])
            drag.setMimeData(mimeData)

            drag.setPixmap(pixmap.scaledToHeight(40, Qt.SmoothTransformation))
            QApplication.restoreOverrideCursor()
            drag.exec_(Qt.CopyAction)
            ev.accept()
            QPixmapCache.clear()
        else:
            ev.ignore()