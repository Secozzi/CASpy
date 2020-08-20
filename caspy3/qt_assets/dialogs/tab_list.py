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

        with open("data/settings.json", "r", encoding="utf8") as json_f:
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
        #print(self.settings_json)

        with open("data/settings.json", "w", encoding="utf-8") as json_f:
            json.dump(self.settings_json, json_f, ensure_ascii=False, indent=4, sort_keys=False)

        self.main_window.load_settings()

        event.accept()