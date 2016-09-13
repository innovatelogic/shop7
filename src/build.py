import os, sys, shutil, argparse
import codecs, json, io
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter


def letter_to_index(letter):
    """Converts a column letter, e.g. "A", "B", "AA", "BC" etc. to a zero based
    column index.

    A becomes 0, B becomes 1, Z becomes 25, AA becomes 26 etc.

    Args:
        letter (str): The column index letter.
    Returns:
        The column index as an integer.
    """
    letter = letter.upper()
    result = 0

    for index, char in enumerate(reversed(letter)):
        # Get the ASCII number of the letter and subtract 64 so that A
        # corresponds to 1.
        num = ord(char) - 64

        # Multiply the number with 26 to the power of `index` to get the correct
        # value of the letter based on it's index in the string.
        final_num = (26 ** index) * num

        result += final_num

    # Subtract 1 from the result to make it zero-based before returning.
    return result - 1


def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	parser = argparse.ArgumentParser()

	print("start script")
		
	with io.open('../data/db_cache.json', 'w', encoding='utf8') as f:

		print("open cache file")

		wb = load_workbook('../data/data.xlsx')
			
		ws = wb.active 

		print wb.get_sheet_names()
		
		#for sheet in wb:
		#	print(sheet.title)
			
		row_count = ws.max_row - 1
		max_column = ws.max_column
		
		print('rows:' + str(row_count))
		print('columns:' + str(max_column) + ":" + get_column_letter(max_column))

		#ws0 = wb.get_sheet_by_name("Export Products Sheet")
		
		#print(ws0.columns)
		
		range = 'B1:' + get_column_letter(max_column) + str(row_count)
		for row in ws.iter_rows(range):
			row_dict = {}
			for cell in row:
				if cell.value != None:
					if cell.column == 'B':
						row_dict['Name'] = cell.value
					elif cell.column == 'F':
						row_dict['Price'] = cell.value
					#f.write(str(cell.value) + '\n')
		
			json_str = json.dumps(row_dict, ensure_ascii=False)
			#json.dump(row_dict, f)
			f.write(json_str + '\n')
		
	return 1
	
if __name__== "__main__":
	main()