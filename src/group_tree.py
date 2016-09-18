import os, sys
import codecs, json, io
import codecs
from pprint import pprint

class Node:
	def __init__(self, data):
		self.name = data['GroupName']
		self.number = data['GroupNumber']
		self._id = None
		self._parent_id = None
		self.id = None # old data id from xlsx file
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
			

def dump_tree(filename, root):
	print("opening damp groups file:" + filename + '.dump')
	with io.open(filename + '.dump', 'w', encoding='utf8') as f:
		print("opening OK")
		f.write(unicode('{\n'))
		root.dump(f, 0)
		f.write(unicode('}\n'))
		
def dump_tree_flat(filename, root):
	print("opening flat dump groups file:" + filename + '.flat')
	with io.open(filename + '.flat', 'w', encoding='utf8') as f:
		print("opening OK")
		flat = flatten_tree(root)
		for item in flat:
			f.write(unicode(str(item.number) + ' ' + str(item.name) + ' ', 'utf8'))
			if item.parent_number:
				f.write(unicode(str(item.parent_number) + ' ', 'utf8'))
			if item._id:
				f.write(unicode(str(item._id) + ' ', 'utf8'))
			if item._parent_id:
				f.write(unicode(str(item._parent_id) + ' ', 'utf8'))
			f.write(unicode('\n', 'utf8'))

def flatten_tree(root):
	flat_array = []
	if root:
		top = root
		index_last = 0
		flat_array.append(top)
		while top:
			for child in top.childs:
				flat_array.append(child)
			index_last += 1
			top = flat_array[index_last] if len(flat_array) > index_last else None
			
	return flat_array
	
def unflatten_tree(self, plain_arr):
	new_root = None
	return new_root
	
def find_node_by_number(number, node):
	if node:
		if node.number == number:
			return node
		for child in node.childs:
			out = find_node_by_number(number, child)
			if out:
				return out
	return None