import os, sys, shutil, argparse
import group_tree_generator
import connection_db
import group_writer_db

CONNECTION_URL = 'mongodb://localhost:27017/'

class BuilderDB:
	def __init__(self, filename_groups_cache, filename_items_cache):
		self.filename_groups_cache = filename_groups_cache
		self.filename_items_cache = filename_items_cache
		self.connection = None
		self.db = None
		
	def build(self):
				
		groups = group_tree_generator.GroupTreeGenerator(self.filename_groups_cache)
		groups.generate()

		self.connect()
		
		groups_db = group_writer_db.GroupsWriterDB(groups.root, self.connection)
		groups_db.write()
	
		self.close()
		
	def connect(self):
		self.connection = connection_db.ConnectionDB(CONNECTION_URL)
		self.connection.connect()
	
	def close(self):
		self.connection.close()