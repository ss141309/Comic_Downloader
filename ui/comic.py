import os
import sys, traceback
import re
import sqlite3
import ctypes
import concurrent.futures

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from retrieve.retrieve_search import Retrieve
from sql_tables.table import SQLTables
from img_download.img_download import img_dwnld, dwnld_batch
from makedir.makedir import mkdirs, cleanup

from com_table import table

myappid = 'abcd' # arbitrary string

# the following statment tells windows,
# that the program that I am running is using Python as a host,
# so that I can display its taskbar icon, see: https://bit.ly/3fv9kr7
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class ComicUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Comic Viewer')
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(1200, 50, 600, 400)

        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.table = table()
        self.generalLayout.addWidget(self.table.tabs_wid, 0, 0, 1, 6)
        self.search()
        self.info()

    '''def table(self):
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

        self.generalLayout.addWidget(self.tabs_wid, 0, 0, 1, 6)'''

    def search(self):
        hlayout = QHBoxLayout()

        self.ledit = QLineEdit()
        self.btn = QPushButton()

        self.ledit.setPlaceholderText('Search')
        self.btn.setText('Ok')

        hlayout.addWidget(self.ledit, 1000)
        hlayout.addWidget(self.btn, 2)

        self.generalLayout.addLayout(hlayout, 5, 0, 2, 1)

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

        self.generalLayout.addLayout(self.vlayout, 7, 0)


    def img(self, img_path):
        frame = QWidget()
        label_Image = QLabel(frame)
        image_path = img_path  # path to your image file
        image_profile = QImage(image_path)  # QImage object
        image_profile = image_profile.scaled(250, 250, aspectRatioMode=Qt.KeepAspectRatio,
                                             transformMode=Qt.SmoothTransformation)  # To scale image for example and keep its Aspect Ratio
        label_Image.setPixmap(QPixmap.fromImage(image_profile))

        self.generalLayout.addWidget(label_Image, 6, 1, 4, 5)

class ComicCtrl:
    def __init__(self):
        SQLTables()
        self.getter = Retrieve()
        self.app = QApplication(sys.argv)
        self.view = ComicUI()
        self.threadpool = QThreadPool()
        self.disp_down_chaps()
        self.connectSignals()

    def connectSignals(self):
        self.view.btn.clicked.connect(self.get_name)
        self.view.ledit.returnPressed.connect(self.get_name)

        self.view.table_list[0].cellDoubleClicked.connect(lambda : self.get_info(self.view.table_list[0], 'SEARCH'))
        self.view.table_list[2].cellDoubleClicked.connect(lambda : self.get_info(self.view.table_list[2], 'DOWNLOADED'))

        self.view.button[0].clicked.connect(lambda : self.btn_was_clicked(0, self.view.stack_layout1))
        self.view.button[1].clicked.connect(lambda : self.btn_was_clicked(1, self.view.stack_layout1))

        self.view.button[2].clicked.connect(lambda : self.btn_was_clicked(0, self.view.stack_layout2))
        self.view.button[3].clicked.connect(lambda : self.btn_was_clicked(1, self.view.stack_layout2))

        self.view.table_list[1].cellDoubleClicked.connect(self.down_chaps)

    def btn_was_clicked(self, index, lay_out):
        lay_out.setCurrentIndex(index)

    def get(self):
        self.getter.search(self.name)

        with sqlite3.connect('comic.db') as conn:
            cur = conn.cursor()

            cur.execute('SELECT ID, TITLE FROM SEARCH')
            rows = cur.fetchall()

        return rows

    def get_name(self):
        self.name = self.view.ledit.text()
        self.view.ledit.clear()
        rows = self.get()
        self.set_table_contents(rows, self.view.table_list[0])

    def set_table_contents(self, records, table):
        table.clearContents()
        for i in enumerate(records):
            d = 0
            table.setItem(i[0], d, QTableWidgetItem(str(i[1][0])))
            item = QTableWidgetItem(i[1][1])
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) # set items not editable
            table.setItem(i[0], d+1, item)
            d += i[0]

    def cell_was_clicked(self, table):
        row = table.currentRow()

        if table.currentItem() != None:
            return table.currentItem().text()

    def thumbnails(self, img_url, name, tab_name):
        dirpath = os.path.abspath('img'+'/'+'thumbnails')
        mkdirs(dirpath)

        title = re.sub('[^a-zA-Z0-9 \n\.]', '', name)
        img_dwnld(img_url, dirpath, title)
        img_path = os.path.join(dirpath, title+'.jpg')

        with sqlite3.connect('comic.db') as conn:
            cur = conn.cursor()

            if tab_name == 'SEARCH':
                cur.execute('''UPDATE SEARCH SET IMG_PATH = ?
                                             WHERE TITLE = ?''',
                                             (img_path, name))

            cur.execute('SELECT IMG_PATH FROM '+ tab_name +
                                        ' WHERE TITLE = ?',
                                         (name,))

            self.img_path = cur.fetchone()
            self.img_path = self.img_path[0]


    def get_info(self, table, tab_name):
        title = self.cell_was_clicked(table)

        with sqlite3.connect('comic.db') as conn:
            cur = conn.cursor()

            cur.execute('SELECT URL FROM '+ tab_name +
                           ' WHERE TITLE = ?', (title,))
            comic_url = cur.fetchone()
            self.getter.info(comic_url[0]) if tab_name == 'SEARCH' else None

            cur.execute('''SELECT TITLE,
                                  PUBLISHER,
                                  WRITER,
                                  PUBLICATION_DATE,
                                  SUMMARY,
                                  STATUS,
                                  IMG_URL,
                                  URL FROM '''+ tab_name +

                          ' WHERE TITLE = ?', (title,))

            info = cur.fetchone()

        for i in range(6):
            self.view.labels[i][1].setText(info[i])

        self.thumbnails(info[6], info[0], tab_name)
        self.view.img(self.img_path)

        self.disp_chapters(info[7], table)
        self.view.stack_layout1.setCurrentIndex(1) if tab_name == 'SEARCH' else self.view.stack_layout2.setCurrentIndex(1)

    def disp_chapters(self, url, table):
        if table == self.view.table_list[0]:
            self.getter.chapters(url)
            tbl = 'CHAPTERS'
        else:
            tbl = 'DOWNLOADED_CHAPTERS'

        with sqlite3.connect('comic.db') as conn:
            cur = conn.cursor()

            cur.execute('SELECT ID, CHAPTER_NAME FROM '+ tbl + ' WHERE URL = ?', (url, ))
            row = cur.fetchall()

        self.set_table_contents(row, self.view.table_list[1]) if table == table == self.view.table_list[0] else self.set_table_contents(row, self.view.table_list[3])

    def down_chaps(self):
        chap_name = self.cell_was_clicked(self.view.table_list[1])
        with sqlite3.connect('comic.db') as conn:
            cur = conn.cursor()

            cur.execute('''SELECT * FROM CHAPTERS
                                  WHERE CHAPTER_NAME = ?''', (chap_name, ))
            url = cur.fetchone()

            cur.execute('''SELECT * FROM SEARCH
                                  WHERE URL = ?''', (url[3],))

            name = cur.fetchone()

            cur.execute('''INSERT INTO DOWNLOADED  ('TITLE',
                                                   'PUBLISHER',
                                                   'WRITER',
                                                   'PUBLICATION_DATE',
                                                   'IMG_URL',
                                                   'URL',
                                                   'IMG_PATH',
                                                   'SUMMARY',
                                                   'STATUS')
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                            ,(name[1], name[2], name[3], name[4], name[5], name[6], name[7], name[8], name[9]))

            cur.execute('''INSERT INTO DOWNLOADED_CHAPTERS (CHAPTER_URL, CHAPTER_NAME, URL) VALUES
                           (?, ?, ?)''', (url[1], url[2], url[3]))

        chap_imgs = self.getter.chap_img(url[1])

        com_name = re.sub('[^a-zA-Z0-9 \n\.]', '', name[1])
        chptr_name = re.sub('[^a-zA-Z0-9 \n\.]', '', url[2])

        dirname = os.path.join('img', com_name, chptr_name)
        dirpath = os.path.abspath(dirname)
        mkdirs(dirpath)

        dwnld_batch(chap_imgs, dirpath)

    def disp_down_chaps(self):
        with sqlite3.connect('comic.db') as conn:
            cur = conn.cursor()

            cur.execute('SELECT ID, TITLE, URL FROM DOWNLOADED GROUP BY TITLE')
            rows = cur.fetchall()

        self.set_table_contents(rows, self.view.table_list[2])


    def run(self):
        self.view.show()
        return self.app.exec_()


def main():
    c = ComicCtrl()
    sys.exit(c.run())


main()
