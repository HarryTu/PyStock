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


def HandleRTStock( stocktype, circulated=450000 ):

    logger = LoggerFactory.getLogger("HandleRTStock")
    dboper = DBOperation.DBOperation()

#     circulated = 450000  #查找流通市值45亿以下股票 
    
    rtstockslist = []
    codealiaslist = []
    codelist_sql = ""
    sql ="select code from rtstocks"
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    
    rtstocks = dboper.queryData(sql)
    
    if len(rtstocks) == 0:
        DBDataHandle.InitRTStocks(circulated, dboper, logger)
        
    
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
            
                if checkExist(code[0][2:8], rtstockslist):
                    
                    logger.info("RT表已有股票:%s 信息,将做更新..."%code[0])
                    
                    realtimeData = StockDataByTX.CollectRealTimeData(code[0], logger) 
                  
                    if realtimeData is not None: 
                    
                        logger.info("正在处理: %s" % realtimeData['code'])
                        
                        DBDataHandle.UpdateRTData(realtimeData, logger, mytime)
                    
                    else: 
                        
                        logger.error("股票: %s, 数据获取失败!!!"%code[0])
                    
                else:
                    
                    logger.info("RT表无股票:%s 信息,将插入新值..."%code[0])
                    
                    realtimeData = StockDataByTX.CollectRealTimeData(code[0], logger) 
                  
                    if realtimeData is not None: 
                    
                        logger.info("正在处理: %s" % realtimeData['code'])
                        
                        DBDataHandle.InsertRTData(realtimeData, logger, mytime)
                    
                    else: 
                        
                        logger.error("股票: %s, 数据获取失败!!!"%code[0])
                        


def checkExist(codename, codelist):            
    
    if codename in codelist:
         
        return True
    else: 
        return False
    
           
if "__name__ == __main__(input)":
    
#     input = raw_input()

    input = sys.argv[1]
        
    if input is None or input not in('sh','sz'):
        
        print "输入股票市场号码:'sh' 或者 'sz'"
        
    else:
        
        HandleRTStock(input)
        
        
             
    