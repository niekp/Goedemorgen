from abc import ABCMeta, abstractmethod

class _Module(object):
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
		return self.text.rstrip()
