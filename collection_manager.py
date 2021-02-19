import pymongo
import json
from datetime import datetime, timedelta

from collection_query import CollectionQuery, CollectionStatistics
import mongodb_manager as MDBMan


class CollectionManager:
    def __init__(self, collection: pymongo.collection):
        self.collection = collection

    def create_text_index(self, field: str):
        self.collection.create_index([(field, "text")])

    def check_text_index(self, field: str):
        index_info = self.collection.index_information()

        return (f'{field}_text' in index_info.keys())

    def remove_all_index(self):
        self.collection.drop_indexes()

    def get_query(self):
        col_query = col_query = CollectionQuery(self.collection)

        return col_query

    def get_stats(self):
        col_stats = CollectionStatistics(self.collection)

        return col_stats

    def get_lenght(self):
        return self.collection.count()
