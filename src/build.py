import os, sys, shutil, argparse
import codecs, json, io
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
import cache_items


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
	
	cur_file_dir = os.path.dirname(os.path.realpath(__file__))
	proj_dir = os.path.dirname(cur_file_dir)
	data_dir = cur_file_dir + '\..\data\\'
	
	print ('cur_file_dir:' + cur_file_dir)
	print ('proj_dir:' + proj_dir)
	print ('data_dir:' + data_dir)
	
	wb = load_workbook(data_dir + 'data.xlsx')
	
	ws = wb.active
	
	print wb.get_sheet_names()
	
	items_cache = cache_items.CacheItemsDB(data_dir + 'db_cache.json', ws)
	
	items_cache.generate()

	return 1
	
if __name__== "__main__":
	main()