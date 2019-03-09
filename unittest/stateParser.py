import sys
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
__package__='crawler'
from CrawlerApp import CrawlerWorker

from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep


def get_individual_state_text(state_name):
    """
    This function is used to get text for a specific state.
    :param state_name:
    :return:
    """

    url = "https://esd.ny.gov/"
    crawler = CrawlerWorker.Crawler()
    crawler_response = crawler.crawl(url)
    if crawler_response[1] != 200:
        return

    response = crawler_response[2]
    soup = BeautifulSoup(response, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    for a in soup.find_all('a'):
        del a['href']

    text = soup.get_text()

    print(text)

def get_all_links(state_name):


if __name__ == "__main__":
    get_individual_state_text("NewYork")

