from PyQt5.QtGui import QImage, QPixmap, QPixmapCache
from PyQt5.QtWidgets import QTreeWidgetItem, QWidget, QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QSize
from PyQt5.uic import loadUi

import matplotlib
import matplotlib.pyplot as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg
from sympy.printing import latex
from sympy.parsing import parse_expr
from sympy import Eq

matplotlib.rcParams["mathtext.fontset"] = "cm"

data = [
    {
        "A": "A|Area|m^2 (kvadratmeter)",
        "cl": "c;299792458|Ljusets hastighet|m/s",
        "m_ga_A": "A|Arean på en geometrisk figur|a.e (areaenheter)",
        "m_ga_b": "b|Basen på en geometrisk figur|l.e (längdenheter)",
        "m_ga_bå": "b|Båge på en cirkelsektor|l.e (längdenheter)",
        "m_ga_h": "h|Höjden på en geometrisk figur|l.e (längdenheter)",
        "m_ga_a": "a|En sida på en geometrisk figur|l.e (längdenheter)",
        "m_ga_ba": "b|En sida på en geometrisk figur|l.e (längdenheter)",
        "m_ga_c": "c|En sida på en geometrisk figur|l.e (längdenheter)",
        "m_ga_d1": "d1|En diagonal på en geometrisk figur|l.e (längdenheter)",
        "m_ga_d2": "d2|En diagonal på en geometrisk figur|l.e (längdenheter)",
        "m_ga_d": "d|Diametern på en geometrisk figur|l.e (längdenheter)",
        "m_ga_o": "o|Omkretsen på en geometrisk figur|l.e (längdenheter)",
        "m_ga_r": "r|Radien på en geometrisk figur|l.e (längdenheter)",
        "m_ga_v": "v|Medelpunktsvinkeln i radianer|rad (radianer)",
        "m_gv_a": "a|en sida på en geometrisk figur|l.e (längdenheter)",
        "m_gv_b": "b|en sida på en geometrisk figur|l.e (längdenheter)",
        "m_gv_B": "B|Basarea|a.e (areaenheter)",
        "m_gv_c": "c|En sida på en geometrisk figur|l.e (längdenheter)",
        "m_gv_h": "h|Höjden på en geometrisk figur|l.e (längdenheter)",
        "m_gv_r": "r|Radien på en geometrisk figur|l.e (längdenheter)",
        "m_gv_V": "V|Volymen på en geometrisk figur|v.e (volymenheter)",
        "f_m_A": "A|Area|m^2 (Kvadratmeter)",
        "f_m_a": "a|acceleration|m/s^2 (Meter per sekundkvadrat)",
        "f_m_E": "E|Energi|J (Nm)(Joule)",
        "f_m_Ek": "E|Rörelseenergi|J (Nm)(Joule)",
        "f_m_Ep": "E|Lägesenergi|J (Nm)(Joule)",
        "f_m_F": "F|Kraft|N (Newton)",
        "f_m_G": "G;6.674*10**(-11)|Allmäna Gravitationskonstanten|Nm^2/kg^2 (Kvadratnewtonmeter per kvadratkilo)",
        "f_m_g": "g;9.81|Tyngdaccelerationen|m/s^2 (Meter per sekundkvadrat)",
        "f_m_I": "I|Impuls|Ns (Newtonsekund)",
        "f_m_k": "k|Fjäderkonstant|N/m (Newton per meter)",
        "f_m_M": "M|Kraftmoment|Nm (Newtonmeter)",
        "f_m_m": "m|Massa|kg (Kilogram)",
        "f_m_p": "p|Rörelsemängd|kg*m/s (Kilogrammeter per sekund)",
        "f_m_s": "s|Lägeskoordinat, väg, sträcka|m (Meter)",
        "f_m_T": "T|Omloppstid|s (Sekund)",
        "f_m_t": "t|Tidskoordingat, tid|s (Sekund)",
        "f_m_u": "u|Hastighet|m/s (Meter per sekund)",
        "f_m_v": "v|Hastighet|m/s (Meter per sekund)",
        "f_m_W": "W|Arbete|Nm (Newtonmeter)",
        "f_m_wo": "ω|Vinkelhastighet|rad/s (Radianer per sekund)",
        "kf_akp_p": "p|Rörelsemängd",
    },
    {
        "Fysik": {
            "Mekanik - Kinematik": {
                "v = s/t": {"v": "f_m_v", "s": "f_m_s", "t": "f_m_t"},
                "a = v/t": {"a": "f_m_a", "v": "f_m_v", "t": "f_m_t"},
                "v = v0+a*t": {"v": "f_m_v", "v0": "f_m_v", "a": "f_m_a", "t": "f_m_t"},
                "s = v0*t+(a*t**2)/2": {
                    "s": "f_m_s",
                    "v0": "f_m_v",
                    "t": "f_m_t",
                    "a": "f_m_a",
                },
                "s = (v+v0)/2*t": {
                    "s": "f_m_s",
                    "v0": "f_m_v",
                    "v": "f_m_v",
                    "t": "f_m_t",
                },
                "v**2-v0**2=2*a*s": {
                    "v": "f_m_v",
                    "v0": "f_m_v",
                    "a": "f_m_a",
                    "s": "f_m_s",
                },
            }
        },
        "Matematik": {
            "Geometri - Area": {
                "A_triangel = (b*h)/2": {
                    "A_triangel": "m_ga_A",
                    "b": "m_ga_b",
                    "h": "m_ga_h",
                },
                "A_triangel = sqrt(((a+b+c)/2)*(((a+b+c)/2)-a)*(((a+b+c)/2)-b)*(((a+b+c)/2)-c))": {
                    "A_triangel": "m_ga_A",
                    "a": "m_ga_a",
                    "b": "m_ga_ba",
                    "c": "m_ga_c",
                },
                "A_parallellogram = b*h": {
                    "A_parallellogram": "m_ga_A",
                    "b": "m_ga_b",
                    "h": "m_ga_h",
                },
                "A_rektangel = a*b": {"a": "m_ga_a", "b": "m_ga_ba"},
                "O_rektangel = 2*(a+b)": {
                    "O_rektangek": "m_ga_o",
                    "a": "m_ga_a",
                    "b": "m_ga_ba",
                },
                "A_romb = (d1*d2)/2": {
                    "A_romb": "m_ga_A",
                    "d1": "m_ga_d1",
                    "d2": "m_ga_d2",
                },
                "A_cirkel = pi*r**2": {"A_cirkel": "m_ga_A", "r": "m_ga_r"},
                "O_cirkel = 2*pi*r": {"O_cirkel": "m_ga_o", "r": "m_ga_r"},
                "Båge_cirkelsektor = v*r": {
                    "Båge_cirkelsektor": "m_ga_bå",
                    "v": "m_ga_v",
                    "r": "m_ga_r",
                },
                "A_cirkelsektor = (v*r**2)/2": {
                    "A_cirkelsektor": "m_ga_A",
                    "v": "m_ga_v",
                    "r": "m_ga_r",
                },
            },
            "Geometri - Volym": {
                "V_rätblock = a*b*c": {
                    "V_rätblock": "m_gv_V",
                    "a": "m_gv_a",
                    "b": "m_gv_b",
                    "c": "m_gv_c",
                },
                "V_primsa = B*h": {"V_primsa": "m_gv_V", "B": "m_gv_B", "h": "m_gv_h"},
                "V_klot = (4*pi*r**3)/3": {"V_klot": "m_gv_V", "r": "m_gv_r"},
                "A_klot = 4*pi*r**2": {"A_klot": "m_gv_a", "r": "m_gv_r"},
                "V_klotsegment = (1/3)*pi*h**2*(3*r-h)": {
                    "V_klotsegment": "m_gv_v",
                    "h": "m_gv_h",
                    "r": "m_gv_r",
                },
            },
        },
    },
]


def mathTex_to_QPixmap(mathTex, fs, fig):
    """Create QPixMap from LaTeX
    https://stackoverflow.com/questions/32035251/displaying-latex-in-pyqt-pyside-qtablewidget

    :param mathTex: str
        LaTeX string
    :param fs: int
        Font size
    :param fig: matplotlib.figure.Figure
        Matplotlib Figure
    :return: QPixmap
        QPixMap contaning LaTeX image
    """
    fig.clf()
    fig.patch.set_facecolor("none")
    fig.set_canvas(FigureCanvasAgg(fig))
    renderer = fig.canvas.get_renderer()

    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.patch.set_facecolor("none")
    t = ax.text(0, 0, mathTex, ha="left", va="bottom", fontsize=fs)

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


class Testing(QWidget):
    def __init__(self):
        super().__init__()

        self.info = data[0]
        self.data = data[1]
        self.fig = mpl.figure()

        self.init_ui()
        self.add_formulas()
        self.init_bindings()

    def init_ui(self):
        loadUi("test4.ui", self)
        self.splitter_2.setSizes([int(self.height() * 0.45), int(self.height() * 0.55)])

    def add_formulas(self):
        for branch in self.data:
            parent = QTreeWidgetItem(self.FormulaTree)
            parent.setText(0, branch)

            for sub_branch in self.data[branch]:
                child = QTreeWidgetItem(parent)
                child.setText(0, sub_branch)

                for formula in self.data[branch][sub_branch]:
                    formula_child = QTreeWidgetItem(child)
                    formula_label = QLabel()

                    formula_label.setObjectName(f"{formula}")
                    self.FormulaTree.setItemWidget(formula_child, 0, formula_label)

    def init_bindings(self):
        self.FormulaTree.itemDoubleClicked.connect(self.formula_tree_selected)
        self.FormulaTree.itemExpanded.connect(self.expanded_sub)
        self.FormulaTree.itemCollapsed.connect(self.collapsed_sub)

    def expanded_sub(self, item):
        # Collapse everything else
        root = self.FormulaTree.invisibleRootItem()
        for i in range(root.childCount()):
            branch = root.child(i)
            for j in range(branch.childCount()):
                sub_branch = branch.child(j)
                if sub_branch != item:
                    self.FormulaTree.collapseItem(sub_branch)

        # Set QPixMaps
        # TODO: Move to thread?
        if item.parent():
            for i in range(item.childCount()):
                formula_widget = item.child(i)
                formula_label = self.FormulaTree.itemWidget(formula_widget, 0)
                formula_name = formula_label.objectName()
                expr = formula_name.split("=")
                left = parse_expr(expr[0], evaluate=False)
                right = parse_expr(expr[1], evaluate=False)
                latex_pixmap = mathTex_to_QPixmap(
                    f"${latex(Eq(left, right))}$",
                    15,
                    fig=self.fig,
                )
                formula_label.setPixmap(latex_pixmap)
                item.child(i).setSizeHint(
                    0, QSize(self.sizeHint().width(), latex_pixmap.height())
                )

                self.FormulaTree.setItemWidget(item.child(i), 0, formula_label)
        QPixmapCache.clear()

    def collapsed_sub(self, item):
        """In order to save memory, LaTeX QPixmaps are generated when shown
        and cleared once the user clicks on another sub-branch.

        :param item: QTreeWidgetItem
            The item the user clicked at
        :return:
        """
        if item.parent():
            for i in range(item.childCount()):
                qlabel = self.FormulaTree.itemWidget(item.child(i), 0)
                qlabel.clear()
        QPixmapCache.clear()

    # TODO: Get stuff
    def formula_tree_selected(self):
        selected = self.FormulaTree.selectedItems()
        if selected:
            widget = selected[0]
            qlabel = self.FormulaTree.itemWidget(widget, 0)
            print(qlabel.objectName())


class Main(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

        self.setFixedHeight(900)
        self.setFixedWidth(1500)

        self.formula = Testing()
        self.setCentralWidget(self.formula)


def main():
    import sys

    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    caspy = Main()
    caspy.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
