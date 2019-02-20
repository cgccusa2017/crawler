

import sys
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
__package__='crawler'
from CrawlerApp import CrawlerManager

import unittest



class CrawlerManagerTest(unittest.TestCase):

    def __init__(self):
        self.manager = CrawlerManager.CrawlerManager()

    # def test_manager(self, target_url):
    #     return self.crawler.crawl(target_url)

    def test_get_url(self):
        return self.manager.get_url()

    def test_check_domain(self, origin_url, new_url):
        return self.manager.check_domain(origin_url, new_url)


if __name__ == "__main__":
    cmt = CrawlerManagerTest()
    print("Testing CrawlerManager...")

    print("Testing Method get_url()")
    assert len(cmt.test_get_url()) == 2
    assert isinstance(cmt.test_get_url()[0], str)
    assert isinstance(cmt.test_get_url()[1], int)
    assert cmt.test_get_url()[0] is not None
    assert cmt.test_get_url()[1] is not None

    print("Testing Method check_domain(self, origin_url, new_url)")
    assert isinstance(cmt.test_check_domain("http://www.github.com", "www.github.com"), bool)
    assert cmt.test_check_domain("http://www.github.com", "www.com") is False
    assert cmt.test_check_domain("http://www.github.com", "http://www.github.com") is True
    assert cmt.test_check_domain("http://github.com", "http://github.com/pulls") is True

    print("Passed All Test cases.")
