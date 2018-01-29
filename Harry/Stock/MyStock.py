# -*    - coding=UTF-8 -*-

'''
Created on 20180129

@author: HarryTu
'''

import time
import DBOperation
import LoggerFactory
import DBDataHandle


def SelectMyStock( dboper, logger, circulatedMin=70000,circulatedMax=600000, changerate=2, iorate=1.4, amountp=1000 ):
    
    select_sql = "select a.code,a.name,b.cashin,b.cashout,b.netvalue,b.iorate,b.turnover,b.price,b.changeratio,b.amountp,b.amountn from stocks a, rtstocks b \
            where a.code=b.code and b.iorate>=%0.2f and b.amountp>=%0.2f and b.changeratio > %0.2f and( circulated >= %0.2f and circulated <= %0.2f)" \
            %(iorate,amountp,changerate,circulatedMin,circulatedMax)
    
    check_sql="select code from mystocks"
    
    stockData ={}
    codelist = []
    
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    
    checkData = dboper.queryData( check_sql )
    
    if checkData is not None:
        
        for data in checkData:
             
            codelist.append(data[0])
    
    selectedData = dboper.queryData( select_sql )
    
    if selectedData is not None and len(selectedData) > 1:
        
        for data in selectedData:
            
            if checkExist( data[0], codelist ):
        
                stockData['code']=data[0]
                stockData['name']=data[1]
                stockData['cashin']=data[2]
                stockData['cashout']=data[3]
                stockData['netvalue']=data[4]  
                stockData['iorate']=data[5]
                stockData['turnover']=data[6]
                stockData['price']=data[7]
                stockData['changeratio']=data[8]
                stockData['amountp']=data[9]
                stockData['amountn']=data[10]
                
                logger.info("更新股票信息: %s" %stockData['name'])
                
                DBDataHandle.UpdateMyStock(stockData, logger, mytime)
                
                
            else:
                
                stockData['code']=data[0]
                stockData['name']=data[1]
                stockData['cashin']=data[2]
                stockData['cashout']=data[3]
                stockData['initnetvalue']=data[4]
                stockData['iorate']=data[5]
                stockData['turnover']=data[6]
                stockData['price']=data[7]
                stockData['initchangeratio']=data[8]
                stockData['amountp']=data[9]
                stockData['amountn']=data[10]
            
                logger.info("插入新选出股票: %s" %stockData['name'])
                
#                 insert_sql = "insert into stocks(code, name, cashin, cashout, initnetvalue, iorate, turnover, price, initchangeratio, amountp, amountn)\
#                              values('%s', '%s', '%0.2f', '%0.2f', %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %s )" \
#                     %(stockData['code'], stockData['name'], stockData['cashin'], stockData['cashout'], stockData['initnetvalue'], \
#                       stockData['iorate'], stockData['turnover'], stockData['price'], stockData['initchangeratio'], stockData['amountp'], stockData['amountn'], mytime )  
                
                DBDataHandle.InsertMyStock(stockData, logger, mytime)
    
    else: 
        
        logger.info("没有发现符合规则的股票!!!")           
                
                
                
def checkExist(codename, codelist):            
    
    if codename in codelist:
         
        return True
    else: 
        return False   
    

if __name__ == '__main__':
    
    dboper = DBOperation.DBOperation()
    logger = LoggerFactory.getLogger("SelectMyStock")
    
    SelectMyStock(dboper, logger)
    
    