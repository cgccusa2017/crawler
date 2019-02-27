# Crawler


#### To initialize tables in the database: 
(After successfully initializing all tables, the program should print current tables in the database.) 

```python CrawlerModel.py```


#### To initiate the crawl application:

```python CrawlerManager.py```


#### Example:
```"taxfoundation.py"``` in the **unittest** folder provides a simple example of using this Crawler Application. 



## TODO: 

1. In **CrawlerManager.py**: 
    - method **start_crawl** and **collect_result** haven't finished yet, need to finish the **async** in **TaskQueue** to be able to run.
    - **update_url_text_table** method need modification to store file path into database instead of store the raw text.
2. **TaskQueue.py** haven't finished. This class will be used to arrange crawling task queue.
3. In CrawlerModel.py: 
    - For the URLTask, could add the exponential back-off for updating the duration.
4. **LoginModule.py** haven't finished. This class will be used to handle crawler settings for crawling url that requires login information.
5. In **TextProcessor.py**: 
    - method **check_relevance** haven't finished. 
    This method will be used to evaluate the relevance of a new url link before start process the text and store it into database.
    - method **calculate_priority** haven't finished. 
    This method will be used to calculate the priority of the url based on the url content. 
    And it will be used in updating url task table when storing new task to database. 

    






