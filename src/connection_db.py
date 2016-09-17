from pymongo import MongoClient

class ConnectionDB:
	def __init__(self, url):
		self.url = url
		self.connection = None
		
	def connect(self):
		connection = MongoClient(self.url)