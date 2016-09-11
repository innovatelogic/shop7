import os, sys, shutil, argparse
from openpyxl import Workbook
from openpyxl import load_workbook

def main():
	parser = argparse.ArgumentParser()
	
	print("start")

	wb = load_workbook('../data/data.xlsx')
	
	print wb.get_sheet_names()
	
	for sheet in wb:
		print(sheet.title)
	
	ws = wb.active 
	#ws0 = wb.get_sheet_by_name("Export Products Sheet")
	
	#print(ws0.columns)
	
	for row in ws.iter_rows('A1:C2'):
		for cell in row:
			print cell.value
	return 1
	
if __name__== "__main__":
	main()