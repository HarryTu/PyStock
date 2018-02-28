# -*- coding=UTF-8 -*-

'''
Created on 20180127

@author: Harry
'''

import datetime
 
today = datetime.date.today() 
weekday = today.weekday() 

if weekday == 0:
    print "周一"
else:
    print "other days"


#view-source:http://basic.10jqka.com.cn/300140/concept.html
    
    