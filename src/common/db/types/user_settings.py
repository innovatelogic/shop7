
#----------------------------------------------------------------------------------------------
class UserSettings():
    def __init__(self, spec):
		self._id = spec['_id']
		self.user_id = spec['user_id']
		self.update(spec)

#----------------------------------------------------------------------------------------------
    def update(self, spec):
		self.options = {
			'client':{
				'ui':{
					'cases':{
						'active_base_aspect':'basic',
						'show_base_aspect_whole_tree':False,
						'list_image_size':2,
						'item_columns':{
								'image': True,
								'name': True,
								'availability': True,
								'amount': True,
								'unit' : True,
								'price' : True,
								'currency' : True,
								'desc' : True,
								},
						'item_preview_column':True,
						},
					'clients':{},
					'connect':{},
					'settings':{},
					'statistics':{},
					'dashboard':{},
					}
				},
			'curr_lang': 0 }
		
		src_ui_cases_dict = {}
		dst_ui_cases_dict = self.options['client']['ui']['cases']
		
		if 'options' in spec and \
			'client' in spec['options'] and \
			'ui' in spec['options']['client'] and \
			'cases' in spec['options']['client']['ui']: 
				src_ui_cases_dict = spec['options']['client']['ui']['cases']
				
  		if 'active_base_aspect' in src_ui_cases_dict:
  			dst_ui_cases_dict['active_base_aspect'] = src_ui_cases_dict['active_base_aspect']
	      		
  		if 'show_base_aspect_whole_tree' in src_ui_cases_dict:
	  		dst_ui_cases_dict['show_base_aspect_whole_tree'] = src_ui_cases_dict['show_base_aspect_whole_tree']
  		if 'item_preview_column' in src_ui_cases_dict:
  			dst_ui_cases_dict['item_preview_column'] = src_ui_cases_dict['item_preview_column']
	      	
		if 'item_columns' in src_ui_cases_dict:
			src_spec_columns = src_ui_cases_dict['item_columns']
			dst_spec_columns = dst_ui_cases_dict['item_columns']
			
			if 'image' in src_spec_columns:
				dst_spec_columns['image'] = src_spec_columns['image']
			if 'name' in src_spec_columns:
				dst_spec_columns['name'] = src_spec_columns['name']
			if 'availability' in src_spec_columns:
				dst_spec_columns['availability'] = src_spec_columns['availability']
			if 'amount' in src_spec_columns:
				dst_spec_columns['amount'] = src_spec_columns['amount']	
			if 'unit' in src_spec_columns:
				dst_spec_columns['unit'] = src_spec_columns['unit']
			if 'price' in src_spec_columns:
				dst_spec_columns['price'] = src_spec_columns['price']
			if 'currency' in src_spec_columns:
				dst_spec_columns['currency'] = src_spec_columns['currency']
			if 'desc' in src_spec_columns:
				dst_spec_columns['desc'] = src_spec_columns['desc']
      	
	      	
    def get(self):
    	record = {
			'_id':self._id,
			'user_id':self.user_id,
			'options':self.options,
			}
        return record