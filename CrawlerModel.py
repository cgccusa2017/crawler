import pymysql

pymysql.install_as_MySQLdb()
from sqlalchemy import Column, ForeignKey, Integer, String, SmallInteger, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager
import time

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
db_uri = 'mysql+pymysql://root:Ace1997!@localhost:3306/Crawler'
engine = create_engine(db_uri)


class URLTask(Base):
    __tablename__ = 'URLTask'
    url_id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(length=2038), nullable=False)
    # Shall we store DateTime instead?
    timestamp = Column(Integer)
    duration = Column(Integer)
    # unit: millisecond
    # TODO: exponential back-off

    # TODO: how to get next duration, and update status
    status = Column(SmallInteger)
    # 1: available, 2: idle, 0: fail

    priority = Column(SmallInteger)
    # TODO: use text processor to calculate, or based on user-defined value

    available_time = Column(Integer)
    # timestamp + duration

    def __str__(self, ):
        return str(self.url_id)

    def get_id(self):
        return self.url_id

    def get_url(self):
        return self.url

    def get_timestamp(self):
        return self.timestamp

    def get_duration(self):
        return self.duration

    def update_duration(self):
        pass

    def get_status(self):
        return self.status

    def get_priority(self):
        return self.priority

    def get_available_time(self):
        return self.available_time

    def set_timestamp(self, time):
        self.timestamp = time

    def set_available_time(self, time):
        self.available_time = time + self.duration

    def __lt__(self, other):
        return self.priority < other.priority


class URLText(Base):
    __tablename__ = 'URLText'
    text_id = Column(Integer, primary_key=True, autoincrement=True)
    url_id = Column(Integer, ForeignKey('URLTask.url_id'), nullable=False)
    timestamp = Column(Integer)
    text = Column(Text, nullable=False)

    def __str__(self, ):
        return str(self.url_id)

    def get_timestamp(self):
        return self.timestamp

    def get_text(self):
        return self.text


# This table store the users' name
class UserList(Base):
    __tablename__ = 'UserList'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=2038), nullable=False)

    def __str__(self, ):
        return str(self.id)


# This table contains user ID and their url task id.
class UserTask(Base):
    __tablename__ = 'UserTask'
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('UserList.uid'))
    url_id = Column(Integer, ForeignKey('URLTask.url_id'), nullable=False)
    timestamp = Column(Integer)

    def __str__(self, ):
        return str(self.user_id)

    def get_task(self):
        return self.url_id


# This table stores the quota of the websites we can crawl from certain domain
class DomainQuota(Base):
    __tablename__ = 'DomainQuota'
    domain_id = Column(Integer, primary_key=True, autoincrement=True)
    domain_name = Column(String(length=2038), nullable=False)
    quota = Column(Integer, default=1000)



if __name__ == '__main__':
    Base.metadata.create_all(bind=engine, checkfirst=True)
    print("Tables in database:")
    for _t in Base.metadata.tables:
        print(_t)

