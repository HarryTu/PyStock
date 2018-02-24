# -*- coding=UTF-8 -*-

'''
Created on 20180127

@author: Harry
'''

import time
import DBOperation
import LoggerFactory
import StockDataByTX




def InsertHisData( dboper, stockdata ):
        
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')"
                    
    sql = "insert into hisstocks(code, cashin, cashout, netvalue, iorate, turnover, qrratio, price, changeratio, amountp, amountn, mtime)  values('%s', %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %s )" \
            %(stockdata['code'], stockdata['cashin'], stockdata['cashout'], stockdata['netvalue'], stockdata['iorate'], stockdata['turnover'], stockdata['qrratio'], stockdata['price'], stockdata['changeratio'], stockdata['amountp'],stockdata['amountn'], mytime) 
    
    LoggerFactory.debug("InsertHisData", sql)
#     logger.debug( sql )
    
    dboper.sqlExecute(sql)



def InsertRTData( dboper, stockdata, mytime ):
                    
    sql = "insert into rtstocks(code, cashin, cashout, netvalue, iorate, turnover, qrratio, price, changeratio, amountp, amountn, mtime)  values('%s', %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %s )" \
            %(stockdata['code'], stockdata['cashin'], stockdata['cashout'], stockdata['netvalue'], stockdata['iorate'], stockdata['turnover'], stockdata['qrratio'], stockdata['price'], stockdata['changeratio'], stockdata['amountp'],stockdata['amountn'], mytime) 

    
    LoggerFactory.debug("InsertRTData", sql)
#     logger.debug( sql )
    
#     dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)


def InsertJJStock( dboper, stockdata, logger, mytime ):
                    
    sql = "insert into jjstocks(code, cashin, cashout, netvalue, qrratio, turnover, price, changeratio, amountp, amountn, mtime)  values('%s', %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %s )" \
            %(stockdata['code'], stockdata['cashin'], stockdata['cashout'], stockdata['netvalue'], stockdata['qrratio'], stockdata['turnover'], stockdata['price'], stockdata['changeratio'], stockdata['amountp'],stockdata['amountn'], mytime) 

    
    logger.debug( sql )
    
#     dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)


def InsertJJTemp( dboper, stockdata, logger, mytime ):
                    
    sql = "insert into jjtemp(code, codealias, initprice, price, initchangeratio, changeratio, mtime)  values('%s', '%s', %0.2f, %0.2f, %0.2f, %0.2f, %s)" \
            %(stockdata['code'], stockdata['codealias'], stockdata['price'], stockdata['price'], stockdata['changeratio'], stockdata['changeratio'], mytime) 

    
    logger.debug( sql )
    
#     dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)


def UpdateJJTemp( dboper, stockdata, logger, mytime ):
                    
    sql = "update jjtemp set price=%0.2f, changeratio=%0.2f, mtime=%s where code='%s'" \
            %(stockdata['price'], stockdata['changeratio'], mytime, stockdata['code']) 

    
    logger.debug( sql )
    
#     dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)


def UpdateRTData( dboper, stockdata, mytime ):
                    
    sql = "update rtstocks set cashin=%0.2f, cashout=%0.2f, netvalue=%0.2f, iorate=%0.2f, turnover=%0.2f, qrratio=%0.2f, price=%0.2f, changeratio=%0.2f, amountp=%0.2f, amountn=%0.2f, mtime=%s where code='%s'" \
            %(stockdata['cashin'], stockdata['cashout'], stockdata['netvalue'], stockdata['iorate'], stockdata['turnover'], stockdata['qrratio'], stockdata['price'], stockdata['changeratio'], stockdata['amountp'],stockdata['amountn'], mytime, stockdata['code']) 

    
    LoggerFactory.debug("UpdateRTData", sql)
#     logger.debug( sql )
    
#     dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)



def UpdateMyStock( dboper, stockData, mytime ):
                    
    sql = "update mystocks set cashin=%0.2f, cashout=%0.2f, netvalue=%0.2f, iorate=%0.2f, turnover=%0.2f, qrratio=%0.2f, price=%0.2f, changeratio=%0.2f, amountp=%0.2f, amountn=%0.2f, mtime=%s where code='%s'" \
                %(stockData['cashin'], stockData['cashout'], stockData['netvalue'], stockData['iorate'], stockData['turnover'], stockData['qrratio'], stockData['price'], stockData['changeratio'], stockData['amountp'],stockData['amountn'], mytime, stockData['code']) 

    
    LoggerFactory.debug("UpdateMyStock", sql)
    
#     dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)
    


def InsertMyStock( dboper, stockData, mytime ):
                    
#     print stockData['code']
#     print stockData['name']
#     print stockData['cashin']
#     print stockData['cashout']
#     print stockData['initnetvalue']
#     print stockData['netvalue']
#     print stockData['iorate']
#     print stockData['turnover']
#     print stockData['price']
#     print stockData['initchangeratio']
#     print stockData['changeratio']
#     print stockData['amountp']
#     print stockData['amountn']
#     print mytime
#     print stockData['codealias']
                    

    sql = "insert into mystocks(code, cashin, cashout, initnetvalue, netvalue, iorate, turnover, qrratio, initprice, price, pricerate, initchangeratio, changeratio, amountp, amountn, inittime, codealias, mtype)\
                 values('%s', %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.4f, %0.2f, %0.2f, %0.2f, %0.2f, %s, '%s', %d)" \
        %(stockData['code'], stockData['cashin'], stockData['cashout'], stockData['initnetvalue'], stockData['netvalue'], \
          stockData['iorate'], stockData['turnover'], stockData['qrratio'], stockData['initprice'], stockData['price'], stockData['pricerate'], stockData['initchangeratio'], stockData['changeratio'], stockData['amountp'], stockData['amountn'], mytime, stockData['codealias'], stockData['mtype'])  
                
    
    LoggerFactory.debug("InsertMyStock", sql)
#     logger.debug( sql )
    
#     dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)


def GetStockCode(dboper):
    
    sql = "select codealias from stocks where status=1"
    
#     dboper = DBOperation.DBOperation()
    
    results = dboper.queryData(sql)
    
    return results
    
    
    
    
if __name__=='__main__':

    circulated = 450000
    dboper = DBOperation.DBOperation()

    
#     InitRTStocks(circulated,dboper,logger)
