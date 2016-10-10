import os, sys, shutil
import codecs, json, io
import common.group_tree_generator
import cache_data
import common.db.instance
import groups_writer_db
import items_writer_db

class BuilderDB:
	'''write cache to database'''
	def __init__(self, specs, cache):
		self.specs = specs
		self.filename_groups_cache = cache.groups_cache_filename
		self.filename_items_cache = cache.items_cache_filename
		self.db = common.db.instance.Instance(self.specs)
		
	def build(self):		
		groups = common.group_tree_generator.GroupTreeGenerator(self.filename_groups_cache)
		groups.generate()

		self.db.connect()
		
		# retrieve user form database
		user = self.db.users.get_user_by_name(self.specs['user']['login'])
		
		if user:
			print("get user /'%s/' OK"%self.specs['user']['login'])
			
			self.db.items.drop()
			self.db.connection.drop()
			
			groups_db = groups_writer_db.GroupsWriterDB(groups.root, self.db)
			groups_db.write()
			
			items = self.loadItems(self.filename_items_cache)
			items_db = items_writer_db.ItemsWriterDB(items, groups.root, self.db, user)
			items_db.write()
		else:
			print('no such user in database')
			
		self.db.disconnect()
		
	def loadItems(self, filename):
		print ('opening items cache file:' + filename)
		items = []
		with io.open(filename, 'r', encoding = 'utf8') as f:
			print 'opening OK'
			for line in f:
				items.append(json.loads(line))
		return items