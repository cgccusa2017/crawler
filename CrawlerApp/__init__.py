from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# Initial set up for data base and crawlers

db_uri = 'mysql+pymysql://root:<password>@localhost:3306/Crawler'
engine = create_engine(db_uri)
Session = sessionmaker()
Session.configure(bind=engine)

