# -*- coding=UTF-8 -*-

'''
Created on 20180129

@author: tuh
'''

import DBOperation
import time
import sys
import os
from copy import deepcopy 

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
    
#     sql = "select code, name, cashin, cashout, initnetvalue, netvalue, iorate, turnover, \
#             initchangeratio, changeratio, amountp,inittime,price from mystocks where mtype=1 order by changeratio desc" 
    
    sql = "select b.code, a.name, b.cashin, b.cashout, b.initnetvalue, b.netvalue, b.iorate, b.turnover, \
        b.initchangeratio, b.changeratio, b.amountp, b.inittime, b.price, a.industry from stocks a, mystocks b where a.code=b.code and b.mtype=1 order by b.changeratio desc" 
    
    stocklist = []
    
    results = dboper.queryData(sql)
    
    if results is not None and len(results)>0:
        
        for stock in results: 
            
            stockData = {}
            stockData['code'] = stock[0]
            stockData['name'] = stock[1]
            stockData['initnetvalue'] = stock[4]
            stockData['netvalue'] = stock[5]
            stockData['iorate'] = stock[6]
            stockData['turnover'] = stock[7]
            stockData['initchangeratio'] = stock[8]
            stockData['changeratio'] = stock[9]
            stockData['amountp'] = stock[10]            
            stockData['inittime'] = stock[11].strftime('%H:%M:%S')
            stockData['price'] = stock[12]
            stockData['industry'] = stock[13]
 
        
            stocklist.append(deepcopy(stockData)) 
        
        return stocklist
    
    else: 
        
        return None
    
    
def GetJJMyStockReport(dboper):
    
#     sql = "select b.code, a.name, a.industry, b.netvalue, b.amountp, b.initchangeratio, b.changeratio, b.price, b.pricerate, b.qrratio, b.turnover \
#             from stocks a, mystocks b \
#             where a.code=b.code and b.mtype=0 order by b.changeratio desc"
 
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')"
#     mytime = "str_to_date('2018-02-23','%Y-%m-%d')"
    
    sql = "select b.code, a.name, a.industry, b.netvalue, b.amountp, b.initchangeratio, b.changeratio, b.price, b.pricerate, b.qrratio, b.turnover, c.netvalue, c.turnover, c.amountp \
        from stocks a, mystocks b, jjstocks c \
        where a.code=b.code and c.code = b.code and b.mtype=0 and c.mtime >= %s order by b.changeratio desc"  % mytime

    stocklist = []
    
    results = dboper.queryData(sql)
    
    if results is not None and len(results)>0:
        
        for stock in results: 
            
            stockData = {}
            stockData['code'] = stock[0]
            stockData['name'] = stock[1]  
            stockData['industry'] = stock[2]  
            stockData['netvalue'] = stock[3]
            stockData['amountp'] = stock[4]
            stockData['initchangeratio'] = stock[5]
            stockData['changeratio'] = stock[6]
            stockData['price'] = stock[7]
            stockData['pricerate'] = stock[8]
            stockData['qrratio'] = stock[9]
            stockData['turnover'] = stock[10]
            stockData['jjnetvalue'] = stock[11]
            stockData['jjturnover'] = stock[12]
            stockData['jjamountp'] = stock[13]

            stocklist.append(deepcopy(stockData)) 
        
        return stocklist
    
    else: 
        
        return None
    
if __name__ == '__main__':
            
    dboper = DBOperation.DBOperation()
    PrintMyStockReport(dboper)

    
        
