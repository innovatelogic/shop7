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