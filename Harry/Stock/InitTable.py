# -*- coding=UTF-8 -*-

'''
Created on 20180129

@author: HarryTu
'''
import DBOperation
import LoggerFactory
import StockDataByTX
import time
import DBDataHandle


def initStockDB( file ):
    
    logger = LoggerFactory.getLogger("InitStockDB")
    loggerBasicData = LoggerFactory.getLogger("GetStockBasicData")
    
    codelist = StockDataByTX.GetAllStockCode( file )
    
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')" 
    
    dboper = DBOperation.DBOperation()
    
    counter = 0
    
    for code in codelist:
        
        stockBasicData = StockDataByTX.GetStockBasicData( code,loggerBasicData )
        
        if stockBasicData is not None: 
            
            logger.info("正在处理:  %s" % stockBasicData['name'])
            
            if stockBasicData['mount'] == 0:
                status = 0
            else:
                status = 1
            
            sql = "insert into stocks(code, codealias, name, scope, circulated, totalstock, status, peg, lyr, mtime)  values('%s', '%s', '%s', '%s', %0.2f, %0.2f, %d, %0.2f, %0.2f, %s )" \
                    %(stockBasicData['code'], stockBasicData['codealias'], stockBasicData['name'], stockBasicData['scope'], stockBasicData['circulated_stock'], \
                      stockBasicData['total_stock'], status, stockBasicData['peg'], stockBasicData['lyr'], mytime)            
            
            dboper.sqlExecute( sql )
            
            counter = counter + 1
    
    logger.info("Stock DB initialization has completed! There're %s Stocks created into the Database!" % str(counter))      



def InitRTStocks( circulated, dboper, logger ):
    
    sql = "select codealias from stocks where status=1 and circulated<= %0.2f" % circulated
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    
    codelist = dboper.queryData(sql)
    
    if codelist is not None and len(codelist) > 0:
            
            clear_sql = "delete from rtstocks"
            
            logger.info("清除rtstocks表中旧数据.....")
            dboper.sqlExecute( clear_sql )
            
            logger.info("初始化RTStock表...总有 %s只股票需要处理!!"%len(codelist))
            
            for code in codelist:
                 
                realtimeData = StockDataByTX.CollectRealTimeData(code[0], logger) 
                  
                if realtimeData is not None: 
                    
                    logger.info("正在处理: %s" % realtimeData['code'])
                    
                    DBDataHandle.InsertRTData(realtimeData, logger, mytime)
                      
                else: 
                      
                    logger.error("股票: %s 的相关信息获取失败..." % code)
    #
            logger.info("初始化RTStock表完成!")
    else: 
            
        logger.error("股票代码列表信息获取失败.....")
    

if __name__ == '__main__':
    
    circulated = 1800000
    
    dboper= DBOperation.DBOperation()
    logger = LoggerFactory.getLogger("InitRTStocks")
    
    InitRTStocks(circulated, dboper, logger)
    