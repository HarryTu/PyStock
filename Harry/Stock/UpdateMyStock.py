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
import threading


def UpdateMyStock(dboper):
    
#     codelist = []
    realtimeData = {}
    
    sql = "select codealias from mystocks"
    
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    
    results = dboper.queryData(sql)
    
    if results is not None and len(results) > 0:
        
        LoggerFactory.info("UpdateMyStock", "Starting to update stocks in the pool...")
#         logger.info("Starting to update stocks in the pool...")
        
        for code in results: 
             
            stockBasicData = StockDataByTX.GetStockBasicData(code[0])
            stockCashData = StockDataByTX.GetStockCashData(code[0])
            stockBriefData = StockDataByTX.GetStockBriefData(code[0])
            
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
                        realtimeData['qrratio'] = stockBasicData['qrratio']
                        realtimeData['turnover'] = stockBasicData['turnover_rate']
                        realtimeData['changeratio'] = stockBriefData['changeratio']
                        realtimeData['amountp'] = stockBriefData['amountp']
                        realtimeData['amountn'] = stockBriefData['amountn']
                        
                        LoggerFactory.info("UpdateMyStock", "Starting to update stock: %s" %stockBasicData['name'])
                        
                        DBDataHandle.UpdateMyStock(dboper, realtimeData, mytime)
                    
                    else:
                        
                        LoggerFactory.error("UpdateMyStock", "Data collection stockBriefData is Null. code: %s"%code[0])   
                
                else:
                    
                    LoggerFactory.error("UpdateMyStock", "Data collection stockCashData is Null. code: %s"%code[0])
                    
            else: 
                
                LoggerFactory.error("UpdateMyStock", "Data collection stockBasicData is Null. code: %s"%code[0])
    else: 
        
        LoggerFactory.info("UpdateMyStock", "There is no Stocks in the pool yet....Waiting for auto select!")  


if __name__=="__main__":
    
    dboper = DBOperation.DBOperation()        

    UpdateMyStock(dboper)
#     while True:
#          
#         mytime = int(time.strftime("%H%M%S"))      
#        
#         if( 92000 <= mytime <= 113030 ) or ( 130000 <= mytime <= 150030 ):
#             
#             threading.Thread(target = UpdateMyStock, args=(dboper, logger)).start()
#             time.sleep(0.5)
# #             UpdateMyStock(dboper, logger)
#        
#         elif( mytime < 90000 or mytime > 150100):
#                
# #                 logger.info("不在交易时间...退出程序!")
#             logger.info("Out of trade time now...exit!")
#               
#             break
#         
#         else: 
#               
# #                 logger.info("休息时间。。。")
#             logger.info("It's not in trade time yet, waiting for market to open!!")
#             time.sleep(30)
        
