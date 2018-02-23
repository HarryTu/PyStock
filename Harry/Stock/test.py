# -*- coding=UTF-8 -*-

'''
Created on 20180127

@author: Harry
'''

import LoggerFactory
import time



for i in range(0,5):
    
    
    LoggerFactory.info("test", "test" + str(i))
    time.sleep(2)
    
    
    