# -*- coding=UTF-8 -*-

'''
Created on 20180127

@author: Harry
'''

from Harry.Stock import DBDataHandle
import StockDataByTX
import LoggerFactory
import DBOperation

def DailyHisData(dboper):
    
    logger = LoggerFactory.getLogger("DailyHisData")
    
    codelist = DBDataHandle.GetStockCode(dboper)
    
    if codelist is not None and len(codelist) > 1:
        
        for code in codelist:
             
            realtimeData = StockDataByTX.CollectRealTimeData(code[0], logger) 
              
            if realtimeData is not None: 
                
                logger.info("正在处理: %s" % realtimeData['code'])
                
                DBDataHandle.InsertHisData(dboper, realtimeData, logger)
                  
            else: 
                  
                logger.error("股票: %s 的相关信息获取失败..." % code)
#             
    else: 
        
        logger.error("股票代码信息获取失败.....")


if "__name == __main__":
    
    dboper = DBOperation.DBConnection()
    DailyHisData(dboper)   
    
    