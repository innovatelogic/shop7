#----------------------------------------------------------------------------------------------
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