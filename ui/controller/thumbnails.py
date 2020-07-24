from img_download.img_download import img_dwnld
from makedir.makedir import mkdirs

import os
import re
import sqlite3

def thumbnails(img_url, name, tab_name):
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

        img_path = cur.fetchone()
        img_path = img_path[0]

        return img_path
