#!/usr/bin/env python
import sys
import argparse
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from cache_data import CacheData
from writer_db import WriterDB

def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='input data folder')
    args = parser.parse_args()
    
    specs = dict()
    
    if not hasattr(args, 'input'):
        raise Exception('no input attribute')
    
    specs['input'] = { 'path':path.abspath(args.input) + '/'} 
    
    try:
        print("Script started")
        
        cache = CacheData(specs)
        
        cache.generate()
        
        print("Script finished")
        
    except Exception:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1]) 
        
    return 1

if __name__== "__main__":
    main()