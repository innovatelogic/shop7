#!/usr/bin/env python
import sys
import argparse

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from master_server import MasterServer

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help='server host')
    parser.add_argument('--db_name', help='database name')
    parser.add_argument('--dbhost', type=str, help='database host name')
    parser.add_argument('--dbport', type=str, help='database port')
    parser.add_argument('--dbname', type=str, help='database name')
    
    args = parser.parse_args()
    
    specs = dict()
    
    specs['master'] = {
        'host':args.host,
        'db_name':args.db_name
        }
    
    specs['db'] = {
        'host':args.dbhost,
        'port':args.dbport,
        'name':args.dbname
        }
    
    master = MasterServer(specs)
    
    master.run()

if __name__== "__main__":
    main()