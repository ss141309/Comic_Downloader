from bs4 import BeautifulSoup
import requests
import sqlite3

class Retrieve:
    def __init__(self):
        self.baseURL = 'https://www.comicextra.com/'
        self.info()

    def web_scraper(self, url, class_name, *params):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}

        if params:
            search_page = requests.get(url, headers=headers,  params=params[0])  # sends a GET request to the page
        else:
            search_page = requests.get(url, headers=headers)

        soup = BeautifulSoup(search_page.content,'html.parser')

        div_class = soup.findAll('div', class_= class_name) # finds the class
        soup2 = BeautifulSoup(str(div_class), 'html.parser')

        return soup2

    def search(self, title):
        self.title = title
        url = self.baseURL + 'comic-search'

        data = self.web_scraper(url, 'cartoon-box', {'key':title})

        h3 = data.findAll('h3')
        soup2 = BeautifulSoup(str(h3), 'html.parser').findAll('a')

        link = [name['href'] for name in soup2]
        comic = [name.text for name in soup2]

        with sqlite3.connect('comic.db') as conn:
            conn.execute('DELETE FROM SEARCH')

            for ele in range(len(comic)):
                conn.execute('''INSERT INTO SEARCH (ID, TITLE, URL)
                                VALUES (?, ?, ?)''', (ele+1, comic[ele], link[ele]))

    def info(self, url='https://www.comicextra.com/comic/civil-war-2006'):
        data = self.web_scraper(url, 'movie-meta-info')

        a = data.findAll('a')
        dd = data.select("dd[class=movie-dd]") # for exact match of the class

        summary = self.web_scraper(url, 'content')
        summary = summary.text.strip('\n[]')

        status = a[1].text
        publisher = a[2].text

        pub_date = dd[1].text.lstrip('\n')
        author = dd[2].text.lstrip('\n')

        data2 = self.web_scraper(url, 'movie-l-img')
        img = data2.find('img')


        with sqlite3.connect('comic.db') as conn:
            conn.execute('''UPDATE SEARCH SET PUBLISHER = ?,
                                              WRITER = ?,
                                              PUBLICATION_DATE = ?,
                                              IMG_URL = ?,
                                              SUMMARY = ?,
                                              STATUS = ?
                            WHERE URL = ?''', (publisher, author, pub_date, img['src'], summary, status, url))

    def chapters(self, url):
        data = self.web_scraper(url, 'episode-list')

        td = data.findAll('td')
        a = BeautifulSoup(str(td), 'html.parser').findAll('a')
        a = a[::-1]

        counter = 1
        with sqlite3.connect('comic.db') as conn:
            conn.execute('DELETE FROM CHAPTERS')
            for i in a:
                conn.execute('''INSERT INTO CHAPTERS VALUES
                                (?, ?, ?, ?)''', (counter, i['href'], i.text, url))
                counter += 1

    def chap_img(self, url):
        url = url+'/full'
        data = self.web_scraper(url, 'chapter-main')
        img = data.findAll('img', class_='chapter_img')


        imgs = [x['src'] for x in img]

        return imgs
