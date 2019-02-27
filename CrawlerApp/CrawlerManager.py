from sqlalchemy.exc import SQLAlchemyError
import requests
import time
from urllib.parse import urlparse
from CrawlerApp.__init__ import Session
from CrawlerApp import TextProcessor
import CrawlerApp.CrawlerModel as db
import CrawlerApp.CrawlerWorker as Crawler
from CrawlerApp import TaskQueue
from pybloom import ScalableBloomFilter



class CrawlerManager:
    """
    Central component of this Crawler Application.
    This class used to coordinates Crawlers and Text Processors. Also, handles 
    results collection, data storage after the Crawling task complete.
    """

    def __init__(self, state=1, task_queue=None):
        """
        :param state: 1 active, 0 inactive, 2 wait, 3 error
        :param task_queue: the crawling task waiting to be processed.
        """

        self.state = state # manager's state to detect error during crawl
        self.session = Session() # Session for accessing database
        self.tp = TextProcessor.TextProcessor() # Text processor

        # bloomfilter to check url task uniqueness before update db
        self.sbf = self.init_bloom_filter() 


        if not task_queue:
            self.task_queue = TaskQueue.TaskQueue()
        else:
            self.task_queue = task_queue


    def __del__(self):
        """
        Close the db session when done.
        """
        self.session.close()


    def init_bloom_filter(self, userID=None):
        """
        This function builds a bloom filter for urls based on user id's.
        :param userID: if None, put all url task from db into bloom filter.
        :return: bloom filter object
        """

        # initialize bloom filter
        sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
        # initialize a list to store urls
        urls = []

        with db.session_scope() as session:

            if userID:
                # if specified user id, put current user's url tasks into bloom filter
                url_id_list = session.query(db.UserTask.url_id).\
                                      filter(db.UserTask.user_id == userID).all()
                for uid in url_id_list:
                    urls.append(session.query(db.URLTask.url).filter(db.URLTask.url_id == uid))
            else:
                # if no user id, put all url tasks into bloom filter
                urls = session.query(db.URLTask.url).all()

        # add all urls to bloom filter
        for i in range(len(urls)):
            sbf.add(urls[i][0])

        # return the bloom filter object
        return sbf


    def get_url(self):
        """
        This function will query the task table, which sort by the available time 
        ( need to be less than current time to be able to crawl ).        
        Use Priority to break tie. (High Priority goes first when tie on available time).

        :return: the next url to crawl, and the corresponding url_id
        """

        # open the database
        with db.session_scope() as session:

            curr_time = time.time()
            try:
                # query url tasks table, order by ascending avialable time and descending priority
                url = session.query(db.URLTask).\
                    order_by(db.URLTask.available_time, db.URLTask.priority.desc()).\
                    first()

                # if there is url in the task table
                if url:
                    # get the available time of this url
                    url_time = url.get_available_time()

                    # check if available time less than current time
                    if url_time < curr_time:

                        # update the next available time and timestamp
                        url.set_timestamp(curr_time)
                        url.set_available_time(curr_time)

                        # return the url if available time is valid
                        return url.get_url(), url.get_id()

                # return if the table is empty
                else:
                    print("Task table is empty")
                    return None, -1

            # handle database exceptions
            except SQLAlchemyError as e:
                print(e)
                return None, -1

        return None, -1



    def process_text(self, origin_url, url_content, keyword=None):
        """
        This function separate links and text content from the url_content.
        :param: origin_url: the url to process.
        :return: links: all links found in the origin_url
        :return: text: text in the original_url after removing the links
        """
        links, text = self.tp.separate_url_text(origin_url, url_content, keyword)
        return links, text


    # TODO: the async haven't implemented
    def start_crawl(self, crawler, url, url_id, crawler_settings=None):
        """
        This function starts a crawler.
        :param crawler: the crawler worker
        :param origin_url: the seed url
        :param url_id: the seed url's id
        :param crawler_settings: a dictionary contains header {}, form_data {}
        :return: nothing to return, update the url_task and url_text table
        """

        # # get the next url to crawl, store the url_id for later updating urlText table
        # origin_url, url_id = self.get_url()
        #
        # if not origin_url or url_id == -1:
        #     time.sleep(1)
        #     origin_url, url_id = self.get_url()

        self.task_queue.async(crawler, parameters=(url, url_id, crawler_settings))
        # origin_url, code, url_content = crawler.crawl(origin_url, crawler_settings)



    # TODO: find task_queue, see which task finished; get the finished task and update table
    def collect_result(self):

        url_lst, code_lst, content_lst = self.task_queue.collect()

        for (url, code, content) in zip(url_lst, code_lst, content_lst):
            self._collect_result(url, code, content)

    # TODO: similar to collect_result
    def _collect_result(self, url, code, url_content):
        """
        This function update the url_task and url_text table
        :param self:
        :param url:
        :param code:
        :param url_content:
        :return:
        """
        # if able to open the url, get links and texts from it
        if code == requests.codes.ok:
            # get text and put into urlText
            # get links

            url_lists, text = self.process_text(url, url_content)

            if text:
                url_id = self.get_url_id(url)
                if url_id == -1:
                    return -1
                # store text from url into table
                state = self.update_url_text_table(url_id, text)

                # if updating not success
                if state == -1:
                    print("Error: cannot update the URL_TEXT table")
                    return -1

            if url_lists:
                state = self.update_url_task_table(url, url_lists)

                # if updating not success
                if state == -1:
                    print("Error: cannot update the URL_TASK table")
                    return -1

        else:
            print("Error: cannot open current url")
            return -1

        #print("Update Successfully")
        return 0


    
    def get_url_id(self, url):
        """
        This function returns the url id from db by the given url.
        :param url: the url we want to find the id
        """
        with db.session_scope() as session:
            try:
                # query db using url
                curr_row = session.query(db.URLTask).filter(db.URLTask.url == url).first()
                url_id = curr_row.get_id()

            # handle database exceptions
            except SQLAlchemyError as e:
                print(e)
                return -1

            # if no such url exists in db
            if not url_id:
                return -1

            return url_id

    def update_url_text_table(self, url_id, text, filepath_generator):
        """
        This function store information into url text table.

        :param url_id: the url_id from url task table
        :param text:
        :return: 0 if successfully updating row in the table, -1 if failed
        """
        text = "Testing Mode"


        filepath = filepath_generator(url_id)
        # TODO: open specific file path and store text into the path
        # TODO: store the file path into db

        # check whether the text is updated
        # if true
        # # update the url updating frequency

        with db.session_scope() as session:

            try:
                # try query using url_id
                row = session.query(db.URLText).filter(db.URLText.url_id == url_id).first()

                if row is None:
                    curr_time = time.time()
                    row = db.URLText(
                        url_id=url_id,
                        timestamp=curr_time,
                        text=text
                    )
                    session.add(row)
                else:
                    row.text = text

                session.commit()
                # print("Success: Updating url text table")

            # handle database exceptions
            except SQLAlchemyError as e:
                print(e)
                return -1

        return 0


    def update_url_task_table(self, origin_url, url_lists):
        """
        This function enqueue newly found urls into task table
        :param origin_url: the original url, for domain checking
        :param url_lists: list of urls
        :return: 0 success, -1 failure
        """
        duration = 1
        
        with db.session_scope() as session:

            # while there are still url in the url lists
            while url_lists:
                try:
                    # get url from lists 
                    curr_url = url_lists.pop()

                    # check if current url is the same domain as the original url
                    # in order to avoid not important url (e.g.: advertisement link)
                    if self.check_domain(origin_url, curr_url):

                        # try to add the url to the bloom filter
                        if curr_url not in self.sbf:

                            # get current time
                            curr_time = time.time()

                            # create new entry to put in URL Task table
                            row = db.URLTask(
                                url=curr_url,
                                timestamp=curr_time,
                                duration=duration,
                                available_time=curr_time+duration
                            )

                            # adding new row to db
                            session.add(row)
                            # add to bloomfilter
                            self.sbf.add(curr_url)
                    session.commit()
                
                # handle database exceptions
                except SQLAlchemyError as e:
                    print(e)
                    return -1
        # successfully updated the db
        return 0


    def check_domain(self, origin_url, new_url):
        """
        This function check if the new url comes from the same domain as the original one
        :param origin_url: the seed url
        :param new_url: the new url to check
        :return: True if same domain, False otherwise.
        """

        origin_obj = urlparse(origin_url)
        new_obj = urlparse(new_url)

        return origin_obj.netloc == new_obj.netloc


if __name__ == "__main__":

    cm = CrawlerManager()
    crawler = Crawler.Crawler()
    url, url_id = cm.get_url()
    print(url, "\t", url_id)

    #url, code, url_content = crawler.crawl(url)


    """
    #  cm.start_crawl(crawler, origin_url, url_id)
    distributed_Queue(cm.start_crawl(crawler, origin_url, url_id))
    distributed_Queue(cm.start_crawl(crawler, origin_url, url_id))

    distributed_queue.dispatch(crawler1.crawl(url))
    distributed_queue.dispatch(crawler2.crawl(url))
    distributed_queue.dispatch(crawler3.crawl(url))
    distributed_queue.dispatch(crawler4.crawl(url))
    distributed_queue.dispatch(crawler5.crawl(url))
    distributed_queue.dispatch(crawler.crawl(url))
    distributed_queue.dispatch(crawler.crawl(url))
    distributed_queue.dispatch(crawler.crawl(url))

    for res in results:
        cm.update(res)
    """

