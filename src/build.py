import os, sys, shutil, argparse
import codecs
from openpyxl import Workbook
from openpyxl import load_workbook

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	parser = argparse.ArgumentParser()
	
	f = open('db', 'w')

	print("start")
	
	#if sys.stdout.encoding != 'cp850':
	#	sys.stdout = codecs.getwriter('cp850')(sys.stdout, 'strict')
	#if sys.stderr.encoding != 'cp850':
	#	sys.stderr = codecs.getwriter('cp850')(sys.stderr, 'strict')

	wb = load_workbook('../data/data.xlsx')
	
	print wb.get_sheet_names()
	
	for sheet in wb:
		print(sheet.title)
	
	ws = wb.active 
	#ws0 = wb.get_sheet_by_name("Export Products Sheet")
	
	#print(ws0.columns)
	
	for row in ws.iter_rows('A1:AY5768'):
		for cell in row:
			if cell.value != None:
				f.write(str(cell.value))
			
	return 1
	
if __name__== "__main__":
	main()