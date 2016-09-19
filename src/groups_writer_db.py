from connection_db import ConnectionDB, LayoutDB
from group_tree import flatten_tree, dump_tree_flat
from bson.objectid import ObjectId

class GroupsWriterDB:
	def __init__(self, root, connection):
		self.root = root
		self.connection = connection
	
	def write(self):

		item_groups_db = self.connection.getCollection(self.connection.db, LayoutDB.ITEM_GROUP_NAME)
		
		#iterate over the tree and assign id's
		self.assignTreeUIDs(self.root)
		
		dump_tree_flat("flat.txt", self.root)
			
		flat = flatten_tree(self.root)
		
		#
		for item in flat:
			group_record = {'id': item.id, 'parent_id': item.parent_id, 'name':item.name, 'number':item.number}

			if item.parent_number:
				group_record['parent_number'] = item.parent_number
		
			item_groups_db.insert(group_record)
			
	def assignTreeUIDs(self, root):
		root._id = ObjectId()
		root._parent_id = None
		stack = [root]
			
		while stack:
			new_stack = []
			for item in stack:
				for node in item.childs:
					node._id = ObjectId()
					node._parent_id = item._id
					new_stack.append(node)
			stack = new_stack
