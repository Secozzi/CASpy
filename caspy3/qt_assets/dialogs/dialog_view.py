from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

import pkg_resources


class View(QDialog):
    def __init__(self, text, latex_text, parent=None):
        """
        Opens a QDialog and show text and a rendered latex text of exact answer

        :param text: string
            The text that is shown in the QTextBrowser
        :param latex_text: string
            Mathjax will render the LaTeX and show it with QWebEngineView

        The UI file is loaded and set the text to the QTextBrowser.
        A HTML file using the MathJax API is created and shown with the QWebEngineView
        """

        super(View, self).__init__(parent=None)
        loadUi(pkg_resources.resource_filename('caspy3', "qt_assets/dialogs/main_view_e.ui"), self)
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
