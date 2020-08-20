import json

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class AddWebsite(QDialog):
    def __init__(self, main_window, web_tab ,parent=None):
        super(AddWebsite, self).__init__(parent=None)
        self.main_window = main_window
        self.web_list = self.main_window.websites_data
        self.web_tab = web_tab

        loadUi("qt_assets/dialogs/web_add.ui", self)

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