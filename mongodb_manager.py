import json
from datetime import datetime, timedelta
import time

import pymongo
from pymongo import MongoClient

from collection_manager import *


class DBManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.db = self.connect('localhost', db_name)

    def connect(self, domain: str, db_name: str):
        self.client = MongoClient(domain, 27017)
        db = self.client[db_name]

        return db

    def disconnect(self):
        self.client.close()

    def reconnect(self):
        self.client.close()
        self.db = self.connect('localhost', self.db_name)

        return self

    def load_collection_from_file(self, filename: str, collection_name: str):
        collection = self.db[collection_name]

        with open(filename) as tw_collection:
            tweets_list = json.load(tw_collection)

            for tweet in tweets_list:
                created_at = tweet["created_at"]
                dt = datetime.strptime(
                    created_at, '%a %b %d %H:%M:%S +0000 %Y')
                tweet["created_at"] = dt

                collection.insert_one(tweet)

        col_manager = CollectionManager(collection)

        return col_manager

    def load_collection_from_bson(self, docs, collection_name: str):
        collection = self.db[collection_name]

        for doc in docs:
            collection.insert_one(doc)

        col_manager = CollectionManager(collection)

        return col_manager

    def get_collection_manager(self, collection_name: str):
        collection = self.db[collection_name]
        col_manager = CollectionManager(collection)

        return col_manager

    def show_collections_list(self):
        collection_list = self.db.list_collection_names()

        return collection_list

    def remove_collection(self, collection_name: str):
        #response = self.db.drop_collection(collection_name)
        collection = self.db[collection_name]
        response = collection.drop()
        print(response)


if __name__ == "__main__":

    collection_name = "twitter_examenes"

    # create_index_in_collection("twitter_examenes", "full_text")
    # results = find_docs_by_keywords("twitter_examenes", ["examen", "parcial"])
    # results = find_docs_by_date("twitter_examenes", '27-01-2021')
    db_manager = DBManager('twitter_downloads')

    col_manager = db_manager.get_collection_manager(collection_name)

    print(col_manager.get_lenght())

    col_query = col_manager.get_query()
    col_stats = col_manager.get_stats()

    col_manager.remove_all_index()
    col_manager.create_text_index("full_text")

    print(col_manager.check_text_index("full_text"))

    min_date, max_date = col_stats.get_download_period()

    print(min_date)
    print(max_date)

    most_rt_text = col_stats.get_most_retweeted_text()
    print(most_rt_text)

    most_publish_users = col_stats.get_most_published_users()
    print(most_publish_users)

    most_refered_urls = col_stats.get_most_appears_urls()
    print(most_refered_urls)

    most_refered_hashtags = col_stats.get_most_appears_hashtags()
    print(most_refered_hashtags)

    most_refered_users = col_stats.get_most_mentioned_users()
    print(most_refered_users)

    hottest_minute = col_stats.get_hottest_minute()
    print(hottest_minute)

    print(db_manager.show_collections_list())

    # docs = col_query.find_docs_by_keywords_and_date_range(
    #     ["Oficial", "Comunicado"], "27-01-2021", "28-01-2021")

    # for doc in docs:
    #     print(doc['full_text'])

    docs = col_query.find_docs_no_retweet()
    print(docs.count())

    col_manager = db_manager.load_collection_from_bson(
        docs, "twitter_examenes_filtrado")

    time.sleep(1)

    print(col_manager.get_lenght())

    col_query = col_manager.get_query()
    col_manager.create_text_index("full_text")

    docs = col_query.find_docs_by_keywords("examenes")
    print(docs.count())

    col_manager = db_manager.load_collection_from_bson(
        docs, "twitter_examenes_filtrado2")

    print(docs.count())

    col_query = col_manager.get_query()

    db_manager.remove_collection("twitter_examenes_filtrado2")
    db_manager.remove_collection("twitter_examenes_filtrado")

    time.sleep(1)

    db_manager.remove_collection("twitter_arduinos_filtered_nort")
    db_manager.remove_collection("twitter_arduinos_filtered_keywords")
    db_manager.remove_collection("twitter_arduinos_filtered_hashtag")

    print(db_manager.show_collections_list())
