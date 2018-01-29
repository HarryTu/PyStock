# -*- coding=UTF-8 -*-

'''
Created on 20180127

@author: Harry
'''

import time
import DBOperation
import LoggerFactory
import StockDataByTX




def InsertHisData( stockdata, logger ):
        
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')"
                    
    sql = "insert into hisstocks(code, cashin, cashout, netvalue, iorate, turnover, price, changeratio, amountp, acountn, mtime)  values('%s', %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %s )" \
            %(stockdata['code'], stockdata['cashin'], stockdata['cashout'], stockdata['netvalue'], stockdata['iorate'], stockdata['turnover'], stockdata['price'], stockdata['changeratio'], stockdata['amountp'],stockdata['amountn'], mytime) 

    
    logger.debug( sql )
    
    dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)



def InsertRTData( stockdata, logger, mytime ):
                    
    sql = "insert into rtstocks(code, cashin, cashout, netvalue, iorate, turnover, price, changeratio, amountp, amountn, mtime)  values('%s', %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %s )" \
            %(stockdata['code'], stockdata['cashin'], stockdata['cashout'], stockdata['netvalue'], stockdata['iorate'], stockdata['turnover'], stockdata['price'], stockdata['changeratio'], stockdata['amountp'],stockdata['amountn'], mytime) 

    
    logger.debug( sql )
    
    dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)
 

def UpdateRTData( stockdata, logger, mytime ):
                    
    sql = "update rtstocks set cashin=%0.2f, cashout=%0.2f, netvalue=%0.2f, iorate=%0.2f, turnover=%0.2f, price=%0.2f, changeratio=%0.2f, amountp=%0.2f, amountn=%0.2f, mtime=%s where code='%s'" \
            %(stockdata['cashin'], stockdata['cashout'], stockdata['netvalue'], stockdata['iorate'], stockdata['turnover'], stockdata['price'], stockdata['changeratio'], stockdata['amountp'],stockdata['amountn'], mytime, stockdata['code']) 

    
    logger.debug( sql )
    
    dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)



def InitRTStocks( circulated, dboper, logger ):
    
    sql = "select codealias from stocks where status=1 and circulated<= %0.2f" % circulated
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    
    codelist = dboper.queryData(sql)
    
    if codelist is not None and len(codelist) > 0:
            
            logger.info("初始化RTStock表...总有 %s只股票需要处理!!"%len(codelist))
            
            for code in codelist:
                 
                realtimeData = StockDataByTX.CollectRealTimeData(code[0], logger) 
                  
                if realtimeData is not None: 
                    
                    logger.info("正在处理: %s" % realtimeData['code'])
                    
                    InsertRTData(realtimeData, logger, mytime)
                      
                else: 
                      
                    logger.error("股票: %s 的相关信息获取失败..." % code)
    #
            logger.info("初始化RTStock表完成!")
    else: 
            
        logger.error("股票代码列表信息获取失败.....")
    
    


def GetStockCode():
    
    sql = "select codealias from stocks where status=1"
    
    dboper = DBOperation.DBOperation()
    
    results = dboper.queryData(sql)
    
    return results
    
    
    
    
if __name__=='__main__':

    circulated = 450000
    dboper = DBOperation.DBOperation()
    logger = LoggerFactory.getLogger("InitRTStocks")
    
    InitRTStocks(circulated,dboper,logger)
