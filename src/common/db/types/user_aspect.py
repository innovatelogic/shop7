#----------------------------------------------------------------------------------------------
class UserAspect():
	class Node():
		def __init__(self, category, parent):
			''' 
			@param category - Category type
			@param parent - Node type '''
			self.category = category
			self.parent = parent
			self.childs = [] # array of Nodes
			
		def getChildByName(self, name):
			out = None
			for child in self.childs:
				if name == child.category.name:
					out = child
					break
			return out

	def __init__(self, spec):
		self._id = spec['_id']
		self.group_id = spec['group_id']
		self.node_root = spec['node_root'] # runtime only data serialize as category field
		self.hashmap = spec['hashmap'] # runtime only data for fast localize
		
	def get(self):
		record = {
			'_id':self._id,
			'group_id':self.group_id,
			'categories':[]
			}
		
		stack = []
		stack.append(self.node_root)

		while len(stack):      
			new_stack = []
			for item in stack:
				record['categories'].append(item.category.get())
            
				for child in item.childs:
					new_stack.append(child)
					
			stack = new_stack

		return record
	
	def getCategoryNodeById(self, _id):
		''' find category with specified _id in tree
		@param _id category id
		@return: Node if found otherwise None
		'''
		out = None
		if str(_id) in self.hashmap:
			out = self.hashmap[str(_id)]
		return out
		
	def addChildCategory(self, parent_node, category):
		''' adds child category node in Runtime. 
			Do not save to db. use separate storage function for this purpose.
			@warning: Do not add if category with parent_id do not exist.
					  or category with equal name present in same hierarchy level.
					  Do not allow category with name 'All'
			@param parent_id - of parent category node
			@param category_node - newly created node of Node type
			@return True if operation sucess. False otherwise '''
		res = False
		#parent_node = self.getCategoryNodeById(parent_node.category._id)
		if parent_node and category and category.name != 'All':
			bFind = False
			for child in parent_node.childs:
				if child.category.name == category.name:
					bFind = True
					break
			if not bFind:
				node = UserAspect.Node(category, parent_node)
				parent_node.childs.append(node)
				self.hashmap[str(category._id)] = node
				res = True
		return res
		
	def removeCategory(self, cateory_node):
		res = False
		category_node = self.getCategoryNodeById(cateory_node.category._id)
		if category_node:
			if category_node.category.name != 'root' or category_node.category.name != 'All':
				parent_node = self.getCategoryNodeById(cateory_node.parent.category._id)
				if parent_node:
					parent_node.childs.remove(category_node)
					res = True
		return res
		