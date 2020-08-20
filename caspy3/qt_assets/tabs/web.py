import json

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QAction, QActionGroup, QDialog, QWidget
from PyQt5.uic import loadUi

from PyQt5.QtWebEngineWidgets import QWebEnginePage

from qt_assets.dialogs.dialog_add_website import AddWebsite
from qt_assets.dialogs.dialog_remove_website import RemoveWebsite


class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        pass


class WebTab(QWidget):

    display_name = "Web"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/web.ui", self)

        page = WebEnginePage(self.web)
        self.web.setPage(page)

        self.main_window = main_window
        if "selected_web_index" in list(self.main_window.settings_data.keys()):
            self.selected_web_index = self.main_window.settings_data["selected_web_index"]
        else:
            self.selected_web_index = 0
        self.main_window.add_to_save_settings({"selected_web_index": self.selected_web_index})

        self.init_web_menu()
        self.main_window.latex_text = ""

        # Load first url
        self.web.load(QUrl(list(self.main_window.websites_data[self.selected_web_index].values())[0]))

    def init_web_menu(self):
        self.menuWeb = self.main_window.menubar.addMenu("Web")
        self.set_actions()

    def set_actions(self):
        self.menuWeb.clear()
        self.web_list = self.main_window.websites_data
        self.web_menu_action_group = QActionGroup(self.menuWeb)

        for i in self.web_list:
            for key in i:
                webAction = QAction(key, self.menuWeb, checkable=True)
                if webAction.text() == list(self.web_list[self.selected_web_index].keys())[0]:
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

    def updateWeb(self, action):
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
                    self.main_window.update_save_settings({"selected_web_index": self.selected_web_index})

    def add_website_window(self):
        self.website_window_add = AddWebsite(self.main_window, self)

    def remove_website_window(self):
        self.website_window_remove = RemoveWebsite(self.main_window, self)