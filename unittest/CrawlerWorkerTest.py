
import sys
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
__package__='crawler'
from CrawlerApp import CrawlerWorker

import unittest









class CrawlerWorkerTest(unittest.TestCase):
    """
    This is the unit test for Crawler Worker.
    """
    def __init__(self):
        self.crawler = CrawlerWorker.Crawler()

    def test_crawl(self, target_url):
        """
        This function tests the crawl() function in Crawler class.
        """
        return self.crawler.crawl(target_url)




if __name__ == "__main__":
    ct = CrawlerWorkerTest()
    
    print("Testing CrawlerWorker...")

    assert len(ct.test_crawl("www.github.com")) == 3
    assert isinstance(ct.test_crawl("http://www.github.com")[0], str)
    assert ct.test_crawl("..com")[1] == -1
    assert isinstance(ct.test_crawl("www.github.com")[2], str)
    assert ct.test_crawl("www..com")[2] is None
    
    print("Passed All Test cases.")

