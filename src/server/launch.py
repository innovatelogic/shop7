#!/usr/bin/env python
import argparse

from master_server import MasterServer

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help='server host')
    parser.add_argument('--db_name', help='database name')
    
    args = parser.parse_args()
    
    specs = dict()
    
    specs['master'] = {
        'host':args.host,
        'db_name':args.db_name
        }
    
    master = MasterServer(specs)
    
    master.run()

if __name__== "__main__":
    main()