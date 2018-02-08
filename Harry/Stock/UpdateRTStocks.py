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


def HandleRTStock( logger, stocktype, circulated=1800000 ):

    dboper = DBOperation.DBOperation()

#     circulated = 450000  #查找流通市值45亿以下股票 
    
    rtstockslist = []
    
    codelist_sql = ""
    sql ="select code from rtstocks"
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    
    rtstocks = dboper.queryData(sql)
    
    if len(rtstocks) == 0:
        InitTable.InitRTStocks(circulated, dboper, logger)
        
    
    if len(rtstocks) > 0:
        
        for code in rtstocks: 
            rtstockslist.append(code[0])
        
        if stocktype == "sh":
            
            logger.info("Updating stock information in SH marketing.....")
            codelist_sql="select codealias from stocks where codealias like '%s' and status=1 and circulated<= %0.2f" % ("sh%", circulated )
        
        if stocktype == "sz":
            
            logger.info("Updating stock information in SZ marketing.....")
            codelist_sql="select codealias from stocks where codealias like '%s' and status=1 and circulated<= %0.2f" % ("sz%", circulated )
   
        results = dboper.queryData( codelist_sql ) 
      
        if results is not None and len(results) > 0:
            
            logger.info("Starting to update rtstocks....")
            
            begintime = datetime.datetime.now()
            
            for code in results:
            
                if checkExist( code[0][2:8], rtstockslist ):
                    
                    logger.debug("The stock %s already exists in the rtstocks, will perform update information"%code[0])
                    
                    threading.Thread(target = UpdateRT, args=(dboper, code[0], logger, mytime)).start()
                    time.sleep(0.07)
                    
                else:
                    
                    logger.debug("The stock %s DOES NOT exist in the rtstocks, will insert stock information!"%code[0])
#                     InsertRT(dboper, code[0], logger, mytime)
                    threading.Thread(target = InsertRT, args=(dboper, code[0], logger, mytime)).start()    
                    time.sleep(0.1)
             
            endtime = datetime.datetime.now()
            
            logger.info("rtstocks has been updated. Spent time: %s"% str((endtime-begintime).seconds))
#             print (endtime-begintime).seconds     
        

def UpdateRT(dboper, code, logger, mytime):
    
    realtimeData = StockDataByTX.CollectRealTimeData(code, logger) 
  
    if realtimeData is not None: 
    
        logger.debug("Updating the stock %s" % realtimeData['code'])
        
        DBDataHandle.UpdateRTData(dboper, realtimeData, logger, mytime)
        
        
        
def InsertRT(dboper, code, logger, mytime):


    realtimeData = StockDataByTX.CollectRealTimeData(code, logger) 
                  
    if realtimeData is not None: 
    
        logger.info("Insert the stock %s to rtstocks" % realtimeData['code'])
        
        DBDataHandle.InsertRTData(dboper, realtimeData, logger, mytime)
    
    else: 
        
        logger.error("Fetching the stock information failed. code: %s ..."%code)
            


def checkExist(codename, codelist):            
    
    if codename in codelist:
         
        return True
    else: 
        return False
    
           
if "__name__ == __main__(input)":
    
#     input = raw_input()

#     input = sys.argv[1]
    input = 'sz'
         
    if input is None or input not in('sh','sz'):
         
        print "Input marketing type 'sh' or 'sz'"
         
    else:
        
        logger = LoggerFactory.getLogger("HandleRTStock")
        
        circulated = 1800000
        
#         while True:
        HandleRTStock(logger, input, circulated)
         
#         while True:
#            
#             mytime = int(time.strftime("%H%M%S"))
#               
#             if ( 92010 <= mytime <= 113200 ) or ( 130000 <= mytime <= 150200 ):
#                    
#                 HandleRTStock(logger, input, circulated)
#                    
#                 time.sleep(1)
#             
#             elif( mytime < 90000 or mytime > 150200):
#                     
# #                 logger.info("不在交易时间...退出程序!")
#                 logger.info("Out of trade time...exit!")
#                    
#                 break
#              
#             else: 
#                    
# #                 logger.info("休息时间。。。")
#                 logger.info("It's not in trade time yet, waiting for market to open!!")
#                 time.sleep(30)
        
             
    