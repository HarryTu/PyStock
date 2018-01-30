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



def UpdateMyStock( stockData, logger, mytime ):
                    
    sql = "update mystocks set cashin=%0.2f, cashout=%0.2f, netvalue=%0.2f, iorate=%0.2f, turnover=%0.2f, price=%0.2f, changeratio=%0.2f, amountp=%0.2f, amountn=%0.2f, mtime=%s where code='%s'" \
                %(stockData['cashin'], stockData['cashout'], stockData['netvalue'], stockData['iorate'], stockData['turnover'], stockData['price'], stockData['changeratio'], stockData['amountp'],stockData['amountn'], mytime, stockData['code']) 

    
    logger.debug( sql )
    
    dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)
    


def InsertMyStock( stockData, logger, mytime ):
                    
    sql = "insert into mystocks(code, name, cashin, cashout, initnetvalue, iorate, turnover, price, initchangeratio, amountp, amountn, inittime, codealias)\
                 values('%s', '%s', '%0.2f', '%0.2f', %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %s, '%s' )" \
        %(stockData['code'], stockData['name'], stockData['cashin'], stockData['cashout'], stockData['initnetvalue'], \
          stockData['iorate'], stockData['turnover'], stockData['price'], stockData['initchangeratio'], stockData['amountp'], stockData['amountn'], mytime, stockData['codealias'] )  
                
    
    logger.debug( sql )
    
    dboper = DBOperation.DBOperation()
    
    dboper.sqlExecute(sql)


def GetStockCode():
    
    sql = "select codealias from stocks where status=1"
    
    dboper = DBOperation.DBOperation()
    
    results = dboper.queryData(sql)
    
    return results
    
    
    
    
if __name__=='__main__':

    circulated = 450000
    dboper = DBOperation.DBOperation()
    logger = LoggerFactory.getLogger("InitRTStocks")
    
#     InitRTStocks(circulated,dboper,logger)
