import json

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QAction, QActionGroup, QDialog, QWidget
from PyQt5.uic import loadUi


class WebTab(QWidget):

    display_name = "Web"

    def __init__(self, main_window):
        super().__init__()
        loadUi("qt_assets/tabs/web.ui", self)
        self.main_window = main_window
        self.init_web_menu()
        self.main_window.latex_text = ""
        # Load first url
        self.web.load(QUrl(list(self.main_window.websites_data[0].values())[0]))

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
                if webAction.text() == "Desmos":
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

    def add_website_window(self):
        self.website_window_add = Add_Website(self.main_window, self)

    def remove_website_window(self):
        self.website_window_remove = Remove_Website(self.main_window, self)

class Add_Website(QDialog):
    def __init__(self, main_window, web_tab ,parent=None):
        super(Add_Website, self).__init__(parent=None)
        self.main_window = main_window
        self.web_list = self.main_window.websites_data
        self.web_tab = web_tab

        loadUi("qt_assets/tabs/web_add.ui", self)

        self.add_button_box.accepted.connect(self.add_website)
        self.add_button_box.rejected.connect(self.close)

        self.show()

    def add_website(self):
        self.main_window.websites_data.append({self.display_line.text(): self.url_line.text()})

        with open("data/websites.json", "w", encoding="utf-8") as json_f:
            json.dump(self.main_window.websites_data, json_f, ensure_ascii=False, indent=4, sort_keys=False)

        # Reload json file reading
        self.main_window.load_websites()
        self.web_tab.set_actions()

        self.close()

class Remove_Website(QDialog):
    def __init__(self, main_window, web_tab, parent=None):
        super(Remove_Website, self).__init__(parent=None)
        self.main_window = main_window
        self.web_list = self.main_window.websites_data
        self.web_tab = web_tab

        loadUi("qt_assets/tabs/web_remove.ui", self)
        for i in self.web_list:
            self.remove_combo.addItem(list(i.keys())[0])

        self.remove_button_box.accepted.connect(self.remove_website)
        self.remove_button_box.rejected.connect(self.close)

        self.show()

    def remove_website(self):
        """
        Gets selected item, removes it from the list of websites and writes it to the file.
        """
        selected_key = self.web_list[self.remove_combo.currentIndex()]
        self.main_window.websites_data.remove(selected_key)
        with open("data/websites.json", "w", encoding="utf-8") as json_f:
            json.dump(self.main_window.websites_data, json_f, ensure_ascii=False, indent=4, sort_keys=True)

        # Reload json file
        self.main_window.load_websites()
        self.web_tab.set_actions()

        self.close()