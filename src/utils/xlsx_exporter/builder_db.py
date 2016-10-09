import os, sys, shutil
import codecs, json, io
import common.group_tree_generator
import cache_data
import common.db.connection
import groups_writer_db
import items_writer_db

class BuilderDB:
	def __init__(self, specs, cache):
		self.specs = specs
		self.filename_groups_cache = cache.groups_cache_filename
		self.filename_items_cache = cache.items_cache_filename
		self.connection = None
		self.db = None
		
	def build(self):
				
		groups = common.group_tree_generator.GroupTreeGenerator(self.filename_groups_cache)
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
		self.connection = common.db.connection.ConnectionDB(self.specs)
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