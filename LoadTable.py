
from sqlalchemy import create_engine
from sqlalchemy import MetaData
import CreateTable as db
from sqlalchemy.orm import sessionmaker

'''
class URLTask(Base):
	__tablename__ = 'URLTask'
	url_id = Column(Integer, primary_key=True)
	url = Column(String(length=2038))
	timestamp = Column(Integer)
	duration = Column(Integer)
	status = Column(SmallInteger)
	pirority = Column(SmallInteger)


class URLText(Base):
	__tablename__ = 'URLText'
	url_id = Column(Integer, primary_key=True)
	timestamp = Column(Integer)
	text = Column(Text)
'''




db_uri = 'mysql+pymysql://root:Ace1997!@localhost:3306/Crawler'
engine = create_engine(db_uri)
# metadata = MetaData()
# metadata.reflect(bind=engine)
#print(metadata.tables)


Session = sessionmaker()
Session.configure(bind=engine)

with db.session_scope() as session:
    row = session.query(db.URLTask).filter(db.URLTask.url_id == 1).first()
    print('Retrieving: ', row.url_id, row.url)


# try:
# 	row = db.URLTask( url_id=0,
# 		           url='www.google.com',
# 		           timestamp=0,
# 		           duration=1,
# 		           status=2,
# 		           priority=1 )
# 	session.add(row)
# 	session.commit()
#
# 	row = session.query(db.URLTask).filter( db.URLTask.url_id == 0 ).first()
# 	print('original: ', row.url_id, row.url)
#
# except SQLAlchemyError as e:
# 	print(e)
#
# finally:
# 	session.close()





