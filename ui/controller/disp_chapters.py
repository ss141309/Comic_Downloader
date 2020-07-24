from ui.controller.disp_cell_cont import set_table_contents
from ui.view.table_ui import Table

import sqlite3

table = Table()
def disp_chapters(url, table):
    if table == self.view.table_list[0]:
        self.getter.chapters(url)
        tbl = 'CHAPTERS'
    else:
        tbl = 'DOWNLOADED_CHAPTERS'

    with sqlite3.connect('comic.db') as conn:
        cur = conn.cursor()

        cur.execute('SELECT ID, CHAPTER_NAME FROM '+ tbl + ' WHERE URL = ?', (url, ))
        row = cur.fetchall()

    set_table_contents(row, table.table_list[1]) if table == table == table.table_list[0] else set_table_contents(row, table.table_list[3])
