import os, sys, shutil, time
import codecs, json, io
import common.group_tree_generator
import cache_data
import common.db.instance
import groups_writer_db
import items_writer_db
from common.image_loader import ImageURLLoader
from common.models.realm import Realm

class BuilderDB:
	'''write cache to database'''
	def __init__(self, specs, cache):
		self.specs = specs
		self.filename_groups_cache = cache.groups_cache_filename
		self.filename_items_cache = cache.items_cache_filename
		self.realm = Realm(self.specs)
		
	def build(self):
		
		self.realm.start()
		
		#groups = common.group_tree_generator.GroupTreeGenerator(self.filename_groups_cache)
		#groups.generate()

		# retrieve user form database
		user = self.realm.db.users.get_user_by_name(self.specs['user']['login'])
		
		if user:
			print("get user {} OK".format(self.specs['user']['login']))
			
			#self.realm.db.items.drop()
			#self.realm.db.items_mapping.drop()
			
			#groups_db = groups_writer_db.GroupsWriterDB(groups.root, self.db)
			#groups_db.write()
			
			items = self.loadItems(self.filename_items_cache)
			items_db = items_writer_db.ItemsWriterDB(self.specs, items, self.realm, user)
			items_db.write()

			timestr = time.strftime("%Y%m%d-%H%M%S")
			img_refs_filename = self.specs['path']['out'] + 'img_refs_' + self.specs['user']['login'] + '_' + timestr + '.json'
			items_db.save_ref_mapping(img_refs_filename)
			
			#load resources
			print('start load resources')
			loader = ImageURLLoader(img_refs_filename, self.specs['path']['out'] + self.specs['user']['login'])
			loader.run()
         	
		else:
			print('[BuilderDB::build] no such user in database')
		
		self.realm.stop()
		
	def loadItems(self, filename):
		print ('opening items cache file:' + filename)
		items = []
		with io.open(filename, 'r', encoding = 'utf8') as f:
			print 'opening OK'
			for line in f:
				items.append(json.loads(line))
		return items
	
	
###############
		'''self.db.users.drop()
		self.db.user_groups.drop()
		
		#add test user
		
		user_spec = {
			'name':'admin',
			'email':'admin',
			'pwhsh':'admin',
			'phone':'+8044000000'
			}
		
		self.db.users.add_user(user_spec, None, "rwd")
		
		group = self.db.user_groups.get_user_group(user_spec['group_id'])
		
		user_spec2 = {
			'name':'guest',
			'email':'guest',
			'pwhsh':'guest',
			'phone':'+8044000001'
			}
		
		self.db.users.add_user(user_spec2, group._id, 'rwd')
		
		usr = self.db.users.get_user_by_name('foo')
		self.db.users.remove_user(usr._id)
		
		usr = self.db.users.get_user_by_name('admin')
		self.db.users.remove_user(usr._id)
		'''
#########