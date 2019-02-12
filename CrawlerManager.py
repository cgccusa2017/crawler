import sys
from sqlalchemy.exc import SQLAlchemyError

import ErrorCode as ErrorCode
import requests

from Crawler import Crawler
from urllib.parse import urlparse

from __init__ import Session

import TextProcessor
import CrawlerModel as db
import Crawler

class CrawlerManager:
    def __init__(self, state=1):
        """
        :param state: 1 active, 0 inactive, 2 wait, 3 error
        """
        self.state = state
        self.session = Session()
        self.tp = TextProcessor.TextProcessor()

    def __del__(self):
        self.session.close()


    # TODO: build a new table, store domain name and quota #
    # TODO: get url based on SORT(timestamp+duration); compare Priority if tie
    # TODO: add a column: available time
    def get_url(self):
        """
        This function will return the next url to crawl (also the url_id), in the order of priority
        :return: url
        :return: url_id
        """

        #url = "http://www.google.com/"
        url = "http://www.github.com"
        url_id = 1
        # retrieve url from url task table
        return url, url_id


    def process_text(self, origin_url, url_content, keyword=None):
        """
        This function separate links and text content from the url_content.
        :param: url: the url
        :return: links: all links found in the url
        :return: text: text after processing
        """
        links, text = self.tp.separate_url_text(origin_url, url_content, keyword)
        return links, text


    def start_crawl(self, crawler, crawler_settings=None):
        """
        This function starts a crawler
        :param crawler:
        :param crawler_settings: a dictionary contains header {}, form_data {}
        :return: nothing to return, update the url_task and url_text table
        """

        # get the next url to crawl, store the url_id for later updating urlText table
        origin_url, url_id = self.get_url()

        origin_url, code, url_content = crawler.crawl(origin_url, crawler_settings)

        # if able to open the url, get links and texts from it
        if code == requests.codes.ok:
            # get text and put into urlText
            # get links

            url_lists, text = self.process_text(origin_url, url_content)


            if text:
                # store text from url into table
                state = self.update_url_text_table(url_id, text)

                # if updating not success
                if state == -1:
                    print("Error: cannot update the URL_TEXT table")
                    sys.exit()


            if url_lists:
                state = self.update_url_task_table(origin_url, url_lists, quota=100)

                # if updating not success
                if state == -1:
                    print("Error: cannot update the URL_TASK table")
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

        text = "Testing Mode"
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
                print("Success: Updating url text table")

            except SQLAlchemyError as e:
                print(e)
                return -1

        return 0


    # TODO: bloom filter and query db
    def update_url_task_table(self, origin_url, url_lists, quota=100):
        """
        This function enqueue newly found urls into task table
        :param origin_url: the original url, for domain checking
        :param url_lists: list of urls
        :param quota: the maximum number of website to put into table
        :return:
        """
        cnt = 0
        with db.session_scope() as session:
            print(url_lists)


            while url_lists and cnt < quota:
                try:
                    curr = url_lists.pop()

                    if self.check_domain(origin_url, curr):

                        row = session.query(db.URLTask).filter(db.URLTask.url == curr).first()

                        if row is None:
                            row = db.URLTask(url=curr)
                            session.add(row)
                            cnt += 1
                            print("Success: Updating url task table")

                    session.commit()

                except SQLAlchemyError as e:
                    print(e)
                    return -1
            print(cnt)
            return 0
        return 0



    def check_domain(self, origin_url, new_url):
        """
        This function check if the new url comes from the same domain as the original one
        :param origin_url: the seed url
        :param new_url: the new url to check
        :return: True if same domain, False otherwise.
        """
        origin_obj = urlparse(origin_url)
        new_obj = urlparse(new_url)

        return origin_obj.netloc == new_obj.netloc






if __name__ == "__main__":
    cm = CrawlerManager()
    crawler: Crawler = Crawler.Crawler()
    cm.start_crawl(crawler)

    #origin_url = "http://www.google.com/"
    #new_url = "http://www.google.com/intl/en/ads/"
    #print(cm.check_domain(origin_url, new_url))
