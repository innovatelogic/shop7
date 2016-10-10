
class User():
	def __init__(self, spec):
		self.id = spec['_id']
		self.name = spec['name']
		self.group_id = spec['group_id']
		self.email = spec['email']
		self.pwhs = spec['pwhsh']
		self.phone = spec['phone']

class UserRecord():
	'''user id to rights correspondences'''
	def __init__(self, id, rights):
		self.id = id
		self.rights = rights

class UserGroup():
	def __init__(self, spec):
		self.id = spec['_id']
		self.records = []
		for i in range(0, len(spec['records'])):
			self.record.append(UserRecord(spec['records'][i]['id'], spec[records][i]['rights']))
		
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
				}
		for i in range(0, len(self.characteristics)):
			field_name_numered = self.CHARACTERISTIC_FIELD_NAME + str(i)
			record[field_name_numered] = self.characteristics[i]
			
		return record