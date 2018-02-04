# -*    - coding=UTF-8 -*-

'''
Created on 20180129

@author: HarryTu
'''

import time
import datetime
import DBOperation
import LoggerFactory
import DBDataHandle


# def SelectJJStock( dboper, logger):
#     
#     mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')"
#     
#     sql_rtstock = "select code from rtstocks where mtime >= %s" % mytime
#     check_sql="select code from mystocks where mtype=0"
# 
#     selectData = dboper.queryData(sql_rtstock)
#     checkData = dboper.queryData( check_sql )
#    
#     stockData ={}
#     codelist = []
#     
#     if checkData is not None:
#         
#         for data in checkData:
#              
#             codelist.append(data[0])
#     
#     for code in selectData:
#         
#         if checkExist( code[0], codelist ):
#             
#             logger.info("%s This stock already exists in the table mystocks..." % data[0])
#             
#         else:
#         
#             sql_mystock = "select a.code, a.name, b.cashin, b.cashout, b.netvalue, b.iorate, b.price, b.turnover, b.changeratio, b.amountp, b.amountn, a.codealias \
#                             from stocks a, rtstocks b where a.code=b.code and b.code='%s'" % code  
#             
#             sql_jjstock = "select cashin, cashout, netvalue, price from rtjjstocks \
#                             where code='%s'" % code  
#             
#             mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
#             
#             stockData = {}
#             jjstockData = {}
#         
#             logger.debug( sql_mystock )
#             logger.debug( sql_jjstock )
#             
#             rtData = dboper.queryOneData( sql_mystock )
#             jjData = dboper.queryOneData( sql_jjstock )
#             
#             if rtData is not None and jjData is not None:
#                 
#                 stockData['code']= rtData[0]
#                 stockData['name'] = rtData[1]
#                 stockData['cashin'] = rtData[2]
#                 stockData['cashout'] = rtData[3]
#                 stockData['initnetvalue'] = rtData[4]
#                 stockData['netvalue'] = rtData[4]
#                 stockData['iorate'] = rtData[5]
#                 stockData['price'] = rtData[6]
#                 stockData['turnover'] = rtData[7]
#                 stockData['initchangeratio'] = rtData[8]
#                 stockData['changeratio'] = rtData[8]
#                 stockData['amountp'] = rtData[9]
#                 stockData['amountn'] = rtData[10]
#                 stockData['codealias'] = rtData[11]
#                 stockData['mtype'] = 0
#           
#                 jjData = dboper.queryOneData( sql_jjstock )
#                 jjstockData['price'] = jjData[3]
#               
#               
#                 if (stockData['price'] - jjstockData['price']) > 0:
#                     
#                     logger.info("Inserting a new Stock %s during bidding..." % stockData['code'])
#                     DBDataHandle.InsertMyStock(dboper, stockData, logger, mytime)


def SelectJJStock_New( dboper, logger):
    
    mytimequery = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')"
    
    sql_rtstock = "select code from rtstocks where mtime >= %s" % mytimequery
    
    check_sql="select code from mystocks where mtype=0"

    selectData = dboper.queryData(sql_rtstock)
    checkData = dboper.queryData( check_sql )
   
    hisdaytime = "str_to_date('%s'," % (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d') + "'%Y-%m-%d')"
    
    stockData ={}
    codelist = []
    
    if checkData is not None:
        
        for data in checkData:
             
            codelist.append(data[0])
    
    if selectData is not None and len(selectData)>0:
        
        for code in selectData:
            
            if checkExist( code[0], codelist ):
                
                logger.info("%s This stock already exists in the table mystocks..." % data[0])
                
            else:
            
                sql_mystock = "select a.code, a.name, b.cashin, b.cashout, b.netvalue, b.iorate, b.price, b.turnover, b.changeratio, b.amountp, b.amountn, a.codealias \
                                from stocks a, rtstocks b where a.code=b.code and b.code='%s'" % code[0]  
                
                sql_hisstock = "select cashin, cashout, netvalue, price, turnover from hisstocks \
                                where code='%s' and mtime=%s" %(code[0], hisdaytime)  
                
                mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
                
                stockData = {}
                stockHisData = {}
            
                logger.debug( sql_mystock )
                logger.debug( sql_hisstock )
                
                rtData = dboper.queryOneData( sql_mystock )
                hisData = dboper.queryOneData( sql_hisstock )
                
                if rtData is not None and hisData is not None:
                    
                    stockData['code']= rtData[0]
                    stockData['name'] = rtData[1]
                    stockData['cashin'] = rtData[2]
                    stockData['cashout'] = rtData[3]
                    stockData['initnetvalue'] = rtData[4]
                    stockData['netvalue'] = rtData[4]
                    stockData['iorate'] = rtData[5]
                    stockData['price'] = rtData[6]
                    stockData['turnover'] = rtData[7]
                    stockData['initchangeratio'] = rtData[8]
                    stockData['changeratio'] = rtData[8]
                    stockData['amountp'] = rtData[9]
                    stockData['amountn'] = rtData[10]
                    stockData['codealias'] = rtData[11]
                    stockData['mtype'] = 0
              
                    stockHisData['price'] = hisData[3]
                    stockHisData['price'] = hisData[2]
                  
                  
                    if stockData['turnover']>2 and stockData['cashin']>=50 and stockData['netvalue']>=50:
                        
                        logger.info("Inserting a new Stock %s during bidding..." % stockData['code'])
                        DBDataHandle.InsertMyStock(dboper, stockData, logger, mytime)

    else:
        
        logger.error("There is no data selected from rtstocks") 
            
            
            
def SelectMyStock( dboper, logger, circulatedMin=70000,circulatedMax=600000, changerate=2, iorate=1.4, amountp=1000, netvaluemin=1000 ):
    
    mytimeqeury = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')"
    
    select_sql = "select a.code,a.name,b.cashin,b.cashout,b.netvalue,b.iorate,b.turnover,b.price,b.changeratio,b.amountp,b.amountn, a.codealias from stocks a, rtstocks b \
            where a.code=b.code and b.iorate>=%0.2f and b.amountp>=%0.2f and b.changeratio > %0.2f and( circulated >= %0.2f and circulated <= %0.2f) and b.netvalue >= %0.2f and b.mtime >=%s" \
            %(iorate,amountp,changerate,circulatedMin,circulatedMax,netvaluemin,mytimeqeury)
    
    check_sql="select code from mystocks where mtype=1"
    
    stockData ={}
    codelist = []
    
    
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    
    checkData = dboper.queryData( check_sql )
    
    if checkData is not None:
        
        for data in checkData:
             
            codelist.append(data[0])
    
    selectedData = dboper.queryData( select_sql )
    
    if selectedData is not None and len(selectedData) > 0:
        
        for data in selectedData:
            
            if checkExist( data[0], codelist ):
                
                logger.info("The stock %s already exists in the table mystocks..." % data[0])
#                 stockData['code']=data[0]
#                 stockData['name']=data[1]
#                 stockData['cashin']=data[2]
#                 stockData['cashout']=data[3]
#                 stockData['netvalue']=data[4]  
#                 stockData['iorate']=data[5]
#                 stockData['turnover']=data[6]
#                 stockData['price']=data[7]
#                 stockData['changeratio']=data[8]
#                 stockData['amountp']=data[9]
#                 stockData['amountn']=data[10]
#                 
#                 logger.info("更新股票信息: %s" %stockData['name'])
#                 
#                 DBDataHandle.UpdateMyStock(stockData, logger, mytime)
                
                
            else:
                
                stockData['code']=data[0]
                stockData['name']=data[1]
                stockData['cashin']=data[2]
                stockData['cashout']=data[3]
                stockData['initnetvalue']=data[4]
                stockData['netvalue']=data[4]
                stockData['iorate']=data[5]
                stockData['turnover']=data[6]
                stockData['price']=data[7]
                stockData['initchangeratio']=data[8]
                stockData['changeratio']=data[8]
                stockData['amountp']=data[9]
                stockData['amountn']=data[10]
                stockData['codealias']=data[11]
                stockData['mtype']=1
            
                logger.info("Insert a new selected Stock: %s into the pool!" %stockData['name'])
                
#                 insert_sql = "insert into stocks(code, name, cashin, cashout, initnetvalue, iorate, turnover, price, initchangeratio, amountp, amountn)\
#                              values('%s', '%s', '%0.2f', '%0.2f', %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %s )" \
#                     %(stockData['code'], stockData['name'], stockData['cashin'], stockData['cashout'], stockData['initnetvalue'], \
#                       stockData['iorate'], stockData['turnover'], stockData['price'], stockData['initchangeratio'], stockData['amountp'], stockData['amountn'], mytime )  
                
                DBDataHandle.InsertMyStock(dboper, stockData, logger, mytime)
    
    else: 
        
        logger.info("There is no qualified Stock detected at this moment!")           
                
                
                
def checkExist(codename, codelist):            
    
    if codename in codelist:
         
        return True
    else: 
        return False   
    

if __name__ == '__main__':
    
    dboper = DBOperation.DBOperation()
    logger = LoggerFactory.getLogger("SelectMyStock")

#     SelectJJStock_New(dboper, logger)
#     SelectMyStock(dboper, logger)

    while True:
             
        mytime = int(time.strftime("%H%M%S"))
            
        if ( 92000 <= mytime < 92600 ):
              
            SelectJJStock_New(dboper, logger)
                 
            time.sleep(2)
          
        elif ( 93000 <= mytime <= 113030 ) or ( 130000 <= mytime <= 150030 ):
                 
            SelectMyStock(dboper, logger)
                 
            time.sleep(2)
          
        elif( mytime < 90000 or mytime > 150100):
                  
#                 logger.info("不在交易时间...退出程序!")
            logger.info("Out of trade time now...exit!")
                 
            break
           
        else: 
                 
#                 logger.info("休息时间。。。")
            logger.info("It's not in trade time yet, waiting for market to open!!")
            time.sleep(30)
    
    