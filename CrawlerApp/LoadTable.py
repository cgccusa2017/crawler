# from sqlalchemy import create_engine
# from sqlalchemy import MetaData
import CrawlerModel as db
import __init__ as init
# from sqlalchemy.orm import sessionmaker





with db.session_scope() as session:

    row = session.query(db.URLText).filter(db.URLText.url_id == 2).first()
    print(row)
    if row is None:
        row = db.URLText(
            url_id=2,
            timestamp=0,
            text="new row"
        )
        session.add(row)
    else:

        print(row.text)
        row.text = "updating row"
    session.commit()

    row = session.query(db.URLText).filter(db.URLText.url_id == 2).first()
    print(row.text)





'''
with db.session_scope() as session:
    row1 = db.URLTask(
        url="www.github.com",
        timestamp=0,
        duration=1,
        status=2,
        priority=0
    )

    session.add(row1)
    session.commit()

with db.session_scope() as session:
    curr_id = session.query(db.URLTask.url_id).filter(db.URLTask.url == "www.github.com").first()[0]
    print(curr_id)

    if curr_id is not None:

        # print(curr_id)
        row2 = db.URLText(
            url_id=curr_id,
            timestamp=0,
            text="keep updating new text"
        )
        session.add(row2)
    else:
        print("None")

    # print('Add - Retrieve - Add: ',row2.url_id), row2.text)

'''


'''
print("Tables in database:")
for _t in db.Base.metadata.tables:
    print(_t)

# with db.session_scope() as session:
#     row = session.query(db.URLText).filter(db.URLText.url_id == url_id).first()
#     if row is None:
#         row = db.URLText(
#             url_id=url_id,
#             timestamp=0,
#             text=text
#         )
#     session.add(row)


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
'''