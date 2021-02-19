import tweepy as tw
import json

from twitter_keys import *


class TwitterLogin:

    def _auth(self, consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str):
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return auth

    def login(self, consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str):
        auth = self._auth(consumer_key, consumer_secret,
                          access_token, access_token_secret)

        self.api = tw.API(auth, wait_on_rate_limit=True,
                          wait_on_rate_limit_notify=True)

        return self.api


class TwitterQuery:
    def __init__(self, api: tw.API):
        self.api = api

    def get_user_timeline(self, username: str):
        user = self.api.get_user(username)

        return user.timeline

    def search_tweets_by_wordlist(self, wordlist: str, limit: int):
        tweets = tw.Cursor(self.api.search,
                           q=wordlist,
                           tweet_mode='extended').items(limit)

        return tweets

    def search_tweets_by_wordlist_and_date_range(self, wordlist: str, date_start: str, date_end: str, limit: int):
        try:
            tweets = tw.Cursor(self.api.search,
                               q=wordlist,
                               tweet_mode='extended',
                               since=date_start,
                               until=date_end).items(limit)

        except Exception as e:
            print(e)

        return tweets

    def search_tweets_by_wordlist_and_date_start(self, wordlist: str, date_start: str, limit: int):
        tweets = tw.Cursor(self.api.search,
                           q=wordlist,
                           tweet_mode='extended',
                           since=date_start).items(limit)

        return tweets

    def search_tweets_by_wordlist_and_date_end(self, wordlist: str, date_end: str, limit: int):
        tweets = tw.Cursor(self.api.search,
                           q=wordlist,
                           tweet_mode='extended',
                           until=date_end).items(limit)

        return tweets

    def export_tweets_json(self, tweets: tw.Cursor):
        tw_json_list = []

        for tweet in tweets:
            tw_str = json.dumps(tweet._json, ensure_ascii=False)
            tw_json = json.loads(tw_str)
            tw_json_list.append(tw_json)

        return tw_json_list

    def export_tweets_to_file(self, tweets: tw.Cursor, filename: str):
        with open(filename, "a") as file:
            json.dump([tweet._json for tweet in tweets],
                      file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    tw_login = TwitterLogin()
    api = tw_login.login(consumer_key, consumer_secret,
                         access_token, access_token_secret)

    tw_api = TwitterQuery(api)

    #timeline = tw_api.get_user_timeline("unihuelva")
    # print(timeline)

    date_start = "2021-02-05"
    date_end = "2021-02-10"

    # tweetset = tw_api.search_tweets_by_wordlist_and_date_range(
    #    "exámenes febrero", "2021-01-20", "2021-01-21", 100)
    # # print(tweets)

    tweetset = tw_api.search_tweets_by_wordlist_and_date_start(
        "Eres old pero así de old", date_start, 10000)

    # for tweet in tweetset:
    #    print(tweet)

    tw_api.export_tweets_to_file(tweetset, "eres_old.txt")
