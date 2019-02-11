from bs4 import BeautifulSoup as Soup


class TextProcessor:

    def __init__(self):
        # set relevance score = 0 by default
        self.threshold = 0

    def separate_url_text(self, url_content, keyword=None):
        links = set()
        text = Soup(url_content, 'html.parser')


        for a in text.find_all('a'):

            if keyword and self.check_relevance(url_content, keyword) < self.threshold:
                continue
            else:
                links.add(a['href'])

            del a['href']

        return links, text


    # TODO: handle keywords here, calculate the relevance of a url's content(given the keyword)
    def check_relevance(self, url_content, keyword):
        return 0
