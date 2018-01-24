
# -*- coding=UTF-8 -*-

'''
Created on 20180123

注释：通过腾讯股票数据接口获得当日股票实时交易数据。

@author: HarryTu
'''

from __future__ import division

import sys
import urllib2
from pytdx import params
import code
import tushare as ts
import csv
import os
import LoggerFactory
import DBOperation
import time

reload(sys)
sys.setdefaultencoding('utf-8')


def GetStockData( dataUrl):
    
    r = urllib2.Request(dataUrl)
    
    try:
        
        data = urllib2.urlopen(r, data=None, timeout=3)
        
    except Exception,e:
        
        print "getDataFromUrl error...Retrying!!!"   
            
        return None
      
    return data.read().decode('gbk').replace('"', '').split('~')


def GetStockBasicData(code, logger):
    
    baseurl = "http://qt.gtimg.cn/q="
    url = baseurl + code
    
#     print url
    
    stockBasicData = {}
    
    data = GetStockData( url )
    
#     print data[53].split(';')[0]
    
    if data is not None and len(data) > 1:
        
        try: 
            
            if not data[44]:
                data[44] = '0'
                
            if not data[45]:
                data[45] = '0'

            
            #股票代码
            stockBasicData['code'] = code[2:8]
            #股票名称
            stockBasicData['name'] = data[1]
            #实际流通市值
            stockBasicData['circulated_stock'] = float((data[44]))
            #总市值
            stockBasicData['total_stock'] = float(data[45])
            #板块
            stockBasicData['scope']= ''
            #动态市盈率
            stockBasicData['peg'] = float('0')
#             stockBasicData['peg'] = float(data[52])
            #静态市盈率
            stockBasicData['lyr'] = float('0')
#             stockBasicData['lyr'] = float(data[53].split(';')[0])
            #当日总交易量(万)
    #         stockBasicData['volume_amout'] = round( int(data[36]) / 10000, 2)
            #当日换手率(万)
    #         stockBasicData['turnover_rate'] = data[38]
               
            return stockBasicData
        
        except Exception, e: 
            
            logger.info("数据赋值部分错误: " + "\n" + str(e))
            logger.debug("code: " + code[2:8])
            logger.debug("circulated_stock: " + data[44])
            logger.debug("total_stock: " + data[45])
            logger.debug("peg: " + data[52])
            logger.debug("lyr: " + data[53])
            
            return None
        
    else: 
           
        return None


def GetStockCashData(code):
    
    baseurl = "http://qt.gtimg.cn/q=ff_"
    url = baseurl + code
    
#     print url
    
    stockCashData = {}
    
    data = GetStockData( url )
      

    if data is not None and len(data) > 1:
        #主力流入(万)
        stockCashData['main_in_cash'] = data[1]
        #主力流出(万)
        stockCashData['main_out_cash'] = data[2]
        #主力净额  
        stockCashData['netcash'] = data[3]
        #股票名称
        stockCashData['name'] = data[12]
        #交易时间
        stockCashData['date'] = data[13]
         
        return stockCashData
     
    else:
     
        return None


def DonwloadAllStockBasic( FilePath ):
    
    if os.path.isfile( FilePath ):
        print "Will refresh stock list..........."
        os.remove( FilePath )
    
    df = ts.get_stock_basics()
    
    df.to_csv( FilePath, encoding='utf-8' )
    
    print "Stock list is created or updated!"


def GetAllStockCode( FilePath ):
    
    codelist = []
        
    csvFile = open( FilePath,'r')
              
    reader = csv.reader( csvFile )
           
    for item in reader: 
               
        if reader.line_num == 1:
                              
            continue
        
        if item[0][0:1] == '0' or item[0][0:1] == '3':    
            codename = 'sz' + item[0] 
            codelist.append(codename)
        
        if item[0][0:1] == '6':
            codename = 'sh' + item[0]
            codelist.append(codename)
        
        exit 
        
    return codelist


def CollectData( file ):
     
    codelist = GetAllStockCode( file )
    
    for codename in codelist:     
        
        basicdata = GetStockBasicData( codename )
        cashdata = GetStockCashData( codename )
        
        if basicdata is not None and cashdata is not None: 
            print ""
            
            
def initStockDB( file ):
    
    logger = LoggerFactory.getLogger("InitStockDB")
    loggerBasicData = LoggerFactory.getLogger("GetStockBasicData")
    
    codelist = GetAllStockCode( file )
    
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')" 
    
    dboper = DBOperation.DBOperation()
    
    for code in codelist:
        
        stockBasicData = GetStockBasicData( code,loggerBasicData )
        
        if stockBasicData is not None: 
            
            logger.info("正在处理:  %s" % stockBasicData['name'])
            
            
            sql = "insert into stocks(code, name, scope, circulated, totalstock, peg, lyr, mtime)  values('%s', '%s', '%s', %0.2f, %0.2f, %0.2f, %0.2f, %s )" \
                    %(stockBasicData['code'], stockBasicData['name'], stockBasicData['scope'], stockBasicData['circulated_stock'], \
                       stockBasicData['total_stock'], stockBasicData['peg'], stockBasicData['lyr'], mytime)            
            
            dboper.sqlExecute( sql )
     
            
            
def logic():
    
    print ""
#     if float(cashdata['main_in_cash']) > 0 and float(cashdata['main_out_cash']) > 0:
#                 
#                 rate = round((float(cashdata['main_in_cash']) / float(cashdata['main_out_cash'])), 2)
#                         
#                 if rate > 1.5:
#                     print "股票名称: " + cashdata['name'] + '  ',
#                     print "股票代码: " + codename[2:8] + '  ',
#                     print "主力买入: " + cashdata['main_in_cash'] + '  ',
#                     print "主力卖出: " + cashdata['main_out_cash'] + '  ',
#                     print "主力净额: " + cashdata['netcash'] + '  ',
#                     print "换手率: " + basicdata['turnover_rate'] + '  ',
#                     print "出入比: " + str(rate) + '  ',
#                     print "实际流通值: " + basicdata['circulated_stock']            


if __name__=='__main__':
    
#     data = GetStockBasicData('sh603299')
#     
# #     for i in range(0,len(data)):
# #         print str(i)  " ",
# #         print data[i]
#     
# #     print data['main_in_cash']
# #     print data['main_out_cash']
# #     print data['netcash']
# #     print data['name']
#     #实际流通市值
#     print data['circulated_stock']
#     print data['total_stock']
#     print data['volume_amout']
#     print data['turnover_rate']    
    
    file = 'C:/temp/stock_basic_list.csv'
# # # #     DonwloadAllStockBasic( file )
# #     stockBasicData = GetStockBasicData('sz300738')
# #     print stockBasicData['peg']
# #     print stockBasicData['lyr']
# # 
    initStockDB( file )

    a ="0;0"
    print a.split(";")[0]
    