import pymongo
import json
from datetime import datetime, timedelta


class CollectionManager:
    def __init__(self, collection: pymongo.collection):
        self.collection = collection

    def create_text_index(self, field: str):
        self.collection.create_index([(field, "text")])

    def check_text_index(self, index_name: str):
        index_info = self.collection.index_information()

        return (f'{index_name}_text' in index_info.keys())

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


class CollectionQuery:
    def __init__(self, collection: pymongo.collection):
        self.collection = collection

    def find_docs_by_keywords(self, keywords: str):
        # keywords_str = '.'.join([str(word) for word in keywords])

        docs = self.collection.find(
            {"$text": {"$search": keywords}})

        return docs

    def find_docs_by_exact_phrase(self, phrase: str):
        query = f'\\"{phrase}\\"'
        # query = r'\"Comunicado Oficial\"'

        docs = self.collection.find(
            {"$text": {"$search": query}})

        return docs

    def find_docs_by_date_range(self, date_start: str, date_end: str):
        datestart_obj = datetime.strptime(date_start, '%d-%m-%Y')
        dateend_obj = datetime.strptime(date_end, '%d-%m-%Y')

        docs = self.collection.find(
            {"created_at": {'$gte': datestart_obj, '$lte': dateend_obj}})

        return docs

    def find_docs_by_date(self, date: str):
        datetime_obj = datetime.strptime(date, '%d-%m-%Y')
        next_day_obj = datetime_obj + timedelta(days=1)

        docs = self.collection.find(
            {"created_at": {'$gte': datetime_obj, '$lt': next_day_obj}})

        return docs

    def find_docs_by_keywords_and_date(self, keywords: str, date: str):
        datetime_obj = datetime.strptime(date, '%d-%m-%Y')
        next_day_obj = datetime_obj + timedelta(days=1)

        docs = self.collection.aggregate([
            {'$match': {
                "created_at": {'$gte': datetime_obj, '$lte': next_day_obj},
                "$text": {"$search": keywords}
            }}
        ])

        return docs

    def find_docs_by_keywords_and_date_range(self, keywords: str, date_start: str, date_end: str):
        datestart_obj = datetime.strptime(date_start, '%d-%m-%Y')
        dateend_obj = datetime.strptime(date_end, '%d-%m-%Y')

        docs = self.collection.aggregate([
            {'$match': {
                "created_at": {'$gte': datestart_obj, '$lte': dateend_obj},
                "$text": {"$search": keywords}
            }}
        ])

        return docs

    def find_docs_by_user(self, username: str):
        docs = self.collection.find({"user.screen_name": username})

        return docs

    def find_docs_by_hashtag(self, hashtag: str):
        docs = self.collection.find({"entities.hashtags.text": hashtag})

        return docs

    def find_docs_no_retweet(self):
        docs = self.collection.find({"retweeted_status": {'$exists': 0}})

        return docs


class CollectionStatistics:
    def __init__(self, collection: pymongo.collection):
        self.collection = collection

    def get_docs_number(self):
        quantity = self.collection.count()

        return quantity

    def get_download_period(self):
        period = self.collection.aggregate([
            {'$group':
             {
                 '_id': None,
                 'min_date': {'$min': "$created_at"},
                 'max_date': {'$max': "$created_at"}
             }
             },
            {'$project':
             {
                 '_id': 0
             }
             }
        ]).next()

        min_date = period['min_date']
        max_date = period['max_date']

        return min_date, max_date

    def get_most_retweeted_text(self):

        doc = self.collection.find().sort(
            [('retweeted_status.retweet_count', -1)]).limit(1).next()

        text = doc['full_text']

        return text

    def get_most_published_users(self):
        users_data = {}

        users = self.collection.aggregate([
            {'$group':
             {
                 '_id': "$user.screen_name",
                 'num_tweets': {'$sum': 1}
             }
             },
            {'$sort': {"num_tweets": -1}},
            {'$limit': 5}
        ])

        for user in users:
            username = user['_id']
            num_tweets = user['num_tweets']
            users_data[username] = num_tweets

        return users_data

    def get_most_appears_urls(self):
        url_list = {}

        urls = self.collection.aggregate([
            {'$group':
             {
                 '_id': "$entities.urls.url",
                 'num_ocurrences': {'$sum': 1}
             }
             },
            {'$unwind': "$_id"},
            {'$sort': {"num_ocurrences": -1}},
            {'$limit': 5}
        ])

        for url in urls:
            url_u = url['_id']
            num_appears = url['num_ocurrences']
            url_list[url_u] = num_appears

        return url_list

    def get_most_appears_hashtags(self):
        hashtag_list = {}

        hashtags = self.collection.aggregate([
            {'$group':
             {
                 '_id': "$entities.hashtags.text",
                 'num_ocurrences': {'$sum': 1}
             }
             },
            {'$unwind': "$_id"},
            {'$sort': {"num_ocurrences": -1}},
            {'$limit': 5}
        ])

        for hash in hashtags:
            hashtag = hash["_id"]
            num_ocurrences = hash["num_ocurrences"]

            hashtag_list[hashtag] = num_ocurrences

        return hashtag_list

    def get_most_mentioned_users(self):
        user_list = {}

        users = self.collection.aggregate([
            {'$unwind': "$entities.user_mentions"},
            {'$group': {
                '_id': "$entities.user_mentions.screen_name",
                'count': {'$sum': 1}
            }},
            {'$project': {
                '_id': 0,
                'username': "$_id",
                'num_mentions': "$count"
            }},
            {'$sort': {
                "num_mentions": -1
            }},
            {'$limit': 5}
        ])

        for user in users:
            username = user['username']
            num_mentions = user['num_mentions']

            user_list[username] = num_mentions

        return user_list

    def get_hottest_minute(self):
        date = self.collection.aggregate([
            {"$project": {
                "y": {"$year": "$created_at"},
                "M": {"$month": "$created_at"},
                "d": {"$dayOfMonth": "$created_at"},
                "h": {"$hour": "$created_at"},
                "m": {"$minute": "$created_at"}}
             },
            {"$project": {
                "date": {"$dateFromParts": {
                    "year": "$y",
                    "month": "$M",
                    "day": "$d",
                    "hour": "$h",
                    "minute": "$m"
                }}
            }},
            {"$group": {
                "_id": "$date",
                "total_tweets": {"$sum": 1}
            }},
            {"$sort": {"total_tweets": -1}},
            {"$limit": 1},

        ]).next()

        minute = date['_id'].strftime('%d/%m/%Y %H:%M')
        num_tweets = date['total_tweets']

        return minute, num_tweets

    def show_all_stats(self):
        stats_str = ""

        docs_number = self.get_docs_number()
        stats_str += f"Numero de documentos: {docs_number}\n"

        dl_start, dl_end = self.get_download_period()
        stats_str += f"Periodo de descarga: {dl_start} - {dl_end}\n\n"

        most_rt_text = self.get_most_retweeted_text()
        stats_str += f"Tuit mas retuiteado:\n{most_rt_text}\n\n"

        users_most_published = self.get_most_published_users()
        stats_str += "Usuarios con mas tuits publicados: \n"

        for user in users_most_published:
            username = user
            num_pubs = users_most_published[user]

            stats_str += f"Usuario: {username}\tPublicaciones: {num_pubs}\n"

        stats_str += "\nURLs con mas apariciones: \n"

        url_most_appeared = self.get_most_appears_urls()
        for url in url_most_appeared:
            num_pubs = url_most_appeared[url]

            stats_str += f"URL: {url}\tApariciones: {num_pubs}\n"

        stats_str += "\nHashtag mas mencionados\n"

        hashtag_most_appeared = self.get_most_appears_hashtags()

        for hashtag in hashtag_most_appeared:
            num_pubs = hashtag_most_appeared[hashtag]

            stats_str += f"Hashtag: {hashtag}\tApariciones: {num_pubs}\n"

        stats_str += "\nUsuarios mas mencionados\n"

        users_most_cited = self.get_most_mentioned_users()

        for user in users_most_cited:
            num_cites = users_most_cited[user]

            stats_str += f"Usuario: {user}. Menciones: {num_cites}\n"

        stats_str += "\nMinuto mas caliente\n"

        hottest_minute, num_tweets = self.get_hottest_minute()

        stats_str += f"Minuto: {hottest_minute}\tNumero de tuits: {num_tweets}"

        return stats_str
