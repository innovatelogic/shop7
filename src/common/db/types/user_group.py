
#----------------------------------------------------------------------------------------------
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