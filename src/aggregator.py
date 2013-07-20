#!/usr/bin/env python
# -*-coding:utf-8 -*

import datetime
import settings
from publisher import Publisher

# decorator interval from http://stackoverflow.com/questions/5179467/equivalent-of-setinterval-in-python
import threading

def setInterval(interval, times = -1):
    # This will be the actual decorator,
    # with fixed interval and times parameter
    def outer_wrap(function):
        # This will be the function to be
        # called
        def wrap(*args, **kwargs):
            stop = threading.Event()

            # This is another function to be executed
            # in a different thread to simulate setInterval
            def inner_wrap():
                function(*args, **kwargs)
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap

class TimelineAggregator(Publisher):
	def __init__(self):
		Publisher.__init__(self)
		self.history = {}
		
	def receive(self, tweets):
		self.clean_history()

		to_publish = []
		for tweet in tweets:
			if tweet.id not in self.history:
				self.history[tweet.id] = datetime.datetime.now()
				to_publish.append(tweet)
			elif settings.debug:
				print("IGNORED [%d]" % tweet.id)
		self.publish(to_publish)
	
	def clean_history(self):
		time_limit = datetime.datetime.now() - datetime.timedelta(minutes = 5)
		for tweet_id, tweet_add_time in self.history.items():
			# we use items() and not iteritems() because we change the dict while looping over it, so we need a full copy
			if tweet_add_time < time_limit:
				del self.history[tweet_id]
				if settings.debug:
					print("CLEANED [%d]\n" % tweet_id)

class TwitterTimelineFetcher(Publisher):
	def __init__(self, twitter):
		Publisher.__init__(self)
		self.twitter = twitter
		self.last_ids = {'home': -1, 'mentions': -1}
		self.timelines_fetchers = {'home': self.twitter.home_timeline, 'mentions': self.twitter.mentions_timeline}
		
	def get_last_tweets(self, channel):
		last_id = self.last_ids[channel]
		tweets = []
		for tweet in self.get_timeline(channel):
			if tweet.id > last_id:
				tweets.append(tweet)
			if tweet.id > self.last_ids[channel]:
				self.last_ids[channel] = tweet.id
		return tweets		
	
	def get_timeline(self, channel):
		return self.timelines_fetchers[channel]()
	
	@setInterval(settings.polling_interval)
	def start(self):
		if settings.debug:
			print("POLLING")
		self.publish(self.get_last_tweets('home'))
		self.publish(self.get_last_tweets('mentions'))
		
	
		
