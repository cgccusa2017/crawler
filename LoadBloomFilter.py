
from pybloom import ScalableBloomFilter
import CrawlerModel as db
from sqlalchemy.exc import SQLAlchemyError

"""
This file runs when the crawler system starts. 
It will put all existing URLs from URL task table into the bloom filter. 
"""

def Set_up_bloom_filter():

    with db.session_scope() as session:
        try:
            urls = session.query(db.URLTask.url).all()

            sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
            for i in range(len(urls)):
                sbf.add(urls[i][0])
            # print(sbf.capacity)
            # print(sbf.count)
            return sbf
        except SQLAlchemyError as e:
            print(e)





if __name__ == "__main__":
    Set_up_bloom_filter()
