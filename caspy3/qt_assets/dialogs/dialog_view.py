#
#    CASPy - A program that provides both a GUI and a CLI to SymPy.
#    Copyright (C) 2020 Folke Ishii
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

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

import pkg_resources


class View(QDialog):
    def __init__(self, text: str, latex_text: str, parent=None) -> None:
        """
        Opens a QDialog and show text and a rendered latex text of exact answer

        :param text: str
            The text that is shown in the QTextBrowser
        :param latex_text: str
            Mathjax will render the LaTeX and show it with QWebEngineView

        The UI file is loaded and set the text to the QTextBrowser.
        A HTML file using the MathJax API is created and shown with the QWebEngineView
        """

        super(View, self).__init__(parent=None)
        loadUi(
            pkg_resources.resource_filename(
                "caspy3", "qt_assets/dialogs/main_view_e.ui"
            ),
            self,
        )
        font_size = "2.5em"
        page_source = f"""
             <html><head>
             <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
             <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
             </script></head>
             <body>
             <p><mathjax style="font-size:{font_size}">$${latex_text}$$</mathjax></p>
             </body></html>
             """
        self.exact_text.setText(text)
        self.web.setHtml(page_source)
        self.show()
