import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import Column, ForeignKey, Integer, String, SmallInteger, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import time

# This blocks handle the database accessing
@contextmanager
def session_scope():
    Session = sessionmaker()
    Session.configure(bind=engine)

    """Provide a transactional scope around a series of operations."""
    session = Session(expire_on_commit=False)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


Base = declarative_base()
# the path to db
db_uri = 'mysql+pymysql://root:<password>@localhost:3306/Crawler'
engine = create_engine(db_uri)


class URLTask(Base):
    """
    This class initialize URLTask table.
    The URLTask table stores the url that are waiting to be crawled.
    """
    __tablename__ = 'URLTask'
    url_id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(length=2038), nullable=False)

    # timestamp: the time when put in the url task
    timestamp = Column(Integer)
    
    # TODO: get update duration
    duration = Column(Integer)
    # unit: millisecond
    # TODO: exponential back-off

    # TODO: handle status update
    status = Column(SmallInteger)
    # 1: available, 2: idle, 0: fail

    # TODO: use text processor to calculate, or based on user-defined value
    priority = Column(SmallInteger)
    
    # available_time: next available time to crawl this url
    available_time = Column(Integer)
    # timestamp + duration

    def __str__(self, ):
        return str(self.url_id)

    def get_id(self):
        """
        This function returns the url_id of current entry in the table.
        """
        return self.url_id

    def get_url(self):
        """
        This function returns the url of current entry in the table.
        """
        return self.url

    def get_timestamp(self):
        """
        This function returns time stamp of current entry in the table.
        """
        return self.timestamp

    def get_duration(self):
        """
        This function returns duration of current entry in the table.
        """
        return self.duration

    def get_status(self):
        """
        This function returns the status of current entry in the table.
        """
        return self.status

    def get_priority(self):
        """
        This function returns the priority of current entry in the table.
        """
        return self.priority

    def get_available_time(self):
        """
        This function returns the available time of current entry in the table.
        """
        return self.available_time

    def __lt__(self, other):
        """
        Handles comparison between two entries.
        """
        return self.priority < other.priority


class URLText(Base):
    """
    This class initialize URLText table.
    The URLText table stores the text that crawls from the url.
    """
    __tablename__ = 'URLText'
    text_id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey('URLTask.url_id'), nullable=False)
    timestamp = Column(Integer)
    # TODO: store filepath instead of raw text
    text = Column(Text, nullable=False)

    def __str__(self, ):
        return str(self.url_id)

    def get_timestamp(self):
        """
        This function returns time stamp of current entry in the table.
        """
        return self.timestamp

    def get_text(self):
        """
        This function returns the file path of current entry in the table.
        """
        return self.text


class UserList(Base):
    """
    This class initialize UserList table to store users' name.
    """
    __tablename__ = 'UserList'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=2038), nullable=False)

    def __str__(self, ):
        return str(self.id)


class UserTask(Base):
    """
    This class initialize UserTask table to store user id and their url tasks.
    """
    __tablename__ = 'UserTask'
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('UserList.uid'))
    url_id = Column(Integer, ForeignKey('URLTask.url_id'), nullable=False)
    timestamp = Column(Integer)

    def __str__(self, ):
        return str(self.user_id)

    def get_task(self):
        """
        This function returns the url task id of current entry in the table.
        """
        return self.url_id


class DomainQuota(Base):
    """
    This class initialize table to stores the quota of the websites that allowed to crawl from certain domain.
    """
    __tablename__ = 'DomainQuota'

    domain_id = Column(Integer, primary_key=True, autoincrement=True)
    # domain name
    domain_name = Column(String(length=2038), nullable=False)
    # maximum number to crawl from certain domain
    quota = Column(Integer, default=1000)


# To initialize all tables, run "Python CrawlerModel.py"
if __name__ == '__main__':
    Base.metadata.create_all(bind=engine, checkfirst=True)
    print("Tables in database:")
    for _t in Base.metadata.tables:
        print(_t)




