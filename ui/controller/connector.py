from ui.view.base import ComicUi

from nav import btn_was_clicked
from get_term import get_name
from disp_cell_cont import set_table_contents

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys

class ComicCtrl:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = ComicUi()
        self.connectSignals()

    def connectSignals(self):
        search_bar = self.view.search.ledit
        table1 = self.view.table.table_list[0]
        self.view.search.btn.clicked.connect(lambda : [content_list := get_name(search_bar), set_table_contents(content_list, table1)])
        self.view.search.ledit.returnPressed.connect(lambda : [content_list := get_name(search_bar), set_table_contents(content_list, table1)])

        self.view.table.button[0].clicked.connect(lambda : btn_was_clicked(0, self.view.table.stack_layout1))
        self.view.table.button[1].clicked.connect(lambda : btn_was_clicked(1, self.view.table.stack_layout1))

        self.view.table.button[2].clicked.connect(lambda : btn_was_clicked(0, self.view.table.stack_layout2))
        self.view.table.button[3].clicked.connect(lambda : btn_was_clicked(1, self.view.table.stack_layout2))

    def run(self):
        self.view.show()
        return self.app.exec_()

if __name__ == '__main__':
    c = ComicCtrl()
    sys.exit(c.run())
