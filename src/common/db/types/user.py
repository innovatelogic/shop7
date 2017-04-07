#----------------------------------------------------------------------------------------------
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