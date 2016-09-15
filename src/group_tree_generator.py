import os, sys
import codecs, json, io
import codecs
from pprint import pprint

class GropTreeGenerator:
	def __init__(self, filename):
			self.filename = filename
			
	def generate(self):
		#json.loads(self.filename, encoding='utf-16')
		with io.open(self.filename, 'r', encoding='utf8') as f:
			arr_groups = []
			for line in f:
				data = json.loads(line)
				arr_groups.append(data)
			#ustr_to_load = unicode(json_data.read(), 'utf8')
			
			pprint(arr_groups)