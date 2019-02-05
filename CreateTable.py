

import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import Column, ForeignKey, Integer, String, SmallInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import MetaData

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager

@contextmanager
def session_scope():
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
class URLTask(Base):
	__tablename__ = 'URLTask'
	url_id = Column(Integer, primary_key=True)
	url = Column(String(length=2038), nullable=False)
	timestamp = Column(Integer)
	duration = Column(Integer)
	status = Column(SmallInteger)
	priority = Column(SmallInteger)

	def __str__(self, ):
		return self.url_id

	def get_url():
		return self.url

	def get_timestamp():
		return self.timestamp
	
	def get_duration():
		return self.duration

	def update_duration():
		pass
	
	def get_status():
		return self.status
	
	def get_priority():
		return self.priority
	
	def __lt__(self, other):
		return self.priority < other.priority



class URLText(Base):
	__tablename__ = 'URLText'
	text_id = Column(Integer, primary_key=True)
	url_id = Column(Integer, ForeignKey('URLTask.url_id'), nullable=False)
	timestamp = Column(Integer)
	text = Column(Text, nullable=False)

	def __str__(self, ):
		return self.url_id

	def get_timestamp():
		return self.timestamp

	def get_text():
		return self.text



db_uri = 'mysql+pymysql://root:Ace1997!@localhost:3306/Crawler'
engine = create_engine(db_uri)

Base.metadata.create_all(engine, checkfirst=True)

for _t in Base.metadata.tables:
	print(_t)


# Session = sessionmaker()
# Session.configure(bind=engine)
# session = Session()


# with session_scope() as session:
# 	task_row = URLTask( url_id=1, 
# 						url='www.google.com', 
# 						timestamp=0,
# 						duration=1,
# 						status=2,
# 						priority=1 )

# 	text_row = URLText( text_id=1, 
# 						url_id=1,
# 						timestamp=20190204,
# 						text='Try to see if ForeignKey works')
# 	session.add(task_row)
# 	session.add(text_row)
# 	session.commit()


# with session_scope() as session:
# 	row = session.query(URLTask).filter( URLTask.url_id == 1 ).first()
# 	print('Retrieving: ', row.url_id, row.url)


