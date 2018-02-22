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
    
    logger = LoggerFactory.getLogger("DailyHisData")
    
    codelist = DBDataHandle.GetStockCode(dboper)
    
    if codelist is not None and len(codelist) > 1:
         
        for code in codelist:
             
            InsertHisData(code[0], dboper, logger)

        
    else: 
        
        logger.error("股票代码信息获取失败.....")


def InsertHisData(code,dboper,logger):

    realtimeData = StockDataByTX.CollectRealTimeData(code, logger) 
          
    if realtimeData is not None: 
        
        logger.info("正在处理: %s" % realtimeData['code'])
        
        DBDataHandle.InsertHisData(dboper, realtimeData, logger)
          
    else: 
          
        logger.error("股票: %s 的相关信息获取失败..." % code)


if "__name == __main__":
    
#     dboper = DBOperation.DBOperation()
#     DailyHisData(dboper)

   td = ts.get_realtime_quotes('600519')
   
   for i in td: 
       print i
    