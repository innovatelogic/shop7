from common.db.connection import LayoutDB
from group_tree import flatten_tree, dump_tree_flat
from bson.objectid import ObjectId

class GroupsWriterDB:
	def __init__(self, root, db):
		self.root = root
		self.db = db
	
	def write(self):

		groups_db = self.db.connection.getCollection(self.db.connection.db, LayoutDB.GROUPS_NAME)
		
		#iterate over the tree and assign id's
		self.assignTreeUIDs(self.root)
		
		#dump_tree_flat("flat.txt", self.root)

		flat = flatten_tree(self.root)
		
		#
		for item in flat:
			group_record = {'_id': item._id, 'parent_id': item._parent_id, 'name':item.name, 'number':item.number}

			#if item.parent_number:
			#	group_record['parent_number'] = item.parent_number
		
			groups_db.insert(group_record)
			
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
