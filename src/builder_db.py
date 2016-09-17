import os, sys, shutil, argparse
import group_tree_generator
import connection_db
import group_db_writer

class BuilderDB:
	def __init__(self, filename_groups_cache, filename_items_cache):
		self.filename_groups_cache = filename_groups_cache
		self.filename_items_cache = filename_items_cache
		db = None
		
	def build(self):
		self.connect()
		
		groups = group_tree_generator.GroupTreeGenerator(self.filename_groups_cache)
		groups.generate()

		groups_db = group_db_writer.GroupsDBWriter(groups.root)
		groups_db.write()
	
		return None
		
	def connect(self):
		db = connection_db.ConnectionDB('mongodb://localhost:27017/')
		return None