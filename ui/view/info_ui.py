from PyQt5.QtWidgets import *

class Info:
    def __init__(self):
        self.info()

    def info(self):
        self.vlayout = QVBoxLayout()

        hlay = []
        for lay in range(6):
            self.hlayout = QHBoxLayout()
            hlay.append(self.hlayout)

        self.labels = []

        names = ['Name:',
                 'Publisher:',
                 'Writer:',
                 'Publication Date:',
                 'Summary:',
                 'Status:']

        for label in range(len(names)):
            self.label = QLabel()
            self.label2 = QLabel()
            self.label2.setWordWrap(True)

            self.labels.append([self.label, self.label2])

            self.label.setText(names[label])

        for sett in range(6):
            hlay[sett].addWidget(self.labels[sett][0], 1)  # Second argument sets the stretch ratio with the other widget
            hlay[sett].addWidget(self.labels[sett][1], 50)

            hlay[sett].setSpacing(5)

            self.vlayout.addLayout(hlay[sett])

        self.vlayout.setSpacing(25)
