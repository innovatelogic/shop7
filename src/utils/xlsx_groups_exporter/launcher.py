#!/usr/bin/env python
import sys
import argparse

from cache_data import CacheData
from writer_db import WriterDB

def main():
    try:
        print("Script started")
        
        
        print("Script finished")
        
    except Exception:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1]) 
        
    return 1

if __name__== "__main__":
    main()