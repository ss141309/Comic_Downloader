from retrieve.retrieve_search import Retrieve

import sqlite3

def get(name):
    getter = Retrieve()
    getter.search(name)

    with sqlite3.connect('comic.db') as conn:
        cur = conn.cursor()

        cur.execute('SELECT ID, TITLE FROM SEARCH')
        rows = cur.fetchall()

    return rows

def get_name(search_bar):
    name = search_bar.text()
    search_bar.clear()
    rows = get(name)

    return rows
