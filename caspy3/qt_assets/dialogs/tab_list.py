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

import json, sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon


class TabList(QListWidget):
    def __init__(self, main_window):
        super(TabList, self).__init__()
        self.main_window = main_window
        self.setFixedWidth(340)
        self.setWindowTitle("CASPy Tab List")
        self.setWindowIcon(QIcon("assets/logo.png"))
        self.setToolTip("Settings take into effect on application launch.")

        self.setAlternatingRowColors(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDragDropOverwriteMode(False)

        with open(self.main_window.get_resource_path("data/settings.json"), "r", encoding="utf8") as json_f:
            tab_file = json_f.read()
            self.settings_json = json.loads(tab_file)
            self.tab_data = self.settings_json["tabs"]

        self.setFixedHeight(int(18.2 * len(self.tab_data.keys())))

        for tab in list(self.tab_data.keys()):
            item = QListWidgetItem(tab)

            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
            if self.tab_data[tab]:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

            self.addItem(item)

        self.show()

    def str_to_class(self, classname):
        return getattr(sys.modules[__name__], classname)

    def closeEvent(self, event):
        new_tab_list = {}

        for i in range(self.count()):
            item = self.item(i)
            new_tab_list[item.text()] = True if item.checkState() == 2 else False

        self.settings_json.update({"tabs": new_tab_list})

        with open(self.main_window.get_resource_path("data/settings.json"), "w", encoding="utf-8") as json_f:
            json.dump(self.settings_json, json_f, ensure_ascii=False, indent=4, sort_keys=False)

        self.main_window.load_settings()

        event.accept()
