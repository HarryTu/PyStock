# -*- coding=UTF-8 -*-

'''
Created on 20180130

@author: HarryTu
'''

import DBOperation
import StockDataByTX
import LoggerFactory
import time
import DBDataHandle


def UpdateMyStock(dboper, logger):
    
#     codelist = []
    realtimeData = {}
    
    sql = "select codealias from mystocks"
    
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    
    results = dboper.queryData(sql)
    
    if results is not None and len(results) > 0:
        
        logger.info("开始更新股票池中股票信息...")
        
        for code in results: 
             
            stockBasicData = StockDataByTX.GetStockBasicData(code[0], logger)
            stockCashData = StockDataByTX.GetStockCashData(code[0], logger)
            stockBriefData = StockDataByTX.GetStockBriefData(code[0], logger)
            
            if stockBasicData is not None: 
                if stockCashData is not None: 
                    if stockBriefData is not None:
                        
                        if float(stockCashData['main_out_cash']) > 0:
                            
                            rate = round((float(stockCashData['main_in_cash']) / float(stockCashData['main_out_cash'])), 2)
                            
                        else:
                            
                            rate = round((float(stockCashData['main_in_cash']) / 1), 2)
            
                        realtimeData['code'] = code[0][2:8]
                        realtimeData['price'] = stockBriefData['price']
                        realtimeData['cashin'] = stockCashData['main_in_cash']
                        realtimeData['cashout'] = stockCashData['main_out_cash']
                        realtimeData['netvalue'] = stockCashData['netvalue']
                        realtimeData['iorate'] = float(rate)
                        realtimeData['turnover'] = stockBasicData['turnover_rate']
                        realtimeData['changeratio'] = stockBriefData['changeratio']
                        realtimeData['amountp'] = stockBriefData['amountp']
                        realtimeData['amountn'] = stockBriefData['amountn']
                        
                        logger.info("开始更新股票: %s" %stockBasicData['name'])
                        DBDataHandle.UpdateMyStock(dboper, realtimeData, logger, mytime)
                    
                    else:
                        
                        logger.error("Data collection stockBriefData is Null....")   
                
                else:
                    
                    logger.error("Data collection stockCashData is Null....")
                    
            else: 
                
                logger.error("Data collection stockBasicData is Null....")
    else: 
        
        logger.info("股票池中没有股票信息....")   


if __name__=="__main__":
    
    dboper = DBOperation.DBOperation()
    logger = LoggerFactory.getLogger("MyStockUpdate")        
    
#     UpdateMyStock(dboper, logger)
    while True:
        
        mytime = int(time.strftime("%H%M%S"))
        
        if ( 93000 < mytime < 113000 ) or ( 130000 < mytime < 150030 ):
             
            UpdateMyStock(dboper, logger)
             
            time.sleep(1)
      
        elif( mytime < 93000 or mytime > 150100):
              
#                 logger.info("不在交易时间...退出程序!")
            logger.info("Out of trade time now...exit!")
             
            break
       
        else: 
             
#                 logger.info("休息时间。。。")
            logger.info("In the rest time....waiting for trade market reopen afternoon")
            time.sleep(60)
        
