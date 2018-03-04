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
import code


def GetJJBasicData( dboper ):
            
    mytimequery = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')"
    
#     mytimequery = "str_to_date('2018-02-23', '%Y-%m-%d')"
      
    sql_jjData = "select a.code, a.codealias, a.name, a.industry, b.initprice, b.price, c.cashin, c.cashout, c.netvalue, c.turnover, c.changeratio, c.amountp, c.amountn \
                 from stocks a, jjtemp b, jjstocks c where a.code = b.code and b.code = c.code and b.mtime >=%s \
                 and c.mtime >=%s and b.price > b.initprice and b.initprice >0 " % (mytimequery, mytimequery)
      
    sql_mystock="select code from mystocks where mtype=0"
    
    
    LoggerFactory.debug("sql_jjData", sql_jjData)
    LoggerFactory.debug("sql_mystock", sql_mystock)
    
    jjDataCol = dboper.queryData(sql_jjData)
    myStockDataCol = dboper.queryData( sql_mystock )
      
    stockDataList =[]
    codelist = []
      
    if myStockDataCol is not None:
          
        for data in myStockDataCol:
               
            codelist.append(data[0])
      
    if jjDataCol is not None and len(jjDataCol)>0:
          
        for jjdata in jjDataCol: 
        
            if checkExist( jjdata[0], codelist ):
                
                LoggerFactory.debug("SelectJJStock_rule1", "%s This stock already exists in the table mystocks..." % data[0])
                  
            else:
                stockData ={}
                
                stockData['code'] = jjdata[0]
                stockData['codealias'] = jjdata[1]
                stockData['name'] = jjdata[2]
                stockData['industry'] = jjdata[3]
                stockData['initprice'] = jjdata[4]
                stockData['price'] = jjdata[5]
                stockData['cashin'] = jjdata[6]
                stockData['cashout'] = jjdata[7]
                stockData['netvalue'] = jjdata[8]
                stockData['turnover'] = jjdata[9]
                stockData['changeratio'] = jjdata[10]
                stockData['amountp'] = jjdata[11]
                stockData['amountn'] = jjdata[12]
                
                stockDataList.append(stockData) 
        
        return stockDataList
        
        
    else:
          
        LoggerFactory.error("SelectJJStock_rule1", "There is no data selected from rtstocks")
        
        return None
            
            
def SelectJJStock_rule1( dboper ):
          
    dataList = GetJJBasicData(dboper)
    
    stockData = {}
    
    if dataList is not None and len(dataList) > 0: 
        
        for data in dataList: 
          
            stockData['code'] = data['code']
            stockData['codealias'] = data['codealias']
            stockData['name'] = data['name']
            stockData['industry'] = data['industry']
            stockData['initprice'] = data['initprice']
            stockData['price'] = data['price']
            stockData['cashin'] = data['cashin']
            stockData['cashout'] = data['cashout']
            stockData['initnetvalue'] = data['netvalue']
            stockData['netvalue'] = data['netvalue']
            stockData['turnover'] = data['turnover']
            stockData['initchangeratio'] = data['changeratio']
            stockData['changeratio'] = data['changeratio']
            stockData['amountp'] = data['amountp']
            stockData['amountn'] = data['amountn']
            stockData['qrratio'] = 0
            stockData['mtype']= 0
            
            if stockData['cashout'] > 0 and stockData['cashin'] > 0:
                
                stockData['iorate'] = round( stockData['cashin'] / stockData['cashout'], 2 )
                
            else: 
                
                stockData['iorate'] = 0
        
        
                    
            if stockData['price'] > 0 and stockData['initprice'] > 0:
                
                stockData['pricerate'] = round( stockData['price'] / stockData['initprice'], 4 )
                
            else: 
                
                stockData['pricerate'] = 0
            
            
            if round(stockData['price'] / stockData['initprice'], 4) >= 1.005 \
                and stockData['amountp'] >= 200 and ( stockData['changeratio'] >= -3 and stockData['changeratio'] <= 5) \
                    and stockData['netvalue'] > 0: 
                
                mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
                
                DBDataHandle.InsertMyStock(dboper, stockData, mytime)
                
                LoggerFactory.info("SelectJJStock_rule1", "The stock %s is selected out" % stockData['code'])
            
               
            
            
def SelectMyStock( dboper, circulatedMin=70000,circulatedMax=1000000, changerate=1, iorate=1.4, amountp=3000, netvaluemin=1000 ):
    
    mytimeqeury = "str_to_date('%s'," % time.strftime('%Y-%m-%d') + "'%Y-%m-%d')"
    
    mytimeqeury = "str_to_date('2018-02-22', '%Y-%m-%d')"
    
    select_sql = "select a.code,a.name,b.cashin,b.cashout,b.netvalue,b.iorate,b.turnover,b.price,b.changeratio,b.amountp,b.amountn, a.codealias, b.qrratio from stocks a, rtstocks b \
            where a.code=b.code and b.iorate>=%0.2f and b.amountp>=%0.2f and b.changeratio > %0.2f and ( circulated >= %0.2f and circulated <= %0.2f) and b.netvalue >= %0.2f and b.mtime >=%s and b.turnover <= %0.2f" \
            %(iorate,amountp,changerate,circulatedMin,circulatedMax,netvaluemin,mytimeqeury,5)
    
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
                
                LoggerFactory.info("SelectMyStock", "The stock %s already exists in the table mystocks..." % data[0])
#                 logger.info("The stock %s already exists in the table mystocks..." % data[0])
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
                stockData['qrratio']=data[12]
                stockData['mtype']=1
                
                LoggerFactory.info("SelectMyStock", "Insert a new selected Stock: %s into the pool!" %stockData['name'])
#                 logger.info("Insert a new selected Stock: %s into the pool!" %stockData['name'])
                
#                 insert_sql = "insert into stocks(code, name, cashin, cashout, initnetvalue, iorate, turnover, price, initchangeratio, amountp, amountn)\
#                              values('%s', '%s', '%0.2f', '%0.2f', %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %0.2f, %s )" \
#                     %(stockData['code'], stockData['name'], stockData['cashin'], stockData['cashout'], stockData['initnetvalue'], \
#                       stockData['iorate'], stockData['turnover'], stockData['price'], stockData['initchangeratio'], stockData['amountp'], stockData['amountn'], mytime )  
                
                DBDataHandle.InsertMyStock(dboper, stockData, mytime)
    
    else: 
        
        LoggerFactory.info("SelectMyStock", "There is no qualified Stock detected at this moment!")
#         logger.info("There is no qualified Stock detected at this moment!")           
                
                

def GetFiveDaysHisData(dboper):
    
    circulated = 1800000
    
    nowtime=datetime.datetime.now()    
    detaday = datetime.timedelta(days=-6)
    days_ago= nowtime + detaday
    
    beginday = "str_to_date('%s'," % days_ago.strftime('%Y-%m-%d') + "'%Y-%m-%d')"
    endday = "str_to_date('%s'," % nowtime.strftime('%Y-%m-%d') + "'%Y-%m-%d')"
    
    sql = "select code, name, industry, circulated from stocks where status=1 and circulated<= %0.2f" % circulated
    
    results = dboper.queryData(sql)
    
    if results is not None and len(results) > 0:
        
        for stock in results:
            
            changeratio = 0
            code = stock[0] 
            name = stock[1]
            industry = stock[2]
            circulated = stock[3]

            stockeach = DBDataHandle.GetHisStockData(dboper, code, beginday, endday)
            
            if stockeach is not None and len(stockeach) == 5:
                
                for ratio in stockeach: 
                    
                    changeratio = changeratio + ratio[0]
                    
                if changeratio >= 8 and changeratio <= 9:
                    
                    print code + " ",
                    print name + " ",
                    print str(changeratio) + " ",
                    print  industry + " ",
                    print round(circulated / 10000 , 2 )

                
                
            
    

                
def checkExist(codename, codelist):            
    
    if codename in codelist:
         
        return True
    else: 
        return False   
    

if __name__ == '__main__':
    
    dboper = DBOperation.DBOperation()

#     SelectJJStock_rule1(dboper)

    GetFiveDaysHisData(dboper)
#     while True:
#              
#         mytime = int(time.strftime("%H%M%S"))
#             
#         if ( 92520 <= mytime < 92950 ):
#               
#             SelectJJStock_New( dboper )
#                  
#             time.sleep(2)
#           
#         elif ( 93000 <= mytime <= 113030 ) or ( 130000 <= mytime <= 150030 ):
#                  
#             SelectMyStock( dboper )
#                  
#             time.sleep(2)
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
    
    