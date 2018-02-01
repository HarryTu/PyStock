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

def PrintMyStockReport(dboper):
    
    sql = "select code, name, cashin, cashout, initnetvalue, netvalue, iorate, turnover, \
            initchangeratio, changeratio, amountp,inittime from mystocks order by changeratio" 
    
    while True:
        
        results = dboper.queryData(sql)
        
        if results is not None and len(results) > 0:
            
            print ("{:^30s}".format('代码')),
            print ("{:^30s}".format('股票名称')),
            print ("{:^25s}".format('上榜净额')),
            print ("{:^25s}".format('净额')),
            print ("{:^33s}".format('换手率')),
            print ("{:^20s}".format('上榜时间')),
            print ("{:^35s}".format('初始涨幅')),
            print ("{:^20s}".format('当前涨幅')),
            print ("{:^30s}".format('成交量')),
            print ("{:^32s}".format('出入比'))
            
            for stock in results: 
                
                print ("{:^10s}".format(stock[0])),
                print ("{:^10s}".format(stock[1])),
                print ("{:^6s}".format(str(stock[4]))),
                print ("{:^14s}".format(str(stock[5]))),
                print ("{:^1.2f}".format(stock[7])),
                print ("{:^12s}".format(str(stock[11])[11:])),
                print ("{:^12.2f}".format(stock[8])),
                print ("{:^6s}".format(str(stock[9]))),
                print ("{:^15.2f}".format(stock[10])),
                print ("{:^6.2f}".format(stock[6]))

                
#                 print "iorate: " + str(stock[6]) + "  ",
#                 
#                 print "initchangeratio: " + str(stock[8]) + "  ",
#                 print "changerate: " + str(stock[9]) + "  ",
#                 print "amountp: " + str(stock[10])
                
        else: 
            
            print "No data can be found!!"
        
        time.sleep(1)
        print "Complete!"
        print " "


def Test():
    
    print ("{:^10s}".format('code')),
    print ("{:^12s}".format('name')),
    print ("{:^12s}".format('netvalue')),
    print ("{:^12s}".format('turnover')),
    print ("{:^12s}".format('initchangeratio')),
    print ("{:^12s}".format('changerate')) ,
    print ("{:^12s}".format('amountp'))

    

def GetMyStockReport(dboper):
    
    sql = "select code, name, cashin, cashout, initnetvalue, netvalue, iorate, turnover, \
            initchangeratio, changeratio, amountp,inittime from mystocks order by changeratio" 
    
    
    stocklist = []
    
    results = dboper.queryData(sql)
    
    if results is not None and len(results)>0:
        
        for stock in results: 
            
            stockData = {}
            stockData['code'] = stock[0]
            stockData['name'] = stock[1]
            stockData['changeratio'] = stock[9]
        
            stocklist.append(stockData) 
        
        return stocklist
    
    else: 
        
        return None
    
    

if __name__ == '__main__':
            
    dboper = DBOperation.DBOperation()
    PrintMyStockReport(dboper)

    
        
