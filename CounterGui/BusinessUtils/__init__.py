from typing import (
	List,
	Iterable,
	Dict
)
import requests

class BusinessABC:
	def __init__(self, name):
		self.name = name


class BusinessHandler:
	def __init__(self):
		pass

	def getBusiness(self, **kwargs):
		return self