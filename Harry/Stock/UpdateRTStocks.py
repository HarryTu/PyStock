# -*- coding=UTF-8 -*-

'''
Created on 20180128

@author: HarryTu
'''

import DBOperation
import LoggerFactory
import DBDataHandle
import StockDataByTX
import time
import datetime
import sys
import InitTable
import threading

reload(sys)
sys.setdefaultencoding('utf-8')


def GetMarketSql(stocktype):
    
    sql = ""
    
    if stocktype == "sh":
        
        LoggerFactory.info("GetMarketSql", "Updating stock information in SH marketing.....")

        sql = "select codealias from stocks where codealias like '%s' and status=1 and circulated<= %0.2f" % ("sh%", circulated)
    
    if stocktype == "sz":
        
        LoggerFactory.info("GetMarketSql", "Updating stock information in SZ marketing.....")

        sql = "select codealias from stocks where codealias like '%s' and status=1 and circulated<= %0.2f" % ("sz%", circulated)
    
    return sql

        
def UpdateRT(dboper, code, mytime):
       
    realtimeData = StockDataByTX.CollectRealTimeData(code) 
    
    if realtimeData is not None: 
        
        LoggerFactory.debug("UpdateRT", "Updating the stock %s" % realtimeData['code'])
        
        DBDataHandle.UpdateRTData(dboper, realtimeData, mytime)

        
def InsertRT(dboper, code, mytime): 
    
    realtimeData = StockDataByTX.CollectRealTimeData(code) 
                  
    if realtimeData is not None: 
    
        LoggerFactory.info("InsertRT", "Insert the stock %s to rtstocks" % realtimeData['code'])
        
        DBDataHandle.InsertRTData(dboper, realtimeData, mytime)
    
    else: 
        
        LoggerFactory.error("InsertRT", "Fetching the stock information failed. code: %s ..." % code)
    
    
def HandleRTStock(dboper, stocktype, circulated=1800000):
    
    rtstockslist = []
    
    codelist_sql = ""
    sql = "select code from rtstocks"
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    
    rtstocks = dboper.queryData(sql)  
    
    if len(rtstocks) == 0:
        InitTable.InitRTStocks(circulated, dboper)
    
    if len(rtstocks) > 0:
        
        for code in rtstocks: 
            rtstockslist.append(code[0])
        
        codelist_sql = GetMarketSql(stocktype)
        
        results = dboper.queryData(codelist_sql) 
      
        if results is not None and len(results) > 0:
            
            LoggerFactory.info("HandleRTStock", "Starting to update rtstocks....")
            
            begintime = datetime.datetime.now()
            
            for code in results:
            
                if checkExist(code[0][2:8], rtstockslist):
                    
                    LoggerFactory.debug("HandleRTStock", "The stock %s already exists in the rtstocks, will perform update information" % code[0])
                    
                    threading.Thread(target=UpdateRT, args=(dboper, code[0], mytime)).start()
                    time.sleep(0.07)
                    
                else:
                    
                    LoggerFactory.debug("HandleRTStock", "The stock %s DOES NOT exist in the rtstocks, will insert stock information!" % code[0])
                    
                    threading.Thread(target=InsertRT, args=(dboper, code[0], mytime)).start()    
                    time.sleep(0.1)
             
            endtime = datetime.datetime.now()
            
            LoggerFactory.info("HandleRTStock", "rtstocks has been updated. Spent time: %s" % str((endtime - begintime).seconds))
 
        
        
def InsertJJStock(dboper, code, mytime):

    realtimeData = StockDataByTX.CollectRealTimeData(code) 
                  
    if realtimeData is not None: 
    
#         logger.info("Insert the stock %s to jjstocks" % realtimeData['code'])
        
#         DBDataHandle.InsertRTData(dboper, realtimeData, logger, mytime)
        DBDataHandle.InsertJJStock(dboper, realtimeData, mytime)
    
    else: 
        
        LoggerFactory.error("InsertJJStock", "Fetching the stock information failed. code: %s ..." % code)


def HandleJJStock(dboper, stocktype, circulated=1800000):  
 
#     mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')"
      
    codelist_sql = GetMarketSql(stocktype)
    
    results = dboper.queryData(codelist_sql)
    
    if results is not None and len(results) > 0:
        
        for code in results: 
            
            threading.Thread(target=InsertJJStock, args=(dboper, code[0], mytime)).start()    
            
            time.sleep(0.1)

    else: 

        LoggerFactory.error("HandleJJStock", "There is no stock list retrieved...")



def InsertJJTemp(dboper, code, mytime):

    realtimeData = StockDataByTX.CollectRealTimeData(code) 
                  
    if realtimeData is not None: 
        
        realtimeData['codealias'] = code
        
        LoggerFactory.info("InsertJJTemp", "Insert the stock %s to JJTemp" % realtimeData['code'])
        
        DBDataHandle.InsertJJTemp(dboper, realtimeData, mytime)
    
    else: 
        
        LoggerFactory.error("InsertJJTemp", "Fetching the stock information failed. code: %s ..." % code)


def UpdateJJTemp(dboper, code, mytime):
    
    realtimeData = StockDataByTX.CollectRealTimeData(code) 
  
    if realtimeData is not None: 
        
        LoggerFactory.debug("UpdateJJTemp", "Updating the stock %s" % realtimeData['code'])
        
        DBDataHandle.UpdateJJTemp(dboper, realtimeData, mytime)


def InitJJTemp(dboper, stocktype, circulated):
    
#     sql_clear = "delete from jjtemp"
#     results = dboper.sqlExecute(sql_clear)
    results = True
    if results: 
    
        mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
           
        codelist_sql = GetMarketSql(stocktype)
        
        results = dboper.queryData(codelist_sql)
        
        if results is not None and len(results) > 0:
            
            for code in results: 
                
                LoggerFactory.debug("InitJJTemp", "The stock %s DOES NOT exist in the rtstocks, will insert stock information!" % code[0])
                
                threading.Thread(target=InsertJJTemp, args=(dboper, code[0], mytime)).start()    
                
                time.sleep(0.07)
            
            LoggerFactory.info("InitJJTemp", "The tble JJTemp has completed initialization...")
            
        else: 
            
            LoggerFactory.error("InitJJTemp", "There is no stock list retrieved...")
    
    else: 
        
        LoggerFactory.info("InitJJTemp", "Init JJTemp table failed!!")


def HandleJJTemp(dboper, stocktype):
    
    codelist_sql = GetMarketSql(stocktype)
    
    results = dboper.queryData(codelist_sql) 
  
    if results is not None and len(results) > 0:
        
        mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
        
        for code in results: 
            
            LoggerFactory.debug("HandleJJTemp", "Updating the stock: %s" % code[0])
            
            threading.Thread(target=UpdateJJTemp, args=(dboper, code[0], mytime)).start()
            time.sleep(0.07)
        
        LoggerFactory.info("HandleJJTemp", "Updating the table JJTemp has completed....")
                   
    else: 
        
        LoggerFactory.info("HandleJJTemp", "There is no stock need to be updated in the pool... ")


def checkExist(codename, codelist):            
    
    if codename in codelist:
         
        return True
    else: 
        return False
    
           
if "__name__ == __main__(input)":
    
#     input = raw_input()


    input = sys.argv[1]
#     input = 'sz'
         
    if input is None or input not in('sh', 'sz'):
         
        print "Input marketing type 'sh' or 'sz'"
         
    else:
        
        circulated = 1800000
        
        dboper = DBOperation.DBOperation()
        
        counter20 = 0
        
        counter25 = 0 
        
#         InitJJTemp(dboper,logger, input, circulated)
#         HandleJJTemp(dboper,logger, input)
#         HandleJJStock(dboper,logger, input, circulated)
         
#         while True:
        
#         InitJJTemp(dboper, input, circulated)
#         HandleJJTemp(dboper, input)
       
        while True:
                 
            mytime = int(time.strftime("%H%M%S"))
                 
            if (92030 <= mytime < 92435):
                     
                if counter20 < 1: 
                         
                    InitJJTemp(dboper, input, circulated)
                    counter20 = counter20 + 1
                
            elif (92435 <= mytime < 92500):
     
                    HandleJJTemp(dboper, input)
     
            elif (92500 <= mytime < 93000):
                    
                if counter25 < 1:
                    HandleJJStock(dboper, input, circulated)
                    counter25 = counter25 + 1
                    
#             elif (93000 <= mytime <= 114000) or (130000 <= mytime <= 180600):
#                       
#                 LoggerFactory.info("UpdateRTStocks", "Starting to update RTStocks table...") 
#                 HandleRTStock(dboper, input, circulated)
#                          
#                 time.sleep(1)
                  
            elif(mytime < 90000 or mytime > 93030):
                
                LoggerFactory.info("UpdateRTStocks", "Out of trade time...exit!")
                         
                break
                   
            else: 
                
                LoggerFactory.info("UpdateRTStocks", "It's not in trade time yet, waiting for market to open!!")
                time.sleep(5)
              
    
