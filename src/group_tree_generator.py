import os, sys
import codecs, json, io
import codecs
from pprint import pprint
from group_tree import Node

class GropTreeGenerator:
	def __init__(self, filename):
			self.filename = filename
			self.root = None
			
	def generate(self):
		print("opening cache groups file:" + self.filename)
		with io.open(self.filename, 'r', encoding='utf8') as f:
			print("opening OK")
			arr_groups = []
			for line in f:
				data = json.loads(line)
				arr_groups.append(data)
			#ustr_to_load = unicode(json_data.read(), 'utf8')
			
			#pprint(arr_groups)
			self.build_tree(arr_groups)
			
		self.dump_tree()
			
	def build_tree(self, arr_plain):
		self.root = Node(arr_plain[0]) #zero element is a root
		del arr_plain[0]
		
		#add first level descents
		descents = []
		for item in arr_plain:
			if not item.get('GroupParentNumber'):
				descents.append(item)
		for node in descents:
			self.root.childs.append(Node(node))
			arr_plain.remove(node)
		
		while arr_plain:
			to_remove = []
			for item in arr_plain:
				parent_number = item['GroupParentNumber']
				parent = self.find_node_by_number(parent_number, self.root)
				if parent:
					parent.childs.append(Node(item))
					to_remove.append(item)
					
			#add exception if to_remove empty
			for node in to_remove:
				arr_plain.remove(node)
				
			
	def find_node_by_number(self, number, node):
		if node:
			if node.number == number:
				return node
			for child in node.childs:
				out = self.find_node_by_number(number, child)
				if out:
					return out
		return None
	
	def dump_tree(self):
		print("opening damp groups file:" + self.filename + '.dump')
		with io.open(self.filename + '.dump', 'w', encoding='utf8') as f:
			print("opening OK")
			f.write(unicode('{\n'))
			self.root.dump(f, 0)
			f.write(unicode('}\n'))
		
		print("opening flat dump groups file:" + self.filename + '.flat')
		with io.open(self.filename + '.flat', 'w', encoding='utf8') as f:
			print("opening OK")
			flat = self.flatten_tree()
			for item in flat:
				f.write(unicode(str(item.number) + ' ' + str(item.name) + '\n', 'utf8'))
				
	def flatten_tree(self):
		flat_array = []
		if self.root:
			top = self.root
			index = 0
			flat_array.append(top)
			while top:
				for child in top.childs:
					flat_array.append(child)
				index += 1
				top = flat_array[index] if len(flat_array) > index else None
				
		return flat_array
		