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