from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton

class Search:
    def __init__(self):
        self.search()

    def search(self):
        self.hlayout = QHBoxLayout()

        self.ledit = QLineEdit()
        self.btn = QPushButton()

        self.ledit.setPlaceholderText('Search')
        self.btn.setText('Ok')

        self.hlayout.addWidget(self.ledit, 1000)
        self.hlayout.addWidget(self.btn, 2)
