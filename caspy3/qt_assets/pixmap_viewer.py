from PyQt5.QtWidgets import QFrame, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import pyqtSignal, QPoint, QRectF, Qt
from PyQt5.QtGui import QPixmap
import typing as ty


class PhotoViewer(QGraphicsView):
    """
    Copied from
    https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
    """

    photoClicked = pyqtSignal(QPoint)

    def __init__(self, parent: "QLabel") -> None:
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._photo.setTransformationMode(Qt.SmoothTransformation)
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)

    def hasPhoto(self) -> bool:
        return not self._empty

    def fitInView(self, scale: bool=True) -> None:
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(
                    viewrect.width() / scenerect.width(),
                    viewrect.height() / scenerect.height(),
                )
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap: ty.Union[QPixmap, None]=None) -> None:
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QGraphicsView.NoDrag)
            self._photo.setPixmap(QPixmap())
        self.fitInView()

    def showEvent(self, event: "QtGui.QShowEvent") -> None:
        if not event.spontaneous():
            self.fitInView()

    def resizeEvent(self, event: "QtGui.QResizeEvent") -> None:
        self.fitInView()

    def swheelEvent(self, event: "QtGui.QWheelEvent") -> None:
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self) -> None:
        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.setDragMode(QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event: "QtGui.QMouseEvent") -> None:
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)
