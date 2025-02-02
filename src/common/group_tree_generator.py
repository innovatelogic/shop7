import os, sys
import codecs, json, io
from pprint import pprint
from group_tree import Node, find_node_by_number, dump_tree, dump_tree_flat

class GroupTreeGenerator:
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

			self.build_tree(arr_groups)
		
		# debugging
		#dump_tree(self.filename, self.root)
		#dump_tree_flat(self.filename, self.root)
			
	def build_tree(self, arr_plain):
		self.root = Node(arr_plain[0]) #zero element is a root
		del arr_plain[0]
		
		#add first level descents
		descents = []
		for item in arr_plain:
			if not item.get('GroupParentNumber'):
				descents.append(item)
		for node in descents:
			new_node = Node(node)
			
			#custom add reference to root as it does not exist in current version of xlsx file
			new_node.parent_number = self.root.number 
			self.root.childs.append(new_node)
			arr_plain.remove(node)
		
		#link other nodes
		while arr_plain:
			to_remove = []
			for item in arr_plain:
				parent_number = item['GroupParentNumber']
				parent = find_node_by_number(parent_number, self.root)
				if parent:
					parent.childs.append(Node(item))
					to_remove.append(item)
					
			#add exception if to_remove empty
			for node in to_remove:
				arr_plain.remove(node)
				
	

		