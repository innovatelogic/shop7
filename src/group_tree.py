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