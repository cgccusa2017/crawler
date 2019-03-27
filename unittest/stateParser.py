import sys
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
__package__='crawler'
from CrawlerApp import CrawlerWorker
from CrawlerApp import TextProcessor
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import pandas as pd

from time import sleep
import csv
import os



def crawl_state_link(root, quota=1000):

    tp = TextProcessor.TextProcessor()
    crawler = CrawlerWorker.Crawler()
    visited = set()
    url_list = [root]

    while url_list:
        curr_url = url_list.pop(0)
        visited.add(curr_url)

        crawler_response = crawler.crawl(curr_url)
        if crawler_response[1] != 200:
            return

        response = crawler_response[2]
        soup = BeautifulSoup(response, 'html.parser')

        for script in soup(["script", "style"]):
            script.extract()    # remove java script and style in html

        for a in soup.find_all('a'):
            if a.has_attr('href'):
                new_url = tp.is_valid_url(curr_url, a['href'])
                if new_url and tp.check_same_domain(curr_url, new_url):
                    if new_url[-1] == '/':
                        new_url = new_url[:-1]

                    if new_url not in visited and not new_url.endswith('.pdf'):
                        url_list.append(new_url)
                        visited.add(new_url)
                        if len(visited) == quota:
                            return list(visited)
    return list(visited)


def crawl_individual_state(url):
    """
    This function is used to get text and urls for a specific state website.
    :param url: url of the state
    :return:
    """

    tp = TextProcessor.TextProcessor()
    crawler = CrawlerWorker.Crawler()
    crawler_response = crawler.crawl(url)
    if crawler_response[1] != 200:
        return

    response = crawler_response[2]
    soup = BeautifulSoup(response, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract() # remove java script and style in html

    links = set()
    for a in soup.find_all('a'):
        new_url = tp.is_valid_url(url, a['href'])
        if new_url and tp.check_same_domain(url, new_url):
            if new_url[-1] == '/':

                new_url = new_url[:-1]

            links.add(new_url)
        del a['href']

    text = soup.get_text()
    return links, text


def save_text(state_link):
    crawler = CrawlerWorker.Crawler()

    for key, value in links.items():
        state_name = key.replace(" ", "")
        state_link = value
        state_file_name = state_name+'_text.txt'
        f = open(state_file_name, 'a')

        for url in state_link:
            crawler_response = crawler.crawl(url)
            if crawler_response[1] != 200:
                return
            response = crawler_response[2]
            soup = BeautifulSoup(response, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract() # remove java script and style in html

            for a in soup.find_all('a'):
                del a['href']

            text = soup.get_text()
            f.write(text)


    for curr_url in links:
        crawler_response = crawler.crawl(curr_url)
        if crawler_response[1] != 200:
            return

        response = crawler_response[2]
        soup = BeautifulSoup(response, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract() # remove java script and style in html

        for a in soup.find_all('a'):
            del a['href']

        text = soup.get_text()
        return text



def read_csvfile(file_name):
    state_link = {}
    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        for row in readCSV:

            if row[1]:
                name = row[0].replace(" ", "").lower()
                state_link[name] = row[1]

    return state_link



if __name__ == "__main__":

    ny_link = "https://esd.ny.gov/"
    #get_individual_state_text("NewYork")
    state_link = read_csvfile('state-url.csv')


    # links, text = crawl_individual_state(state_link['New York'])
    # for l in links:
    #     print(l)

    #save_text(state_link)

    # first store links of each state into different files
    # ny_links = crawl_state_link(ny_link)
    # for l in ny_links:
    #     print(l)

    for key, value in state_link.items():
        link_path = 'crawl_states_data/' + key + '_links.txt'
        link_file = open(link_path, 'a')
        url_list = crawl_state_link(value)
        if url_list:
            for l in url_list:
                link_file.write(l)



