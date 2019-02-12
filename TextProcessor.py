from bs4 import BeautifulSoup as Soup
import re
from urllib.parse import urlparse


class TextProcessor:

    def __init__(self):
        # set relevance score = 0 by default
        self.threshold = 0

    def separate_url_text(self, origin_url, url_content, keyword=None):
        links = set()
        text = Soup(url_content, 'html.parser')

        for a in text.find_all('a'):

            if keyword and self.check_relevance(url_content, keyword) < self.threshold:
                continue
            else:
                curr_url = self.is_valid_url(origin_url, a['href'])
                if curr_url is not None:
                    links.add(curr_url)
            del a['href']

        return links, text

    def add_domain(self, origin_url, broken_url):
        """
        This function add netloc to the broken url and return the new url
        :param origin_url:
        :param broken_url:
        :return:
        """

        obj = urlparse(origin_url)
        domain = obj.netloc

        if domain == "":
            return ""
        else:
            return origin_url + broken_url[1:]

    def is_valid_url(self, origin_url, url):
        """
        This function will check if a url is valid or not.
        :param: url: the url to validate
        :return: True if valid, False if invalid.
        :return: The url if it is valid, or None if invalid
        """

        regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if (url is not None) and (regex.search(url) is not None):
            return url
        else:
            # try adding netloc
            new_url = self.add_domain(origin_url, url)

            if (new_url is not None) and (regex.search(new_url) is not None):
                return new_url

        return None

    # TODO: handle keywords here, calculate the relevance of a url's content(given the keyword)
    def check_relevance(self, url_content, keyword):
        return 0
