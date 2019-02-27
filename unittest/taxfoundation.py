import sys
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
__package__='crawler'
from CrawlerApp import CrawlerWorker

from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep

def get_individual_state_tax(state_name):
    """
    This function is used to get information for a specific state.
    :param state_name: the state name
    :return: a dictionary containing all tax info about this state.
    """
    url = "https://taxfoundation.org/state/{}/".format(state_name)
    crawler = CrawlerWorker.Crawler()
    crawler_response = crawler.crawl(url)
    if crawler_response[1] != 200:
        return

    response = crawler_response[2]
    bs_obj = BeautifulSoup(response, 'html.parser')
    tabs = bs_obj.find('div', class_='state-tabs padded width-constrained')
    label_map = dict()
    for idx, label in enumerate(tabs.find_all('label')):
        label_map[idx] = label.get_text()

    data = dict()
    data['State Name'] = state_name

    for idx, section in enumerate(tabs.find_all('section')):

        for card in section.find_all('div', class_='cards__state-card'):

            header = card.find('div', class_='cards__state-card-header').get_text().strip()
            curr_card = card.find('div', class_='cards__state-card-content')
            check_content = curr_card.find('h1')

            if not check_content:
                check_content = curr_card.find('p', class_='text--h3')
                content = check_content.get_text()
            else:
                content = check_content.get_text().strip()

            data[header] = content

    return data


def get_state_name(url):
    """
    This function gets all states name from the website https://taxfoundation.org
    :param url: the url https://taxfoundation.org/
    :return: list of states in the url
    """
    states = []

    crawler = CrawlerWorker.Crawler()
    crawler_response = crawler.crawl(url)
    if crawler_response[1] != 200:
        return

    sleep(0.1)

    response = crawler_response[2]
    bs_obj = BeautifulSoup(response, 'html.parser')

    options = bs_obj.find('div', class_='state-widget').find_all('option')

    for opt in options:
        curr_opt = opt.get_text()
        curr_opt = re.sub("\s+", "-", curr_opt.strip())
        states.append(curr_opt)
    return states



if __name__ == "__main__":

    url = "https://taxfoundation.org/"
    states = get_state_name(url)

    data = []
    for s in states:
        data.append(get_individual_state_tax(s))

    column = set()
    for d in data:
        for k, v in d.items():
            column.add(k)
            if "&percnt;" in v:
                d[k] = v.strip("&percnt;") + "%"
            if "&dollar;" in v:
                d[k] = v.strip("&dollar;") + "$"

    data = pd.DataFrame(data)
    data.to_csv("data.csv", na_rep="None")





