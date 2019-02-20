#from abc import abc, ABCMeta, abstractmethod
import abc

class _Module(metaclass=abc.ABCMeta):
	config_full = None
	config = None

	def __init__(self, config_full):
		self.hasText = False
		self.text = "";
		self.config_full = config_full

		classname = self.__class__.__name__
		if classname in config_full:
			self.config = config_full[classname]

		self.Run()


	@abc.abstractmethod
	def Run(self):
		raise NotImplementedError()

	def HasText(self):
		return self.hasText

	def GetText(self):
		return self.text.rstrip()
