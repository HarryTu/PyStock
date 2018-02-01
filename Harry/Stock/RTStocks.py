# -*- coding=UTF-8 -*-

'''
Created on 20180128

@author: Harry
'''


import DBOperation
import LoggerFactory
import DBDataHandle
import StockDataByTX
import time
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
        
        if stocktype == "sz":
            
            logger.info("将更新深市股票信息.....")
            codelist_sql="select codealias from stocks where codealias like '%s' and status=1 and circulated<= %0.2f" % ("sz%", circulated )
        
        if stocktype == "sh":
            
            logger.info("将更新沪市股票信息.....")
            codelist_sql="select codealias from stocks where codealias like '%s' and status=1 and circulated<= %0.2f" % ("sh%", circulated )
            
            
        results = dboper.queryData( codelist_sql ) 
                  
        if results is not None and len(results) > 0:
            
            for code in results:
            
                if checkExist( code[0][2:8], rtstockslist ):
                    
                    logger.info("RT表已有股票:%s 信息,将做更新..."%code[0])
                    
                    threading.Thread(target = UpdateRT, args=(dboper, code[0], logger, mytime)).start()
                    time.sleep(0.2)
#                     realtimeData = StockDataByTX.CollectRealTimeData(code[0], logger) 
#                    
#                     if realtimeData is not None: 
#                      
#                         logger.info("正在处理: %s" % realtimeData['code'])
#                          
#                         DBDataHandle.UpdateRTData(realtimeData, logger, mytime)
#                      
#                     else: 
#                          
#                         logger.error("股票: %s, 数据获取失败!!!"%code[0])
                    
                else:
                    
                    logger.info("RT表无股票:%s 信息,将插入新值..."%code[0])
                    
#                     InsertRT( code[0], logger )
                    
                    realtimeData = StockDataByTX.CollectRealTimeData(code[0], logger) 
                   
                    if realtimeData is not None: 
                     
                        logger.info("正在处理: %s" % realtimeData['code'])
                         
                        DBDataHandle.InsertRTData(dboper, realtimeData, logger, mytime)
                     
                    else: 
                         
                        logger.error("股票: %s, 数据获取失败!!!"%code[0])
                        


def UpdateRT(dboper, code, logger, mytime):
    
    realtimeData = StockDataByTX.CollectRealTimeData(code, logger) 
  
    if realtimeData is not None: 
    
        logger.info("正在处理: %s" % realtimeData['code'])
        
        DBDataHandle.UpdateRTData(dboper, realtimeData, logger, mytime)
        
        
        
def InsertRT(dboper, code, logger):


    realtimeData = StockDataByTX.CollectRealTimeData(code, logger) 
                  
    if realtimeData is not None: 
    
        logger.info("正在处理: %s" % realtimeData['code'])
        
        DBDataHandle.InsertRTData(dboper, realtimeData, logger, mytime)
    
    else: 
        
        logger.error("股票: %s, 数据获取失败!!!"%code)
            


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
         
        print "输入股票市场号码:'sh' 或者 'sz'"
         
    else:
        
        logger = LoggerFactory.getLogger("HandleRTStock")
        
        circulated = 1800000
        
        while True:
        
            mytime = int(time.strftime("%H%M%S"))
           
            if ( 93000 < mytime < 113000 ) or ( 130000 < mytime < 150030 ):
                
                HandleRTStock(logger, input, circulated)
                
                time.sleep(1)
         
            elif( mytime < 93000 or mytime > 150100):
                 
#                 logger.info("不在交易时间...退出程序!")
                logger.info("Out of trade time...exit!")
                
                break
          
            else: 
                
#                 logger.info("休息时间。。。")
                logger.info("In the rest time....waiting for trade market reopen afternoon")
                time.sleep(60)
        
             
    