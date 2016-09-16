import os, sys
import codecs, json, io
import codecs
from pprint import pprint

class Node:
	def __init__(self, data):
		self.name = data['GroupName']
		self.number = data['GroupNumber']
		self.id = None
		self.parent_id = None
		self.parent_number = None
		
		if data.get('GroupID'):
			self.id = data['GroupID']
		if data.get('GroupParentID'):
			self.parent_id = data['GroupParentID']
		if data.get('GroupParentNumber'):
			self.parent_number = data['GroupParentNumber']
		self.childs = []
		
	def dump(self, f, deep):
		self.woffset(deep, f)
		f.write(unicode(str(self.number) + ' ' + str(self.name) + '\n', 'utf8'))
		
		if self.childs:
			for child in self.childs:
				child.dump(f, deep + 1)
			
	def woffset(self, deep, f):
		for x in range(0, deep):
			f.write(unicode('  '))

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
		with io.open(self.filename + '.dump', 'w', encoding='utf8') as f:
			f.write(unicode('{\n'))
			self.root.dump(f, 0)
			f.write(unicode('}\n'))
		
		