ID_NONE = -1

#----------------------------------------------------------------------------------------------
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
		
		self.controller = ''
		if 'controller' in spec:
			self.controller = spec['controller']
		
	def get(self):
		record = {
			'_id':self._id,
			'parent_id':self.parent_id,
			'name':self.name,
			'local':self.local,
			'foreign_id':self.foreign_id,
			'controller':self.controller,
			}
		return record
