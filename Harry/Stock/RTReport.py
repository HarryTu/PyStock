# -*- coding=UTF-8 -*-

'''
Created on 20180129

@author: tuh
'''

import DBOperation
import time
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

def GetRTReport(iorate,amountp,dboper):
    
    sql = "select a.code,a.name,b.netvalue,b.iorate,b.turnover,b.changeratio,b.amountp from stocks a, rtstocks b \
            where a.code=b.code and b.iorate>=%0.2f and b.amountp>=%0.2f order by b.iorate"%(iorate,amountp)
    
    while True:
        
        os.system("cls")
        
        results = dboper.queryData(sql)
        
        if results is not None and len(results) > 0:
            
            for stock in results: 
                
                print "code: " + stock[0] + "  ", 
                print "name: " + stock[1] + "  ", 
                print "netvalue: " + str(stock[2]) + "  ",
                print "iorate: " + str(stock[3]) + "  ",
                print "turnover: " + str(stock[4]) + "  ",
                print "changerate: " + str(stock[5]) + "  ",
                print "amountp: " + str(stock[6])
                
        else: 
            
            print "No data can be found!!"
        
        time.sleep(30)
        print "Complete!"
        print " "
    

if __name__ == '__main__':
        
    dboper = DBOperation.DBOperation()
    
    iorate = 1.5
    amountp = 8000
    
    GetRTReport(iorate,amountp,dboper)