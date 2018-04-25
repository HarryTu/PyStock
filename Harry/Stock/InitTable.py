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
import threading
import datetime


def InitStockDB(file):
    
#     logger = LoggerFactory.getLogger("InitStockDB")
#     loggerBasicData = LoggerFactory.getLogger("GetStockBasicData")
    
    stocklist = StockDataByTX.GetAllStockCode(file)
    
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')" 
    
    dboper = DBOperation.DBOperation()
    
    counter = 0
    
    for stock in stocklist:
        
        code = stock['code']
        
        stockBasicData = StockDataByTX.GetStockBasicData(code)
        
        if stockBasicData is not None: 
            
            LoggerFactory.info("InitStockDB", "正在处理:  %s" % stockBasicData['name'])
            
            if stockBasicData['mount'] == 0:
                status = 0
            else:
                status = 1
            
            sql = "insert into stocks(code, codealias, name, industry, circulated, totalstock, status, peg, lyr, mtime, area)  values('%s', '%s', '%s', '%s', %0.2f, %0.2f, %d, %0.2f, %0.2f, %s, '%s' )" \
                    % (stockBasicData['code'], stockBasicData['codealias'], stockBasicData['name'], stock['industry'], stockBasicData['circulated_stock'], \
                      stockBasicData['total_stock'], status, stockBasicData['peg'], stockBasicData['lyr'], mytime, stock['area'])            
            
            dboper.sqlExecute(sql)
            
            counter = counter + 1
    
    LoggerFactory.info("InitStockDB", "Stock DB initialization has completed! There're %s Stocks created into the Database!" % str(counter))      


def InitRTStocks(circulated, dboper):
    
    sql = "select codealias from stocks where status=1 and circulated<= %0.2f" % circulated
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    
    codelist = dboper.queryData(sql)
    
    if codelist is not None and len(codelist) > 0:
            
            clear_sql = "delete from rtstocks"
#             clearjj_sql = "delete from rtjjstocks"
            
            LoggerFactory.info("InitRTStocks", "Refresh old data in the rtstocks tables.....")

            dboper.sqlExecute(clear_sql)
#             dboper.sqlExecute( clearjj_sql )
            
            LoggerFactory.info("InitRTStocks", "Initialing rtstocks tables... There're %s stocks need to be handled" % len(codelist))
            
            for code in codelist:
                 
                threading.Thread(target=InsertRT, args=(dboper, code[0], mytime)).start()
                time.sleep(0.1)
    #        
            LoggerFactory.info("InitRTStocks", "The rtstocks tables initialization have been completed!")
            
    else: 
        
        LoggerFactory.error("InitRTStocks", "Failed to get Stocks list.....")


def InsertRT(dboper, code, mytime):
    
    realtimeData = StockDataByTX.CollectRealTimeData(code) 
      
    if realtimeData is not None: 
        
        LoggerFactory.info("InsertRT", "Inserting the stock: %s" % realtimeData['code'])
        
        DBDataHandle.InsertRTData(dboper, realtimeData, mytime)
        
#         DBDataHandle.InsertJJRTData(dboper, realtimeData, logger, mytime)
          
    else: 
        
        LoggerFactory.error("InsertRT", "Fetching the stock information failed. code: %s ." % code)


def InitMyStocks(dboper):
    
    sql = "delete from mystocks"
    
    LoggerFactory.info("InitMyStocks", "Initialing MyStocks table....")
    
    dboper.sqlExecute(sql)
    
    LoggerFactory.info("InitMyStocks", "Initialing MyStocks has completed!")


if __name__ == '__main__':
    
    circulated = 1800000
    
    dboper = DBOperation.DBOperation()
    
    file = 'C:/temp/stock_basic_list.csv'
    InitStockDB(file)
#     InitMyStocks(dboper, logger)
    
#     begintime = datetime.datetime.now()
#     InitRTStocks(circulated, dboper, logger)
# endtime = datetime.datetime.now()
            
#     logger.error("rtstocks has been updated. Spent time: %s"% str((endtime-begintime).seconds))
    
