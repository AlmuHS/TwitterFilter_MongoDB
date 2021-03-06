import json
from datetime import datetime, timedelta
import time

import pymongo
from pymongo import MongoClient

from collection_manager import CollectionManager


class MongoManager:
    def __init__(self, domain: str):
        self.connect(domain)
        self.domain = domain

    def connect(self, domain: str):
        self.client = MongoClient(domain, 27017)

    def get_db_list(self):
        db_list = self.client.list_database_names()

        return db_list

    def get_db_manager(self, db_name: str):
        db = self.client[db_name]
        db_manager = DBManager(db)

        return db_manager

    def disconnect(self):
        self.client.close()

    def reconnect(self):
        self.client.close()
        self.connect(self.domain)


class DBManager:
    def __init__(self, db: pymongo.database):
        self.db = db

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

    def load_collection_from_cursor(self, docs, collection_name: str):
        collection = self.db[collection_name]

        for doc in docs:
            collection.insert_one(doc)

        col_manager = CollectionManager(collection)

        return col_manager

    def get_collection_manager(self, collection_name: str):
        collection = self.db[collection_name]
        col_manager = CollectionManager(collection)

        return col_manager

    def get_collections_list(self):
        collection_list = self.db.list_collection_names()

        return collection_list

    def remove_collection(self, collection_name: str):
        response = self.db.drop_collection(collection_name)
        print(response)

    def clone_collection_to_another(self, collection_src: str, collection_dest: str):
        collection = self.db[collection_src]
        docs = collection.find()

        col_manager = self.load_collection_from_cursor(
            docs, collection_dest)

        return col_manager


if __name__ == "__main__":

    collection_name = "twitter_examenes"

    # create_index_in_collection("twitter_examenes", "full_text")
    # results = find_docs_by_keywords("twitter_examenes", ["examen", "parcial"])
    # results = find_docs_by_date("twitter_examenes", '27-01-2021')
    MDB_man = MongoManager('localhost')
    print(MDB_man.get_db_list())

    db_manager = DBManager('twitter_downloads')

    # col_manager = db_manager.get_collection_manager(collection_name)

    col_manager = db_manager.load_collection_from_file(
        "colecciones_raw/examenes.txt", "examenes")

    col_query = col_manager.get_query()
    col_stats = col_manager.get_stats()

    col_manager.remove_all_index()
    col_manager.create_text_index("full_text")

    print(col_manager.check_text_index("full_text"))

    col_query = col_manager.get_query()
    col_stats = col_manager.get_stats()
    col_manager.create_text_index("full_text")

    all_stats = col_stats.show_all_stats()

    print(all_stats)

    # docs = col_query.find_docs_by_keywords("examenes")
    # print(docs.count())

    # db_manager.remove_collection("twitter_arduinos_filtered_nort")
    # db_manager.remove_collection("twitter_arduinos_filtered_keywords")
    # db_manager.remove_collection("twitter_arduinos_filtered_hashtag")

    print(db_manager.get_collections_list())
