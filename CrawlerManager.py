
from bs4 import BeautifulSoup as Soup
import ErrorCode as ErrorCode
import requests
import Crawler

from sqlalchemy import create_engine
from sqlalchemy import MetaData
import CreateTable as db
from sqlalchemy.orm import sessionmaker

class CrawlerManager():
    def get_url(self):
        # retrieve url from url task table
        pass
    def process_text(self):
        # parse for url list
        # send text to NLP unit
        pass

    def crawl_url(self, crawler):
        url = self.get_url()
        # crawler = Crawler.Crawler()
        code, text = crawler.crawl(url)

        if code == requests.codes.ok:
            # get text and put into urlText
            # get links
            links = set()

            text = Soup(url, 'html.parser')
            for a in text.find_all('a'):
                links.add(a['href'])
                del a['href']

            # store text from url into table
            self.update_url_text(url, text)


        elif code in ErrorCode.retry_code:
            # should retry crawling this url later
            pass



    def update_url_text(self, url, text):
        '''
        This function store information into url task table.
        row = URLText( text_id=1,url_id=1,timestamp=20190204,text='Try to see if ForeignKey works')

        :param text:
        :return:
        '''
        # check whether the text is updated
        # if true
        # # update the url updating frequency
        # engine = create_engine(db.db_uri)
        Session = sessionmaker()
        Session.configure(bind=engine)

        with db.session_scope() as session:
            print("Adding rows in table")

        pass


    def update_url_task(self, urls):
        '''
        This function enqueue newly found urls
        :param urls:
        :return:
        '''

        # remove duplicate

        # bloom filter vs. query db
        pass



