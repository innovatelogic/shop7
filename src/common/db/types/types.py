
class Category():
	def __init__(self, spec):
		self._id = spec['_id']
		self.parent_id = spec['parent_id']
		self.name = spec['name']
		
	def get(self):
		record = {
			'_id':self._id,
			'parent_id':self.parent_id,
			'name':self.name,
			}
		return record

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

class UserGroup():
	def __init__(self, spec):
		self._id = spec['_id']
		self.aspect_id = spec['aspect_id']
		self.records = {}
		for i in range(0, len(spec['records'])):
			self.records[spec['records'][i]._id] = spec['records'][i].rights
		
	def get(self):
		record = {
			'_id':self._id,
			'aspect_id':self.aspect_id,
			'records':self.records,
			}
		return record
		
class Item():
	CHARACTERISTICS_MAX = 16
	CHARACTERISTIC_FIELD_NAME = 'characteristicName'
	def __init__(self, spec):
		self._id = spec['_id']
		self.user_id = spec['user_id']
		self.user_group_id = spec['user_group_id']
		self.category_id = spec['category_id']
		self.name = spec['name']
		self.desc = spec['desc']
		self.amount = spec['amount']
		self.price = spec['price']
		self.currency = spec['currency']
		self.availability = spec['availability']
		self.unit = spec['unit']
		self.add_time = spec['add_time']
		
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
			'category_id':self.category_id,
			'name':self.name,
			'desc':self.desc,
			'amount':self.amount,
			'price':self.price,
			'currency':self.currency,
			'availability':self.availability,
			'unit':self.unit,
			'add_time':self.add_time,
				}
		for i in range(0, len(self.characteristics)):
			field_name_numered = self.CHARACTERISTIC_FIELD_NAME + str(i)
			record[field_name_numered] = self.characteristics[i]
			
		return record

class UserAspect():
	class Node():
		def __init__(self, category):
			self.category = category
			self.childs = []
        
	def __init__(self, spec):
		self._id = spec['_id']
		self.group_id = spec['group_id']
		self.node_root = spec['node_root']
		self.hashmap = spec['hashmap']
		
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