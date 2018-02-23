# -*- coding=UTF-8 -*-

'''
Created on 20180124

@author: HarryTu
'''

import logging
import time 
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def __getLogger(name):
    
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    
    logfile = 'c:/tmep/stock.log'
        
#     logging.basicConfig(
#            
#             level = logging.INFO,
#             format   = now +" ~ " + name + ' LINE %(lineno)-4d  %(levelname)-8s %(message)s',
#             filename = 'c:/tmp/stock.log',
#             datefmt = '%m-%d %H:%M',
#         
#             )
    
    formatter = logging.Formatter( now +" ~ " + name + ' LINE %(lineno)-4d  %(levelname)-8s %(message)s',)
    
    try: 
        
        handler = logging.StreamHandler()
        handler.setFormatter( formatter )
            
#         logfile_handler = logging.FileHandler( logfile )
#         logfile_handler.setFormatter( formatter )

        logger = logging.getLogger(name)
        
        logger.addHandler( handler )
#         logger.addHandler( logfile_handler )
        logger.setLevel( logging.INFO )
        
        return logger, handler
    
    except Exception, e: 
        
        print "Logger factory creation failed with error message:" +"\n" + str(e) 
        
        return None


def debug(name, msg):
    
    logger, handler = __getLogger(name)
    
    logger.debug(msg)
    
    logger.removeHandler(handler)
    

def info(name, msg):
    
    logger, handler = __getLogger(name)
    
    logger.info(msg)
    
    logger.removeHandler(handler)
    

def error(name, msg):
    
    logger, handler = __getLogger(name)
    
    logger.error(msg)
    
    logger.removeHandler(handler)    
        

if __name__ == '__main__':
    
   print ""
    