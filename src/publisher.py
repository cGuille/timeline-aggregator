#!/usr/bin/env python
# -*-coding:utf-8 -*

class Publisher:
    """Keep a list of subscribers.
    Use 'subscribe' method to add a subscriber
    Use 'unsubscribe' method to remove a subscriber
    Use 'publish' method to broadcast a message to a specified or every subscribers."""

    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        """subscriber: an object that implements a receive(data) method."""
        if subscriber in self.subscribers:
            raise ValueError("Duplicated subscriber `%s`" % (subscriber))
        elif not hasattr(subscriber, 'receive') or not callable(getattr(subscriber, 'receive')):
        	raise TypeError("The subscriber `%s` does not implement the receive(data) method." % (subscriber))
        	
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
		"""subscriber: the one to remove (raise a ValueError if the given subscriber cannot be found)."""
		self.subscribers.remove(subscriber)

    def publish(self, data):
        """data: the data to broadcast (given to 'receive')."""
        for subscriber in self.subscribers:
            subscriber.receive(data)

