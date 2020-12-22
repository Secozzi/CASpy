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

import json

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class AddWebsite(QDialog):
    def __init__(self, main_window: "CASpyGUI", web_tab: "WebTab", parent=None) -> None:
        super(AddWebsite, self).__init__(parent=None)
        self.main_window = main_window
        self.web_list = self.main_window.websites_data
        self.web_tab = web_tab

        loadUi(self.main_window.get_resource_path("qt_assets/dialogs/web_add.ui"), self)

        self.add_button_box.accepted.connect(self.add_website)
        self.add_button_box.rejected.connect(self.close)

        self.show()

    def add_website(self) -> None:
        self.main_window.websites_data.append(
            {self.display_line.text(): self.url_line.text()}
        )

        with open(
            self.main_window.get_resource_path("data/websites.json"),
            "w",
            encoding="utf-8",
        ) as json_f:
            json.dump(
                self.main_window.websites_data,
                json_f,
                ensure_ascii=False,
                indent=4,
                sort_keys=False,
            )

        # Reload json file reading
        self.main_window.load_websites()
        self.web_tab.set_actions()

        self.close()
