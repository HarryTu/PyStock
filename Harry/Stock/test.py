# -*- coding=UTF-8 -*-

'''
Created on 20180127

@author: Harry
'''

import datetime
 
# today = datetime.date.today() 
# weekday = today.weekday() 
# 
# if weekday == 0:
#     print "周一"
# else:
#     print "other days"

nowtime=datetime.datetime.now()    
detaday = datetime.timedelta(days=-1)
da_days= nowtime + detaday

print da_days.strftime('%Y-%m-%d')

    
    