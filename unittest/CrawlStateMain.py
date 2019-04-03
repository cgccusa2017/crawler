import sys
import os
from os.path import dirname
sys.path.append(dirname(sys.path[0]))
__package__='crawler'
from CrawlerApp import CrawlerWorker
from CrawlerApp import TextProcessor
import collections
from bs4 import BeautifulSoup
import CrawlerApp.CrawlerModel as db
from sqlalchemy.exc import SQLAlchemyError
from time import sleep
import csv
import pandas as pd


class CrawlStateMain:

    def __init__(self):
        self.tp = TextProcessor.TextProcessor()
        self.crawler = CrawlerWorker.Crawler()

    def main(self):
        pass


    def crawl(self, ):
        pass

    def crawl_link(self, root, quota=100):
        """
        This function recursively get all distinct links from root urls
        :param root:
        :param quota: maximum number of urls to get
        :return: list of urls
        """
        visited = set()
        url_list = collections.deque([root])

        while url_list:

            curr_url = url_list.popleft()

            crawler_response = self.crawler.crawl(curr_url)
            if crawler_response[1] != 200:
                continue

            visited.add(curr_url)
            response = crawler_response[2]
            soup = BeautifulSoup(response, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()    # remove java script and style in html

            for a in soup.find_all('a'):
                if a.has_attr('href'):
                    new_url = self.tp.is_valid_url(curr_url, a['href'])
                    if new_url and self.tp.check_same_domain(curr_url, new_url):
                        if new_url[-1] == '/':
                            new_url = new_url[:-1]

                        if new_url not in visited and not new_url.endswith('.pdf'):
                            url_list.append(new_url)
                            visited.add(new_url)

                        if len(visited) == quota:
                            return list(visited)

        return list(visited)


    def crawl_text(self, url):
        """
        Return the text we crawled from a url
        :param url:
        :return: all text in the url
        """
        # simply return all text from url
        crawler_response = self.crawler.crawl(url)
        if crawler_response[1] != 200:
            return None

        response = crawler_response[2]
        soup = BeautifulSoup(response, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()    # remove java script and style in html

        for a in soup.find_all('a'):
            if a.has_attr('href'):
                del a['href']

        text = soup.get_text()
        return text


    def save_text(self, file_path):
        # open each file in the directory
        for file in os.listdir(file_path):

            # for each file, build '<state_name>_text.txt'
            state_name = file.split('_')[0]
            print(state_name)
            new_file = 'crawl_states_data/'+state_name+'_text.txt'

            state_text = open(new_file, 'a')

            file = 'crawl_states_data/' + file

            try:
                stream = open(file, 'r', encoding='utf-8')
                for line in stream:
                    print(line)
                    curr_text = self.crawl_text(line)
                    if curr_text:
                        state_text.write(curr_text)
                    state_text.write('\n')

            except IOError:
                continue

            except UnicodeDecodeError:
                continue

            else:
                stream.close()

            # with open(file, 'r') as state_links:
            #     # for each state, read url line by line, store into
            #
            #     for line in state_links:
            #
            #         print(line)
            #         curr_text = self.crawl_text(line)
            #         if curr_text:
            #             state_text.write(curr_text)
            #         state_text.write('\n')
            state_text.close()




# To initialize all tables, run "Python CrawlerModel.py"
if __name__ == '__main__':

    cw = CrawlStateMain()
    file_path = 'crawl_states_data'
    cw.save_text(file_path)



    #
    # # TODO: build a DB model to store links (state name, link)
    # def save_link(self, state_name, url_list, db_name):
    #     with db.session_scope() as session:
    #         while url_list:
    #             try:
    #                 curr_url = url_list.pop()
    #                 row = db.db_name(
    #                     state_name = state_name,
    #                     url = curr_url)
    #                 session.add(row)
    #             except SQLAlchemyError as e:
    #                 return -1
    #         session.commit()
    #     return 0
    #
    #
    #
    # def default_hash(self, url):
    #     """
    #     Default hash function to create file path for url
    #     :param url:
    #     :return:
    #     """
    #     return str(hash(url))
    #
    # def create_file_path(self, url, hash_func=default_hash, format='.h5'):
    #     return hash_func(url)+format
    #
    #
    # # TODO: iterate over the url table, save text of the url in h5 format
    # def save_text(self, db, quota):
    #     # quota: controls how many links
    #     # (1) open db model, get link from model
    #     with db.session_scope() as session:
    #         try:
    #             row = session.query(db.URLTask)

    # # TODO: append text to data frame
    # def save_text(self, state_name, url, text, df):
    #     new_row = pd.DataFrame({"state_name":state_name, "url":url, "text":text})
    #     df.append(new_row)
    #
    # # TODO: convert a dataframe (with set # of rows) to hdf5 format
    # def save_df_to_file(self, df, file_name):
    #     df.to_hdf(file_name, key='df', mode='a')
    #     pass
    #
    # # TODO:
    # def create_hdf_path(self, state_name, ):
    #     pass







