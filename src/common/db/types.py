
class User():
	def __init__(self, spec):
		self.id = spec['_id']
		self.name = spec['name']
		self.group_id = spec['group_id']
		self.email = spec['email']
		self.pwhs = spec['pwhsh']
		self.phone = spec['phone']


class Item():
	CHARACTERISTICS_MAX = 16
	def __init__(self, spec):
		self.id = spec['_id']
		self.user_id = spec['user_id']
		self.user_group_id = spec['user_group_id']
		self.category = spec['category_id']
		self.name = spec['name']
		self.amount = spec['amount']
		self.price = spec['price']
		self.currency = spec['currency']
		
		self.characteristics = []
		FIELD_NAME = 'characteristicName'
		for i in range(0, CHARACTERISTICS_MAX):
			field_name_num = FIELD_NAME + str(i)
			if field_name_num in spec:
			 	self.characteristics.append(spec[field_name_num])
			 	