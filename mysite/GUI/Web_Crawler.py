import tweepy
import json
from datetime import datetime

class twitterCrawl:

    def __init__(self, v2=False):
        self.__API_key = "x9lDLlXTdbU3YQkWFKzDA1Y8h"
        self.__API_secret = "B0ny0DNJdMoDQOKPNd09zm9g5CLGr2hYsIRSGFGcnReYwLfLUf"
        self.__AccessToken = "2936953311-lP0BXBmIrHoMl1Qnq63bUgxZVz3BDK1wE2SalWQ"
        self.__AccessSecret = "z9VLuiXenMp9ZUXnYBrCZ0G88V0Peb0yyE99aeNSQn8Q2"
        if v2:
            self.__client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAABIyIAEAAAAAkN4CieMRh1yMokUnmm0nqWcd7L0%3DwwtU4elHzZk5PzXnD1APbgDKyPRbF7ukl5dQAc1fLEhd9EZCed')
        else:
            self._auth = tweepy.OAuthHandler(self.__API_key, self.__API_secret)
            self._auth.set_access_token(self.__AccessToken, self.__AccessSecret)
            self.__api = tweepy.API(self._auth)
        self.results = []
        self.resFile = "search_results.txt"
        self.query = ""

    def search_tweets_v1(self, query, maxTweets=10000, justText = True):
        try:
            cur = tweepy.Cursor(self.__api.search_tweets, q = query).items(maxTweets)
        except():
            print("try using v2")
        for tweet in cur:
            if justText:
                self.results.append(tweet.text)
            else:
                self.results.append(tweet.text)

    def search_tweets_v2(self, query, max=100):
        for tweet in tweepy.Paginator(self.__client.search_recent_tweets, query=query,
                                      tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=max):
            self.results.append(tweet.data)

    def search_time_frame(self, startTime, endTime, query, resultCount=100):
        for tweet in self.__client.search_all_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],
                                          start_time=startTime,
                                          end_time=endTime, max_results=resultCount):
            self.results.append(tweet.data)

    def recent_search(self, query):
        for tweet in self.__client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],
                                             max_results=100):
            self.results.append(tweet.data)

    def appendResults(self):
        with open(self.resFile, "a") as outfile:
            json.dump(self.results, outfile)
        outfile.close()

    def clearResults(self):
        open(self.resFile, "w").close()

    def loadResults(self):
        with open(self.resFile, "r") as infile:
            self.results = json.loads(infile.read())
        infile.close()


#if __name__ == '__main__':
   #m = twitterCrawl(v2=True)
   # m.search_tweets_v2('"Donald Trump"')
    #m.appendResults()