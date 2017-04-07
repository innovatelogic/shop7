#----------------------------------------------------------------------------------------------
class ItemMapping:
	def __init__(self, spec):
		self._id = spec['_id']
		self.item_id = spec['item_id']
		self.mapping = spec['mapping']
		self.user_group_id = spec['user_group_id']
		pass
	
	def get(self):
		record = {
			'_id':self._id,
			'item_id':self.item_id,
			'user_group_id':self.user_group_id,
			'mapping':self.mapping,
			}
		return record