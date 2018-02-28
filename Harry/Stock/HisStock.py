# -*- coding=UTF-8 -*-

'''
Created on 20180127

@author: Harry
'''

from Harry.Stock import DBDataHandle
import StockDataByTX
import LoggerFactory
import DBOperation
import threading
import time
import datetime
import tushare as ts


def DailyHisData(dboper):
    
#     logger = LoggerFactory.getLogger("DailyHisData")
    
    codelist = DBDataHandle.GetStockCode(dboper)
    
    if codelist is not None and len(codelist) > 1:
         
        for code in codelist:
             
            threading.Thread(target=InsertHisData, args=(code[0], dboper)).start()
            time.sleep(0.1)
        
    else: 
        
        LoggerFactory.error("DailyHisData", "股票代码信息获取失败.....")


def InsertHisData(code,dboper):

    realtimeData = StockDataByTX.CollectRealTimeData(code) 
          
    if realtimeData is not None: 
        
        LoggerFactory.info("InsertHisData", "正在处理: %s" % realtimeData['code'])
        
        DBDataHandle.InsertHisData(dboper, realtimeData)
          
    else: 
        
        LoggerFactory.error("InsertHisData", "股票: %s 的相关信息获取失败..." % code)


if "__name == __main__":
    
    week_day = datetime.date.today().weekday()
    
    if ( week_day == 5 or week_day == 6 ): 
    
        LoggerFactory.info("HisStock", "Today is weekend, no historic data need to be collected.....")
    
    else: 
        
        dboper = DBOperation.DBOperation()
        DailyHisData(dboper)

