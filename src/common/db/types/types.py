ID_NONE = -1

#----------------------------------------------------------------------------------------------
class Category():
	def __init__(self, spec):
		self._id = spec['_id']
		self.parent_id = spec['parent_id']
		self.name = spec['name']
		
		self.local = ''
		if 'local' in spec:
			self.local = spec['local']
			
		self.foreign_id = ID_NONE # foreign resource id
		if 'foreign_id' in spec:
			self.foreign_id = spec['foreign_id']
		
		self.controller_name = ''
		if 'controller_name' in spec:
			self.controller_name = spec['controller_name']
		
	def get(self):
		record = {
			'_id':self._id,
			'parent_id':self.parent_id,
			'name':self.name,
			'local':self.local,
			'foreign_id':self.foreign_id,
			'controller_name':self.controller_name,
			}
		return record

#----------------------------------------------------------------------------------------------
class User():
	def __init__(self, spec):
		self._id = spec['_id']
		self.group_id = spec['group_id']
		self.name = spec['name']
		self.email = spec['email']
		self.pwhs = spec['pwhsh']
		self.phone = spec['phone']
	def get(self):
		record = {
			'_id':self._id,
			'group_id':self.group_id,
			'name':self.name,
			'email':self.email,
			'pwhsh':self.pwhs,
			'phone':self.phone,
			}
		return record

#----------------------------------------------------------------------------------------------
class UserRecord():
	'''user id to rights correspondences. uses in construction spec for UserGroup'''
	def __init__(self, _id, rights):
		self._id = _id
		self.rights = rights
	
	def get(self):
		record = {
			'_id':self._id,
			'rights':self.rights,
			}
		return record

#----------------------------------------------------------------------------------------------
class UserGroup():
	def __init__(self, spec):
		self._id = spec['_id']
		self.aspect_id = spec['aspect_id']
		self.user_mapping_id = None
		if 'user_mapping_id' in spec:
			self.user_mapping_id = spec['user_mapping_id']

		self.records = {} #{ user_id : rights }
		for i in range(0, len(spec['records'])):
			self.records[spec['records'][i]._id] = spec['records'][i].rights

	def get(self):
		record = {
			'_id':self._id,
			'aspect_id':self.aspect_id,
			'user_mapping_id':self.user_mapping_id,
			'records':self.records, #{ user_id : rights }
			}
		return record
	
	def addUserRecord(self, user_id, rights):
		if str(user_id) not in self.records:
			self.records[str(user_id)] = rights
		else:
			self.records[str(user_id)] = rights
			print('user already exist in group')
	
	def removeUserRecord(self, user_id):
		out = self.records.pop(str(user_id), None)
		return out != None
	
	def usersNum(self):
		return len(self.records)
	
#----------------------------------------------------------------------------------------------		
class Item():
	CHARACTERISTICS_MAX = 16
	CHARACTERISTIC_FIELD_NAME = 'characteristicName'
	def __init__(self, spec):
		self._id = spec['_id']
		self.user_id = spec['user_id']
		self.user_group_id = spec['user_group_id']
		self.name = spec['name']
		self.desc = spec['desc']
		self.amount = spec['amount']
		self.price = spec['price']
		self.currency = spec['currency']
		self.availability = spec['availability']
		self.unit = spec['unit']
		self.creation_time = spec['creation_time']
		self.update_time = spec['update_time']
		self.mapping_id = spec['mapping_id']

		self.characteristics = []
		
		for i in range(0, self.CHARACTERISTICS_MAX):
			field_name_numered = self.CHARACTERISTIC_FIELD_NAME + str(i)
			if field_name_numered in spec:
			 	self.characteristics.append(spec[field_name_numered])
			 	
	def get(self):
		record = {
			'_id':self._id,
			'user_id':self.user_id,
			'user_group_id':self.user_group_id,
			'name':self.name,
			'desc':self.desc,
			'amount':self.amount,
			'price':self.price,
			'currency':self.currency,
			'availability':self.availability,
			'unit':self.unit,
			'creation_time':self.creation_time,
        	'update_time':self.update_time,
         	'mapping_id':self.mapping_id,
			}
		
		for i in range(0, len(self.characteristics)):
			field_name_numered = self.CHARACTERISTIC_FIELD_NAME + str(i)
			record[field_name_numered] = self.characteristics[i]
			
		return record

#----------------------------------------------------------------------------------------------
class ItemMapping:
	def __init__(self, spec):
		self._id = spec['_id']
		self.item_id = spec['item_id']
		self.mapping = spec['mapping']
		
		#for key, value in spec['mapping'].iteritems():
		#	self.mapping[key] = value
		pass
	
	def get(self):
		record = {
			'_id':self._id,
			'item_id':self.item_id,
			'mapping':self.mapping,
			}
		return record

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
		parent_node = self.getCategoryNodeById(parent_node.category._id)
		if parent_node and category and category.name != 'All':
			bFind = False
			for child in parent_node.childs:
				if child.category.name == category.name:
					bFind = True
					break
			if not bFind:
				parent_node.childs.append(UserAspect.Node(category, parent_node))
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
		
#----------------------------------------------------------------------------------------------
class UserSettings():
    def __init__(self, spec):
		self._id = spec['_id']
		self.user_id = spec['user_id']
		self.update(spec)
        
    def update(self, spec):
		self.options = {
			'client':{
				'ui':{
					'cases':{
						'active_base_aspect':'basic',
						'show_base_aspect_whole_tree':False,
						'list_image_size':2,
						'item_columns':{
							'image': True,
							'name': True,
							'availability': True,
							'amount': True,
							'unit' : True,
							'price' : True,
							'currency' : True,
							'desc' : True,
							},
						},
					'clients':{},
					'connect':{},
					'settings':{},
					'statistics':{},
					'dashboard':{},
					'curr_lang':{'EN':1, 'UA':0, 'RU':0},
					}
				}
		}
		
		if 'options' in spec and 'client' in spec['options'] and 'ui' in spec['options']['client'] and 'cases' in spec['options']['client']['ui']:
			
			if 'item_columns' in spec['options']['client']['ui']['cases']:
				spec_columns = spec['options']['client']['ui']['cases']['item_columns']
				
				if 'image' in spec_columns:
					self.options['client']['ui']['cases']['item_columns']['image'] = spec_columns['image']
				if 'name' in spec_columns:
					self.options['client']['ui']['cases']['item_columns']['name'] = spec_columns['name']
				if 'availability' in spec_columns:
					self.options['client']['ui']['cases']['item_columns']['availability'] = spec_columns['availability']
				if 'amount' in spec_columns:
					self.options['client']['ui']['cases']['item_columns']['amount'] = spec_columns['amount']	
				if 'unit' in spec_columns:
					self.options['client']['ui']['cases']['item_columns']['unit'] = spec_columns['unit']
				if 'price' in spec_columns:
					self.options['client']['ui']['cases']['item_columns']['price'] = spec_columns['price']
				if 'currency' in spec_columns:
					self.options['client']['ui']['cases']['item_columns']['currency'] = spec_columns['currency']
				if 'desc' in spec_columns:
					self.options['client']['ui']['cases']['item_columns']['desc'] = spec_columns['desc']
      	
		      	if 'active_base_aspect' in spec['options']['client']['ui']['cases']:
		      		self.options['client']['ui']['cases']['active_base_aspect'] = spec['options']['client']['ui']['cases']['active_base_aspect']
		      	if 'show_base_aspect_whole_tree' in spec['options']['client']['ui']['cases']:
		      		self.options['client']['ui']['cases']['show_base_aspect_whole_tree'] = spec['options']['client']['ui']['cases']['show_base_aspect_whole_tree']

    def get(self):
    	record = {
			'_id':self._id,
			'user_id':self.user_id,
			'options':self.options,
			}
        return record

#----------------------------------------------------------------------------------------------
class UserMapping():
	''' link user category with base category
		data format { str(user_category_id) : {'base_aspect_name' : category_id, ...} }
	 '''
	def __init__(self, spec):
		self._id = spec['_id']
		self.group_id = spec['group_id']
		self.mapping = spec['mapping']
		pass
	
	def add(self, user_category_id, base_aspect_name, base_category_id):
		
		if str(user_category_id) not in self.mapping:
			self.mapping[str(user_category_id)] = {}
			
		self.mapping[str(user_category_id)][base_aspect_name] = base_category_id
		
		
	def remove(self, user_category_id, base_aspect_name):
		res = False
		if str(user_category_id) in self.mapping:
			if base_aspect_name in self.mapping[str(user_category_id)]:
				del self.mapping[str(user_category_id)][base_aspect_name]
				res = True
		return res
	
	def clear(self):
		self.mapping.clear()
		
	def get(self):
		record = {
			'_id':self._id,
			'group_id':self.group_id,
			'mapping':self.mapping,
			}
		return record