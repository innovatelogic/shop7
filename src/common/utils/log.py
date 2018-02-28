#----------------------------------------------------------------------------------------------
# color print & logging tool
# Author: Yurg
#----------------------------------------------------------------------------------------------

import sys
from sys import platform
import logging
import time

# console colorors tags
class TxtColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#----------------------------------------------------------------------------------------------
def disable():
    TxtColor.HEADER = ''
    TxtColor.OKBLUE = ''
    TxtColor.OKGREEN = ''
    TxtColor.WARNING = ''
    TxtColor.FAIL = ''
    TxtColor.ENDC = ''
    TxtColor.BOLD = ''
    TxtColor.UNDERLINE = ''

#----------------------------------------------------------------------------------------------
def Init(log_filename):
    logging.basicConfig(filename=log_filename,
                        #level=logging.DEBUG,
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(threadName)-10s %(message)s')
    #if platform == 'win32':
    #    disable()

#----------------------------------------------------------------------------------------------
def Log(msg):
    logging.info("Master Server Starts")
    pass

#----------------------------------------------------------------------------------------------
def Msg(msg):
    print(msg)
    Log(msg)
    pass

#----------------------------------------------------------------------------------------------
def Comment(msg):
    print(TxtColor.OKBLUE + msg + TxtColor.ENDC)
    Log(msg)
    pass

#----------------------------------------------------------------------------------------------
def MsgOK(msg):
    print(TxtColor.OKGREEN + msg + TxtColor.ENDC)
    Log(msg)
    pass

#----------------------------------------------------------------------------------------------
def MsgOk(msg):
    MsgOK(msg)
    pass

#----------------------------------------------------------------------------------------------
def Warning(msg):
    print(TxtColor.WARNING + msg + TxtColor.ENDC)
    Log(msg)
    pass

#----------------------------------------------------------------------------------------------
def Error(msg):
    print(TxtColor.FAIL + msg + TxtColor.ENDC)
    Log(msg)
    pass

#----------------------------------------------------------------------------------------------
def Fail(msg):
    print(TxtColor.FAIL + TxtColor.BOLD + msg + TxtColor.ENDC)
    Log(msg)
    sys.exit()
    pass

#----------------------------------------------------------------------------------------------
def Bold(msg):
    print(TxtColor.BOLD + msg + TxtColor.ENDC)
    Log(msg)
    pass

#----------------------------------------------------------------------------------------------
def Underline(msg):
    print(TxtColor.UNDERLINE + msg + TxtColor.ENDC)
    Log(msg)
    pass
