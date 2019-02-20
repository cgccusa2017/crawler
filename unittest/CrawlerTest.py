
import sys
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
__package__='crawler'
from CrawlerApp import CrawlerWorker

import unittest









class CrawlerTest(unittest.TestCase):

    def __init__(self):
        self.crawler = CrawlerWorker.Crawler()

    def test_crawl(self, target_url):
        return self.crawler.crawl(target_url)






if __name__ == "__main__":
    ct = CrawlerTest()
    print("Testing CrawlerWorker...")
    assert len(ct.test_crawl("www.github.com")) == 3
    assert isinstance(ct.test_crawl("http://www.github.com")[0], str)
    assert ct.test_crawl("..com")[1] == -1
    assert isinstance(ct.test_crawl("www.github.com")[2], str)
    assert ct.test_crawl("www..com")[2] is None
    print("Passed All Test cases.")

