from retrieve.retrieve_search import Retrieve

from ui.controller.thumbnails import thumbnails

import sqlite3

def cell_was_clicked(table):
    row = table.currentRow()

    if table.currentItem() != None:
        return table.currentItem().text()

def get_info(table, tab_name, labels):
    getter = Retrieve()
    title = cell_was_clicked(table)

    if title is not None:
        with sqlite3.connect('comic.db') as conn:
            cur = conn.cursor()

            cur.execute('SELECT URL FROM '+ tab_name +
                           ' WHERE TITLE = ?', (title,))
            comic_url = cur.fetchone()
            getter.info(comic_url[0]) if tab_name == 'SEARCH' else None

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
            labels[i][1].setText(info[i])

        thumbnail = thumbnails(info[6], info[0], tab_name)


        self.disp_chapters(info[7], table)
        #self.view.stack_layout1.setCurrentIndex(1) if tab_name == 'SEARCH' else self.view.stack_layout2.setCurrentIndex(1)
