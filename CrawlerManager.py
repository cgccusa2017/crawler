import sys

from bs4 import BeautifulSoup as Soup
from sqlalchemy.exc import SQLAlchemyError

import ErrorCode as ErrorCode
import requests
import Crawler
import Init

from sqlalchemy import create_engine
from sqlalchemy import MetaData
import CreateTable as db
from sqlalchemy.orm import sessionmaker

class CrawlerManager():

    def get_url(self):
        """
        This function will return the next url to crawl (also the url_id), in the order of priority
        :return: url, url_id
        """
        url = ''
        url_id = 0
        # retrieve url from url task table
        return url, url_id

    def process_text(self, url_content):

        """
        This function separate links and text content from the url_content.
        :param: url: the url
        :return: links: all links found in the url
        :return: text: text after processing
        """
        # parse for url list
        # send text to NLP unit

        links = set()
        text = Soup(url_content, 'html.parser')

        for a in text.find_all('a'):
                links.add(a['href'])
                del a['href']

        return links, text

    # crawler_setter = crawler_setter(): a function that sets up cookies and headers etc.
    def crawler_setter(self, crawler, crawler_settings):

        pass

    def crawl(self, crawler, crawler_setter=None, crawler_settings=None):

        if crawler_setter and crawler_settings:
            crawler = crawler_setter(crawler, crawler_settings)
        # crawler_setter = crawler_setter(): a function that sets up cookies and headers etc.

        # get the next url to crawl, store the url_id for later updating urlText table
        url, url_id = self.get_url()

        # crawler = Crawler.Crawler()
        code, url_content = crawler.crawl(url)

        # if able to open the url, get links and texts from it
        if code == requests.codes.ok:
            # get text and put into urlText
            # get links

            links, text = self.process_text(url_content)

            # store text from url into table
            state = self.update_url_text(url_id, text)

            # if updating not success
            if state == -1:
                print("Error: cannot update the URL_TEXT table")
                sys.exit()

        elif code in ErrorCode.retry_code:
            # should retry crawling this url later
            pass


    def update_url_text_table(self, url_id, text):
        """
        This function store information into url text table.

        :param url_id: the url_id from url task table
        :param text:
        :return: 0 if successfully updating row in the table, -1 if failed
        """

        # check whether the text is updated
        # if true
        # # update the url updating frequency

        with db.session_scope() as session:
            try:
                # try query using url_id
                row = session.query(db.URLText).filter(db.URLText.url_id == url_id).first()

                if row is None:
                    row = db.URLText(
                        url_id=url_id,
                        timestamp=0,
                        text=text
                    )
                    session.add(row)
                else:
                    row.text = text

                session.commit()
                print("Success: Updating rows in table")

            except SQLAlchemyError as e:
                print(e)
                return -1

        return 0


    def update_url_task_table(self, urls):
        '''
        This function enqueue newly found urls
        :param urls:
        :return:
        '''

        # remove duplicate

        # bloom filter vs. query db
        pass



