import os, sys, shutil
import codecs, json, io
import group_tree_generator
import cache_data
import connection_db
import groups_writer_db
import items_writer_db

CONNECTION_URL = 'mongodb://localhost:27017/'

class BuilderDB:
	def __init__(self, cache):
		self.filename_groups_cache = cache.groups_cache_filename
		self.filename_items_cache = cache.items_cache_filename
		self.connection = None
		self.db = None
		
	def build(self):
				
		groups = group_tree_generator.GroupTreeGenerator(self.filename_groups_cache)
		groups.generate()

		self.connect()
		
		self.connection.drop()
		
		groups_db = groups_writer_db.GroupsWriterDB(groups.root, self.connection)
		groups_db.write()
		
		items = self.loadItems(self.filename_items_cache)
		items_db = items_writer_db.ItemsWriterDB(items, groups.root, self.connection)
		items_db.write()
		
		self.close()
		
	def connect(self):
		self.connection = connection_db.ConnectionDB(CONNECTION_URL)
		self.connection.connect()
	
	def close(self):
		self.connection.close()
		
	def loadItems(self, filename):
		print ('opening items cache file:' + filename)
		items = []
		with io.open(filename, 'r', encoding = 'utf8') as f:
			print 'opening OK'
			for line in f:
				items.append(json.loads(line))
		return items