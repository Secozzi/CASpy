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

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QAction, QActionGroup, QDialog, QWidget
from PyQt5.uic import loadUi

from PyQt5.QtWebEngineWidgets import QWebEnginePage

from ..dialogs.dialog_add_website import AddWebsite
from ..dialogs.dialog_remove_website import RemoveWebsite


class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(
        self,
        level: "QWebEnginePage.JavaScriptConsoleMessageLevel",
        message: str,
        lineNumber: int,
        sourceID: str,
    ) -> None:
        pass


class WebTab(QWidget):

    display_name = "Web"

    def __init__(self, main_window: "CASpyGUI") -> None:
        super().__init__()
        self.main_window = main_window
        loadUi(self.main_window.get_resource_path("qt_assets/tabs/web.ui"), self)
        self.eout = None
        self.aout = None

        page = WebEnginePage(self.web)
        self.web.setPage(page)

        if "selected_web_index" in list(self.main_window.settings_data.keys()):
            self.selected_web_index = self.main_window.settings_data[
                "selected_web_index"
            ]
        else:
            self.selected_web_index = 0
        self.main_window.add_to_save_settings(
            {"selected_web_index": self.selected_web_index}
        )

        self.init_web_menu()
        self.main_window.latex_text = ""

        self.web.load(
            QUrl(
                list(self.main_window.websites_data[self.selected_web_index].values())[
                    0
                ]
            )
        )

    def init_web_menu(self) -> None:
        self.menuWeb = self.main_window.menubar.addMenu("Web")
        self.set_actions()

    def set_actions(self) -> None:
        self.menuWeb.clear()
        self.web_list = self.main_window.websites_data
        self.web_menu_action_group = QActionGroup(self.menuWeb)

        for i in self.web_list:
            for key in i:
                webAction = QAction(key, self.menuWeb, checkable=True)
                if (
                    webAction.text()
                    == list(self.web_list[self.selected_web_index].keys())[0]
                ):
                    webAction.setChecked(True)
                self.menuWeb.addAction(webAction)
                self.web_menu_action_group.addAction(webAction)

        self.web_menu_action_group.setExclusive(True)

        self.add_website = QAction("Add Website", self)
        self.remove_website = QAction("Remove Website", self)
        self.menuWeb.addSeparator()
        self.menuWeb.addAction(self.add_website)
        self.menuWeb.addAction(self.remove_website)
        self.add_website.triggered.connect(self.add_website_window)
        self.remove_website.triggered.connect(self.remove_website_window)

        self.web_menu_action_group.triggered.connect(self.updateWeb)

    def updateWeb(self, action: QAction) -> None:
        """
        Updates web tab when user selects new website.

        Parameters
        ---------------
        action: QAction
            action.text() shows text of selected radiobutton
        """
        for i in self.web_list:
            for key in i:
                if action.text() == key:
                    self.web.load(QUrl(i[key]))
                    self.selected_web_index = self.web_list.index(i)
                    self.main_window.update_save_settings(
                        {"selected_web_index": self.selected_web_index}
                    )

    def add_website_window(self) -> None:
        self.website_window_add = AddWebsite(self.main_window, self)

    def remove_website_window(self) -> None:
        self.website_window_remove = RemoveWebsite(self.main_window, self)
