#!/usr/bin/env python
import os, sys
import argparse
import logging
import time

from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from master_server import MasterServer

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
        
def init_logging(path_dir):
    ensure_dir(path_dir)
    log_filename  = time.strftime("ms_%d%m%y_%H-%M.log", time.localtime())
    log_filename = path_dir + '/' + log_filename
    logging.basicConfig(filename=log_filename,
                        #level=logging.DEBUG,
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help='server host')
    parser.add_argument('--db_name', help='database name')
    parser.add_argument('--dbhost', type=str, help='database host name')
    parser.add_argument('--dbport', type=str, help='database port')
    parser.add_argument('--dbname', type=str, help='database name')
    parser.add_argument('--ms_auth_queue', type=str, help='master-auth queue name')
    parser.add_argument('--ms_client_queue', type=str, help='master-client queue name')
    parser.add_argument('--ms_queue_port', type=str, help='master-client queue port')
    parser.add_argument('--res', type=str, help='resource data folder')
    
    args = parser.parse_args()
    
    if not hasattr(args, 'host'):
        raise Exception("Not host argument")
   
    if not hasattr(args, 'dbhost'):
        raise Exception("Not dbhost argument")
    if not hasattr(args, 'dbport'):
        raise Exception("Not dbport argument")
    if not hasattr(args, 'dbname'):
        raise Exception("Not dbname argument")
    
    if not hasattr(args, 'ms_auth_queue'):
        raise Exception("Not ms_auth_queue argument")
    if not hasattr(args, 'ms_client_queue'):
        raise Exception("Not ms_client_queue argument")
    if not hasattr(args, 'ms_queue_port'):
        raise Exception("Not ms_queue_port argument")
    if not hasattr(args, 'res'):
        raise Exception("Not resource folder")
    
    specs = dict()
    
    specs['master'] = {
        'host':args.host,
        'db_name':args.db_name,
        'ms_auth_queue':args.ms_auth_queue,
        'ms_client_queue':args.ms_client_queue,
        'ms_queue_port':int(args.ms_queue_port),
        'res':args.res,
        }
    
    specs['db'] = {
        'host':args.dbhost,
        'port':args.dbport,
        'name':args.dbname
        }
    
    #directory mapping
    proj_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    
    specs['path'] = {
        'proj_dir':proj_dir,
        'bin_dir':proj_dir+'\\bin',
        'logs_dir':proj_dir + '\\logs',
        'auth_proc':proj_dir+'\\bin\\auth_server.cmd',
        }
    
    init_logging(specs['path']['logs_dir'])
    
    master = MasterServer(specs)
    
    master.run()

if __name__== "__main__":
    main()