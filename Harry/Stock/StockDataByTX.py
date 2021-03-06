
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
from pymysql import NULL

reload(sys)
sys.setdefaultencoding('utf-8')


def GetStockData(dataUrl):
    
    r = urllib2.Request(dataUrl)
    
    try:
        
        data = urllib2.urlopen(r, data=None, timeout=2)
        
    except Exception,e:
        
        LoggerFactory.error("GetStockData", "GetDataFromUrl error.... URL: %s"%dataUrl)
#         logger.error("GetDataFromUrl error.... URL: %s"%dataUrl)   
            
        return None
      
    return data.read().decode('gbk').replace('"', '').split('~')


def GetStockBasicData(code):
    
    baseurl = "http://qt.gtimg.cn/q="
    url = baseurl + code
    
    stockBasicData = {}
    
    LoggerFactory.debug("GetStockBasicData", "GetStockBasicData_URL: %s" % url)
#     logger.debug("GetStockBasicData_URL: %s" % url)
    
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
            #股票代码别名
            stockBasicData['codealias'] = code
            #股票名称
            stockBasicData['name'] = data[1]
            #实际流通市值(万)
            stockBasicData['circulated_stock'] = float((data[44]))*10000
            #总市值（万）
            stockBasicData['total_stock'] = float(data[45])*10000
            #板块
            stockBasicData['scope']= ''
            #动态市盈率
            stockBasicData['peg'] = float('0')
#             stockBasicData['peg'] = float(data[52])
            #量比
            stockBasicData['qrratio'] = float(data[49])
            #静态市盈率
            stockBasicData['lyr'] = float('0')
#             stockBasicData['lyr'] = float(data[53].split(';')[0])
            #当日总交易量(万)
    #         stockBasicData['volume_amout'] = round( int(data[36]) / 10000, 2)
            #当日换手率(万)
            stockBasicData['turnover_rate'] = float(data[38])
            #当前成交量
            stockBasicData['price'] = float(data[3])
            #当前价格
            stockBasicData['mount'] = float(data[5])
               
            return stockBasicData
        
        except Exception, e: 
            
            LoggerFactory.error("GetStockBasicData", "Set value error: " + "\n" + str(e))
#             logger.error("Set value error: " + "\n" + str(e))
#             logger.debug("code: " + code[2:8])
#             logger.debug("circulated_stock: " + data[44])
#             logger.debug("total_stock: " + data[45])
#             logger.debug("peg: " + data[52])
#             logger.debug("lyr: " + data[53])
            
            return None
        
    else: 
           
        return None


def GetStockCashData(code):
    
    baseurl = "http://qt.gtimg.cn/q=ff_"
    url = baseurl + code
    
    LoggerFactory.debug("GetStockCashData", "GetStockCashData_url: %s" % url)
#     logger.debug("GetStockCashData_url: %s" % url)
    stockCashData = {}
    
    data = GetStockData( url )
      
    if data is not None and len(data) > 1:
        
        try: 
            
            #主力流入(万)
            stockCashData['main_in_cash'] = float(data[1])
            #主力流出(万)
            stockCashData['main_out_cash'] = float(data[2])
            #主力净额  
            stockCashData['netvalue'] = float(data[3])
            #股票名称
            stockCashData['name'] = data[12]
            #交易时间
            stockCashData['date'] = data[13]
             
            return stockCashData
        
        except Exception, e:
            
            LoggerFactory.error(GetStockCashData, "Set value error: " + "\n" + str(e))
#             logger.error("Set value error: " + "\n" + str(e))
            
            return None
     
    else:
     
        return None  
    

def GetStockBriefData(code):
    
    baseurl = "http://qt.gtimg.cn/q=s_"
    
    url = baseurl + code    
    
    LoggerFactory.debug("GetStockBriefData", "GetStockBriefData_url: %s" % url)
#     logger.debug("GetStockBriefData_url: %s" % url)
    
    stockBriefData = {}
    
    data = GetStockData( url )
          
    if data is not None and len(data) > 1:
        
        try: 
            
            #当前价格
            stockBriefData['price'] = float(data[3]) 
            #当前涨跌幅    
            stockBriefData['changeratio'] = float(data[5])
            #成交金额（万）
            stockBriefData['amountp'] = float(data[7])
            #成交量（手）(万)
            stockBriefData['amountn'] = round(float(data[6])/10000, 2)
            
            return stockBriefData
        
        except Exception, e: 
            
            LoggerFactory.error("GetStockBriefData", "Set value error" + "\n" + str(e))
#             logger.error("Set value error" + "\n" + str(e))
            
            return None
    else:
          
        return None


def CollectRealTimeData(code):
    
#     logger = LoggerFactory("CollectRealTimeData")
    
    stockBasicData = GetStockBasicData(code)
    stockCashData = GetStockCashData(code)
    stockBriefData = GetStockBriefData(code)
    
    realtimeData = {}
    
    if stockBasicData is not None: 
        if stockCashData is not None:
            if stockBriefData is not None:
        
                rate = 0 
                
                if float(stockCashData['main_out_cash']) > 0:
                         
                    rate = round((float(stockCashData['main_in_cash']) / float(stockCashData['main_out_cash'])), 2)
            
                realtimeData['code'] = code[2:8]
                realtimeData['price'] = stockBriefData['price']
                realtimeData['cashin'] = stockCashData['main_in_cash']
                realtimeData['cashout'] = stockCashData['main_out_cash']
                realtimeData['netvalue'] = stockCashData['netvalue']
                realtimeData['changeratio'] = stockBriefData['changeratio']
                realtimeData['turnover'] = stockBasicData['turnover_rate']
                realtimeData['qrratio'] = stockBasicData['qrratio']
                realtimeData['iorate'] = float(rate)
                realtimeData['amountp'] = stockBriefData['amountp']
                realtimeData['amountn'] = stockBriefData['amountn']
                realtimeData['time'] = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')" 
                
                return realtimeData
                
            else: 
                
                LoggerFactory.debug("CollectRealTimeData","stockBriefData is null")
#                 logger.debug("stockBriefData is null")
                
                return None
        else: 
            
            LoggerFactory.debug("CollectRealTimeData","stockCashData is null")
#             logger.debug("stockCashData is null")
            
            return None
    else:
            
            LoggerFactory.debug("CollectRealTimeData","stockBasicData is null")
#             logger.debug("stockBasicData is null")
            
            return None


def DonwloadAllStockBasic( FilePath ):
    
    if os.path.isfile( FilePath ):
        
        os.remove( FilePath )
        
        LoggerFactory.info("DonwloadAllStockBasic", "Will remove the old file and refresh stock list...........")
#         logger.info("Will remove the old file and refresh stock list...........")
    
    try: 
        
        LoggerFactory.info("DonwloadAllStockBasic", "Starting new stock list download....")
#         logger.info("Starting new stock list download....")
        
        df = ts.get_stock_basics()
        
        df.to_csv( FilePath, encoding='utf-8' )
        
        LoggerFactory.info("DonwloadAllStockBasic", "New stock list has been created successfully!")
    
    except Exception, e:
        
        LoggerFactory.error("DonwloadAllStockBasic", "Creating new stock list failed by tushare, please check!!! ")
        
        exit
        
        
def GetAllStockCode( FilePath ):
    
    stocklist = []
 
    csvFile = open( FilePath,'r')
              
    reader = csv.reader( csvFile )
           
    for item in reader: 
               
        basicInfo = {}
        
        if reader.line_num == 1:
                              
            continue
        
        if item[0][0:1] == '0' or item[0][0:1] == '3':    
            codename = 'sz' + item[0] 
            basicInfo['code'] = codename
            
        elif item[0][0:1] == '6':
            codename = 'sh' + item[0]
            basicInfo['code'] = codename
        
        else:
            codename = '00000000'
            basicInfo['code'] = codename
        
        basicInfo['industry'] = item[2]
        basicInfo['area'] = item[3]
        
        stocklist.append(basicInfo)
        
    return stocklist


def CollectData( file ):
     
    codelist = GetAllStockCode( file )
    
    for codename in codelist:     
        
        basicdata = GetStockBasicData( codename )
        cashdata = GetStockCashData( codename )
        
        if basicdata is not None and cashdata is not None: 
            print ""
            
            


            
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
    
#     print ""
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
#     
# #     realtimeData = CollectRealTimeData('sz002129', logger)
    DonwloadAllStockBasic( file )
#  
#     initStockDB( file )
#     stockData = CollectRealTimeData('sh600159',logger )
#     #当前成交量
#     print stockBasicData['price'] 
#     #当前价格
#     print stockBasicData['mount']
#     print stockData['qrratio']
#     if stockBasicData['price'] == 0 and stockBasicData['mount'] == 0:
#         print "stop"
#     else:
#         print "nornal"
#     stockCashData = NULL
#     stockBasicData = NULL

        