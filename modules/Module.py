from abc import ABCMeta, abstractmethod

class Module(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def __init__(self):
		self.hasText = True
		self.text = "";

	@abstractmethod
	def HasText(self):
		return self.hasText

	@abstractmethod
	def GetText(self):
		return self.text
