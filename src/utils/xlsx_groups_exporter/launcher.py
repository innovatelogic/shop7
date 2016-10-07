#!/usr/bin/env python
import sys
import argparse
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from cache_data import CacheData
from builder_db import BuilderDB

def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='input data folder')
    parser.add_argument('--dbhost', type=str, help='database host name')
    parser.add_argument('--dbport', type=str, help='database port')
    parser.add_argument('--dbname', type=str, help='database name')
    args = parser.parse_args()
    
    specs = dict()
    
    if not hasattr(args, 'input'):
        raise Exception('no input attribute')
    
    specs['input'] = { 'path':path.abspath(args.input) + '/'} 
    
    specs['db'] = {
        'host':args.dbhost,
        'port':args.dbport,
        'name':args.dbname
        }
    
    try:
        print("Script started")
        
        cache = CacheData(specs)
        cache.generate()
        
        builder = BuilderDB(specs, cache.tree)
        builder.build()
        
        print("Script finished")
        
    except Exception:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1]) 
        
    return 1

if __name__== "__main__":
    main()