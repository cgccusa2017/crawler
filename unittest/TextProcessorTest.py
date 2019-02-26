


import sys
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
__package__='crawler'
from CrawlerApp import TextProcessor
import unittest


class TextProcessorTest(unittest.TestCase):
    """
    This is the unit test for Text Processor.
    """

    def __init__(self):
        self.tp = TextProcessor.TextProcessor()


    def test_add_domain(self, origin_url, broken_url):
        return self.tp.add_domain(origin_url, broken_url)


    def test_is_valid_url(self, origin_url, url):
        pass



if __name__ == "__main__":
    tpt = TextProcessorTest()
    print("Testing TextProcessor...")
    assert tpt.test_add_domain("", "") == ""
    assert tpt.test_add_domain("http://github.com", "") == "http://github.com"
    print("Passed All Test cases.")
