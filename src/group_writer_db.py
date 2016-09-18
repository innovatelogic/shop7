import os, sys
from connection_db import ConnectionDB, LayoutDB
from group_tree import flatten_tree


class GroupsWriterDB:
	def __init__(self, root, connection):
		self.root = root
		self.connection = connection
	
	def write(self):

		item_groups_db = self.connection.getCollection(self.connection.db, LayoutDB.ITEM_GROUP_NAME)
		
		flat = flatten_tree(self.root)
		
		for item in flat:
			group_record = {'name':item.name, 'number':item.number}

			if item.parent_number:
				group_record['parent_number'] = item.parent_number
		
			item_groups_db.insert(group_record)
