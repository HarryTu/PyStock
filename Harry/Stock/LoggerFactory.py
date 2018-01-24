'''
Created on 20180124

@author: tuh
'''

import logging
import time 

def getLogger(name):
    
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
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter( formatter )
            
#         logfile_handler = logging.FileHandler( logfile )
#         logfile_handler.setFormatter( formatter )

        logger = logging.getLogger(name)
        
        logger.addHandler( console_handler )
#         logger.addHandler( logfile_handler )
        logger.setLevel( logging.INFO )
        
        return logger
    
    except Exception, e: 
        
        print "Logger factory creation failed with error message:" +"\n" + str(e) 
        
        return None
    

if __name__ == '__main__':
    
    logger = getLogger('DBOperation')
    
    if logger is not None: 
        
        logger.error("this is a test")
    