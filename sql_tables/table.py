import sqlite3

class SQLTables:
    def __init__(self):

        with sqlite3.connect('comic.db') as self.conn:
            self.downloaded()
            self.download_chapters()
            self.search()
            self.chapters()

    def downloaded(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS DOWNLOADED
                    (ID INTEGER        PRIMARY KEY AUTOINCREMENT NOT NULL,
                    TITLE              TEXT NOT NULL,
                    PUBLISHER          TEXT,
                    WRITER             TEXT,
                    PUBLICATION_DATE   TEXT,
                    IMG_URL            TEXT,
                    URL                TEXT,
                    IMG_PATH           TEXT,
                    SUMMARY            TEXT,
                    STATUS             TEXT);''')

    def download_chapters(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS DOWNLOADED_CHAPTERS
                    (ID INTEGER   PRIMARY KEY AUTOINCREMENT NOT NULL,
                     CHAPTER_URL  TEXT ,
                     CHAPTER_NAME TEXT,
                     URL          TEXT);''')

    def search(self):
        self.conn.execute('''CREATE  TABLE IF NOT EXISTS SEARCH
                    (ID                INTEGER PRIMARY KEY NOT NULL,
                    TITLE              TEXT,
                    PUBLISHER          TEXT,
                    WRITER             TEXT,
                    PUBLICATION_DATE   TEXT,
                    IMG_URL            TEXT,
                    URL                TEXT,
                    IMG_PATH           TEXT,
                    SUMMARY            TEXT,
                    STATUS             TEXT);''')



    def chapters(self):
        self.conn.execute('''CREATE  TABLE IF NOT EXISTS CHAPTERS
                    (ID           INTEGER,
                     CHAPTER_URL  TEXT,
                     CHAPTER_NAME TEXT,
                     URL          TEXT);''')
