# PyQt5
from PyQt5.QtGui import QImage, QPixmap

# For LaTeX
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg

matplotlib.rcParams["mathtext.fontset"] = "cm"


def mathTex_to_QPixmap(
    mathTex: str,
    fs: int,
    fig: "matplotlib.pyplot.figure.Figure",
    color: str = "#000000",
) -> QPixmap:
    fig.clf()
    fig.patch.set_facecolor("none")
    fig.set_canvas(FigureCanvasAgg(fig))
    renderer = fig.canvas.get_renderer()

    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.patch.set_facecolor("none")
    t = ax.text(0, 0, mathTex, ha="left", va="bottom", fontsize=fs, color=color)

    fwidth, fheight = fig.get_size_inches()
    fig_bbox = fig.get_window_extent(renderer)

    text_bbox = t.get_window_extent(renderer)

    tight_fwidth = text_bbox.width * fwidth / fig_bbox.width
    tight_fheight = text_bbox.height * fheight / fig_bbox.height

    fig.set_size_inches(tight_fwidth, tight_fheight)

    buf, size = fig.canvas.print_to_buffer()
    qimage = QImage.rgbSwapped(QImage(buf, size[0], size[1], QImage.Format_ARGB32))
    qpixmap = QPixmap(qimage)

    return qpixmap
