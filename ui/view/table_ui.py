from PyQt5.QtWidgets import QTabWidget, QTableWidget, QStackedLayout, QWidget,\
                            QPushButton, QHeaderView, QHBoxLayout, QGridLayout

class Table:
    def __init__(self):
        self.table()

    def table(self):
        self.tabs_wid = QTabWidget()
        self.stack_layout1 = QStackedLayout()
        self.stack_layout2 = QStackedLayout()

        self.table_list = []
        for i in range(4):
            self.table = QTableWidget()
            self.table.setColumnCount(2)
            self.table.setRowCount(1000)
            self.table.setFrameStyle(0)
            header = ['S. No.', 'Title'] if i == 0 or i == 2 else ['S. No.', 'Chapter']
            self.table.setHorizontalHeaderLabels(header)
            self.header = self.table.horizontalHeader()
            self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.header.setSectionResizeMode(1, QHeaderView.Stretch)
            self.table.verticalHeader().setVisible(False)

            self.table_list.append(self.table)

        self.stack_layout1.addWidget(self.table_list[0])
        self.stack_layout1.addWidget(self.table_list[1])

        self.stack_layout2.addWidget(self.table_list[2])
        self.stack_layout2.addWidget(self.table_list[3])

        # Since QTabWidget only accepts a widget, a widget is made with the stacked layout
        tab1 = QWidget()
        tab2 = QWidget()

        self.button = []
        for j in range(2):
            self.forward = QPushButton()
            self.back = QPushButton()

            self.forward.setText('\u2192')
            self.back.setText('\u2190')

            self.forward.setFixedSize(22, 22)
            self.back.setFixedSize(22, 22)

            self.button.extend([self.back, self.forward])

        self.horilayout = QHBoxLayout()
        self.horilayout2 = QHBoxLayout()

        self.horilayout.addWidget(self.button[0])
        self.horilayout.addWidget(self.button[1])

        self.horilayout2.addWidget(self.button[2])
        self.horilayout2.addWidget(self.button[3])

        self.vertlayout = QGridLayout()
        self.vertlayout.addLayout(self.horilayout, 0, 5)
        self.vertlayout.addLayout(self.stack_layout1, 1, 0, 1, 6)

        self.vertlayout2 = QGridLayout()
        self.vertlayout2.addLayout(self.horilayout2, 0, 5)
        self.vertlayout2.addLayout(self.stack_layout2, 1, 0, 1, 6)

        tab1.setLayout(self.vertlayout)
        tab2.setLayout(self.vertlayout2)

        self.tabs_wid.addTab(tab1, 'Download')
        self.tabs_wid.addTab(tab2, 'Downloaded')
