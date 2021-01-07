from PyQt5.QtWidgets import (
    QApplication,
    QColorDialog,
    QDialog,
    QFileDialog,
    QLabel,
    QMenu,
)
from PyQt5.QtCore import QMimeData, Qt, QTemporaryDir, QUrl
from PyQt5.QtGui import QDrag, QPalette, QPixmapCache
from PyQt5.uic import loadUi

from sympy.parsing import parse_expr
from sympy import Eq, latex
from pathlib import Path
import pkg_resources
import string
import random

from .latex import mathTex_to_QPixmap


class SaveDialog(QDialog):
    def __init__(self, drag_label, parent=None) -> None:
        super(SaveDialog, self).__init__(parent=parent)
        self.drag_label = drag_label

        loadUi(
            pkg_resources.resource_filename(
                "caspy3", "qt_assets/dialogs/save_dialog.ui"
            ),
            self,
        )
        self.fs_spinbox.setValue(self.drag_label.parent.main_window.latex_fs)

        self.color_hex = "#000000"
        self.update_color(self.color_hex)
        self.render_label()

        # Bindings
        self.pick_color.clicked.connect(self.get_color)
        self.preview.clicked.connect(self.render_label)
        self.cancel.clicked.connect(self.close)
        self.save.clicked.connect(
            lambda: self.drag_label.save_image(self.pixmap)
        )

        self.show()

    def get_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.update_color(color.name())

    def update_color(self, color: str) -> None:
        self.color_preview.setStyleSheet(f"QLabel {{background-color:{color};}}")
        self.color_hex_line.setText(color)
        self.color_hex = color

    def render_label(self):
        formula = self.drag_label.formula
        self.pixmap = self.drag_label.get_latex_pixmap(
            formula=formula, fs=self.fs_spinbox.value(), color=self.color_hex
        )
        self.preview_pixmap.setPhoto(pixmap=self.pixmap)


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
        self.customContextMenuRequested.connect(
            lambda pos: self.customMenuEvent(self, pos)
        )

    def customMenuEvent(self, child: "DragLabel", eventPosition: "QPoint") -> None:
        context_menu = QMenu(self)
        copy = context_menu.addAction("Copy")
        copy_fs = context_menu.addAction("Copy with font-size")
        context_menu.addSeparator()
        save = context_menu.addAction("Save image")

        action = context_menu.exec_(child.mapToGlobal(eventPosition))

        if action == copy:
            QApplication.clipboard().setPixmap(child.pixmap())

        elif action == copy_fs:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            QApplication.clipboard().setPixmap(self.get_latex_pixmap(self.formula))
            QApplication.restoreOverrideCursor()

        elif action == save:
            self._preview = SaveDialog(self)

    def save_image(self, qpixmap):
        formula = self.formula.translate(str.maketrans("", "", '<>:"/\\|?*'))
        dialog = QFileDialog()
        fileName, _ = dialog.getSaveFileName(
            self,
            "Save Image",
            str(Path.home()) + f"/{formula}.png",
            "Images (*.png)",
            options=QFileDialog.DontUseNativeDialog,
        )
        if fileName:
            qpixmap.save(fileName, "PNG")
            self._preview.close()
        else:
            self._preview.show()

    def get_latex_pixmap(self, formula, fs=None, color=None):
        expr = formula.split("=")

        left = parse_expr(expr[0], evaluate=False)
        right = parse_expr(expr[1], evaluate=False)

        if not fs:
            fs = self.parent.main_window.latex_fs

        pixmap = mathTex_to_QPixmap(
            f"${latex(Eq(left, right))}$", fs, fig=self.parent.fig, color=color
        )
        return pixmap

    def mouseMoveEvent(self, ev: "QtGui.QMouseEvent") -> None:
        if ev.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mimeData = QMimeData()
            QApplication.setOverrideCursor(Qt.WaitCursor)

            rand = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
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
