from bs4 import BeautifulSoup as Soup
import re
from urllib.parse import urlparse


class TextProcessor:
    """
    This class handles text processing.
    """

    def __init__(self):
        # set relevance score = 0 by default
        self.threshold = 0

    def check_same_domain(self, origin_url, new_url):
        old_domain = urlparse(origin_url).netloc
        new_domain = urlparse(new_url).netloc
        if old_domain == new_domain:
            return True
        return False

    def separate_url_text(self, origin_url, url_content, keyword=None):
        """
        This function will separate url and text from the original url content.
        :param origin_url: the original url that will be processed, to check if the new url links found inside is the same domain as the original url.
        :param url_content: the content in the url.
        """
        # Initialize a set (handles uniqueness) to store all url links found in the origin_url. 
        url_links = set()
        text = Soup(url_content, 'html.parser')

        for a in text.find_all('a'):
            # check for url's relevance
            if keyword and self.check_relevance(url_content, keyword) < self.threshold:
                continue
            else:
                # Check if the url is a valid url.
                curr_url = self.is_valid_url(origin_url, a['href'])

                # If valid, add to the set.
                if curr_url is not None:
                    url_links.add(curr_url)

            # Delete the newly found url from the url content after processing. 
            del a['href']

        # Return the list of urls and the text found in the origin_url.
        return url_links, text


    def add_domain(self, origin_url, broken_url):
        """
        This function add netloc to the broken url and return the new url
        :param origin_url:
        :param broken_url: 
        :return: the newly constructed url (after adding the netloc).
        """
        # Get the domain using urlparse.
        obj = urlparse(origin_url)
        domain = obj.netloc

        if domain == "":
            return ""
        else:
            return "http://"+ domain + broken_url


    def is_valid_url(self, origin_url, url):
        """
        This function will check if a url is valid or not.
        :param: url: the url to validate
        :return: True if valid, False if invalid.
        :return: The url if it is valid, or None if invalid
        """

        # The regex for validating url.
        regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        # If passed the regex test, return.
        if (url is not None) and (regex.search(url) is not None):
            return url
        else:
            # If didn't pass the regex, first try adding netloc:
            new_url = self.add_domain(origin_url, url)
            # return if passed the regex after added the netloc.

            if (new_url is not None) and (regex.search(new_url) is not None):
                return new_url

        # Handles the case that missing http or https in front of the url.
        if new_url == "":
            new_url = "http://" + url
            if (new_url is not None) and (regex.search(new_url) is not None):
                return new_url

            new_url = "https://" + url

            if (new_url is not None) and (regex.search(new_url) is not None):
                return new_url

        return None

    # TODO: handle keywords here, calculate the relevance of a url's content(given the keyword)
    def check_relevance(self, url_content, keyword):
        return 0


    def calculate_priority(self, url_content):
        pass
