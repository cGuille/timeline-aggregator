#!/usr/bin/env python
# -*-coding:utf-8 -*

from publisher import Publisher

class PubTest(Publisher):
	pass

class SubTest:
	def receive(self, data):
		print(data)

class Foo:
	pass

class Bar:
	def receive(self, one, two):
		print(one, two)

test = PubTest()

test.publish(1)
test.subscribe(SubTest())
test.publish(2)
test.subscribe(Foo())
test.publish(3)
test.subscribe(Bar())
test.publish(4)

