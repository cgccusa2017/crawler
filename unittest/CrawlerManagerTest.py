

import sys
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
__package__='crawler'
from CrawlerApp import CrawlerManager, CrawlerWorker
import CrawlerApp.CrawlerModel as db
from sqlalchemy.exc import SQLAlchemyError
import unittest



class CrawlerManagerTest(unittest.TestCase):
    """
    This is the unit test for Crawler Manager.
    """
    def __init__(self):
        self.manager = CrawlerManager.CrawlerManager()
        self.worker = CrawlerWorker.Crawler()

    # def test_manager(self, target_url):
    #     return self.crawler.crawl(target_url)

    def test_get_url(self):
        return self.manager.get_url()

    def test_check_domain(self, origin_url, new_url):
        return self.manager.check_domain(origin_url, new_url)


    def test_check_update_task_table(self, origin_url):
        #diff = -1
        with db.session_scope() as session:
            try:
                old_count = session.query(db.URLTask).count()

                origin_url, code, text = self.worker.crawl(origin_url)
                url_lists, _ = self.manager.process_text(origin_url, text)
                self.manager.update_url_task_table(origin_url, url_lists)

                new_count = session.query(db.URLTask).count()

                diff = new_count - old_count
            except SQLAlchemyError as e:
                print(e)
                return -1
        return diff

    def test_get_url_id(self, url):
        return self.manager.get_url_id(url)

    def test_check_update_text_table(self, origin_url):
        diff = -1
        with db.session_scope() as session:
            try:
                old_count = session.query(db.URLText).count()
                origin_url, code, text = self.worker.crawl(origin_url)

                if code != -1:
                    url_id = self.manager.get_url_id(origin_url)
                    self.manager.update_url_text_table(url_id, text)

                    new_count = session.query(db.URLText).count()
                    diff = new_count - old_count
                else:
                    return -1
            except SQLAlchemyError as e:
                print(e)
                return -1

        return diff


    def get_text(self, url):
        """
        This function prints all text content (except url link) from the crawler result.
        :param origin_url: the url we want to get text from
        :return:
        """
        url, code, url_content = self.worker.crawl(url)
        _, text = self.manager.process_text(url, url_content)

        print(text)


if __name__ == "__main__":
    cmt = CrawlerManagerTest()
    origin_url = "https://www.python.org/"
    origin_url = "https://tuebui.com/joining-data-sets-with-hadoop-streaming-mapreduce-and-python/"


    cmt.get_text(origin_url)

"""
    print("Testing CrawlerManager...")
    print("Testing Method: get_url()")
    assert len(cmt.test_get_url()) == 2
    assert isinstance(cmt.test_get_url()[0], str)
    assert isinstance(cmt.test_get_url()[1], int)
    assert cmt.test_get_url()[0] is not None
    assert cmt.test_get_url()[1] is not None

    print("Testing Method: check_domain(self, origin_url, new_url)")
    assert isinstance(cmt.test_check_domain("http://www.github.com", "www.github.com"), bool)
    assert cmt.test_check_domain("http://www.github.com", "www.com") is False
    assert cmt.test_check_domain("http://www.github.com", "http://www.github.com") is True
    assert cmt.test_check_domain("http://github.com", "http://github.com/pulls") is True

    print("Testing Method: test_check_update_task_table(self, origin_url, url_lists)")

    assert cmt.test_check_update_task_table(origin_url) >= 0

    print("Testing Method: test_get_url_id(self, url)")
    assert isinstance(cmt.test_get_url_id(origin_url), int)

    print("Testing Method: test_check_update_text_table(self, origin_url)")
    assert cmt.test_check_update_text_table(origin_url) >= 0
    print("Passed All Test cases.")
"""

