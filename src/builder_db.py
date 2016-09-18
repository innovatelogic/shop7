import os, sys, shutil, argparse
import group_tree_generator
import cache_data
import connection_db
import group_writer_db

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
		
		groups_db = group_writer_db.GroupsWriterDB(groups.root, self.connection)
		groups_db.write()
	
		self.close()
		
	def connect(self):
		self.connection = connection_db.ConnectionDB(CONNECTION_URL)
		self.connection.connect()
	
	def close(self):
		self.connection.close()