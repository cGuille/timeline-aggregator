#!/usr/bin/env python
# -*-coding:utf-8 -*

import time
import settings
import tweepy
from aggregator import TimelineAggregator, TwitterTimelineFetcher

class Tweet:
	def __init__(self, raw_status):
		self.id = raw_status.id
		self.author = raw_status.author.screen_name
		self.content = raw_status.text

class EllipsisAdvisor:
	def __init__(self, twitter_api):
		self.twitter_api = twitter_api

	def receive(self, tweets):
		tweets = [Tweet(raw) for raw in tweets]
		for tweet in tweets:
			if settings.debug:
				print ("[%d]\n%s:\n%s\n" % (tweet.id, tweet.author, tweet.content))
			if tweet.content.find('...') != -1:
				self.process(tweet)

	def process(self, tweet):
		print("It contains '...'! %s" % tweet.content)
		self.send_reply(tweet, self.create_reply_to(tweet))
	
	def send_reply(self, reply_to_tweet, status_text):
		self.twitter_api.update_status(status_text, reply_to_tweet.id)
		
	def create_reply_to(self, tweet):
		return "@%s: Tu devrais utiliser '…' plutôt que '...'… tu gagnerais deux caractères dans tes tweets !" % tweet.author
		
if __name__ == '__main__':
	auth = tweepy.OAuthHandler(consumer_key=settings.consumer_key, consumer_secret=settings.consumer_secret)
	auth.set_access_token(settings.access_key, settings.access_secret)

	api = tweepy.API(auth_handler=auth, secure=True, retry_count=3)

	fetcher = TwitterTimelineFetcher(api)
	aggregator = TimelineAggregator()
	advisor = EllipsisAdvisor(api)
	
	fetcher.subscribe(aggregator)
	aggregator.subscribe(advisor)
	
	fetcher.start()
	
	while True:
		time.sleep(70)

