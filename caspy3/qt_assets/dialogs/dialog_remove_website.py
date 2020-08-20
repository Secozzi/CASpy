import json

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class RemoveWebsite(QDialog):
    def __init__(self, main_window, web_tab, parent=None):
        super(RemoveWebsite, self).__init__(parent=None)
        self.main_window = main_window
        self.web_list = self.main_window.websites_data
        self.web_tab = web_tab

        loadUi("qt_assets/dialogs/web_remove.ui", self)
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