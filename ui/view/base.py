from ui.view.table_ui import Table
from ui.view.search_ui import Search
from ui.view.info_ui import Info
from ui.view.disp_img import DispImg

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget

import sys

class ComicUi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Comic Downloader')
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(1200, 50, 600, 400)

        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.table = Table()
        self.generalLayout.addWidget(self.table.tabs_wid, 0, 0, 1, 6)

        self.search = Search()
        self.generalLayout.addLayout(self.search.hlayout, 5, 0, 2, 1)

        self.info = Info()
        self.generalLayout.addLayout(self.info.vlayout, 7, 0)

        self.disp_img = DispImg()
        self.generalLayout.addWidget(self.disp_img.label_Image, 6, 1, 4, 5)
