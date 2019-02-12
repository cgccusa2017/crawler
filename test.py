import CrawlerModel as db
from sqlalchemy.exc import SQLAlchemyError
import Crawler
import CrawlerManager
import TextProcessor

'''
with db.session_scope() as session:
	task_row = URLTask( url_id=1, 
						url='www.google.com', 
						timestamp=0,
						duration=1,
						status=2,
						priority=1 )

	text_row = URLText( text_id=1, 
						url_id=1,
						timestamp=20190204,
						text='Try to see if ForeignKey works')
	session.add(task_row)
	session.add(text_row)
	session.commit()

'''
"""
This piece of code retrieves a row successfully
with db.session_scope() as session:
    row = session.query(db.URLTask).filter(db.URLTask.url_id == 1).first()
    print('Retrieving: ', row.url_id, row.url)
"""

"""
with db.session_scope() as session:
    try:
        row = session.query(db.URLText).filter(db.URLText.url_id == 1).first()

        if row is None:
            row = db.URLText(url_id=1, timestamp=0, text="Insert a New Row")
            session.add(row)

        else:
            row.text = "2nd time: Editing an Existing Row"

        session.commit()
        print("success")
    except SQLAlchemyError as e:
        print(e)
        print("failure")
        
        
        
        
        
        
    cm = CrawlerManager.CrawlerManager()
    crawler = Crawler.Crawler()
    tp = TextProcessor.TextProcessor()

    origin_url = "http://www.google.com/"

    # TODO: handle origin_url is NULL/invalid --> it should not break the program
    code, url_content = crawler.crawl(origin_url)

    links, text = cm.process_text(origin_url, url_content)
    print(links)
    print(len(links))
"""

if __name__ == "__main__":

	with db.session_scope() as session:
		task_row = db.URLTask(
			url_id=18,
			url='www.github.com',
			timestamp=0,
			duration=1,
			status=2,
			priority=1
		)
		session.add(task_row)
		session.commit()



	"""
	cm = CrawlerManager.CrawlerManager()
	crawler = Crawler.Crawler()
	tp = TextProcessor.TextProcessor()
	origin_url = "http://www.google.com/"

	invalid_url = "www"
	code, url_content = crawler.crawl(origin_url)

	cm.start_crawl(crawler)
	"""


