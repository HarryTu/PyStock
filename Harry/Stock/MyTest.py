# -*- coding=UTF-8 -*-

'''
Created on 2018317
@author: Harry
'''

import urllib2
import requests
import LoggerFactory
import sys
import DBDataHandle
import DBOperation
import time
from bs4 import BeautifulSoup
from Harry.Stock.DBConnection import DBConnection
from _socket import timeout

def get_url_content(url):
   
    try:
        s = requests.Session()
        
        response = s.get(url, headers={ 'User-Agent': 'Mozilla/6.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20' }, timeout=3)
        response.encoding = 'gbk'
        
        if response.status_code != 200:
            
            LoggerFactory.error("get_url_content", "URL '%s' is unable to open with error code: %s"%(url, response.status_code))
            return None
      
        soup = BeautifulSoup(response.text,"html.parser")
        
        return soup
    
    except Exception, e:
        
        LoggerFactory.error("get_url_content", "Get url failed....")
        return None
    

def GetStockConcept(code):
    
    url = "http://basic.10jqka.com.cn/%s/concept.html"%(code)
    conceptlist = []
    
    soup = get_url_content(url)
    
    if soup is not None: 
        
        for tag in soup.find_all(class_='J_popLink'):
            
            conceptlist.append(tag.get_text().strip())
   
        return conceptlist
    
    else:
        
        return None 

def HandleStockConcept(dboper):
    
    mytime = "str_to_date('%s'," % time.strftime('%Y-%m-%d %H:%M:%S') + "'%Y-%m-%d %H:%i:%s')"
    
    codelist = DBDataHandle.GetStockCode(dboper)
    
    existconceptlist_sql = "select concept from stockconcept"
    results = dboper.queryData(existconceptlist_sql)
    
    existconceptData = []
    
    if results is not None and len(results) > 0:
        for name in results:
            existconceptData.append(name[0])
    
    conceptlist = []
    
    if codelist is not None and len(codelist) > 0:
        
        conceptData=[]
         
        for code in codelist:
            
            LoggerFactory.info("HandleStockConcept", "It's processing on the code: %s"%code[1])
            
            conceptlist = GetStockConcept(code[1])
            
            if conceptlist is not None:
                
                for name in conceptlist: 
                     
                    if name not in conceptData and name not in existconceptData:
                         
                        conceptData.append(name)
                        LoggerFactory.info("HandleStockConcept", "The new concept name: %s will be created"%name)
  
            time.sleep(1)
            
        counter_sql = "select max(id) from stockconcept"
        results = dboper.queryOneData(counter_sql)
        
        if results[0] is None:
            initnumber = 0 
        else: 
            initnumber = results[0]    
        
        stockData = {}
        for name in conceptData:
            
            initnumber = initnumber + 1
            stockData['id'] = initnumber
            stockData['name'] = name
            
            DBDataHandle.InsertConcept(dboper, stockData, mytime)
    
        LoggerFactory.info("HandleStockConcept", "HandleStockConcept has been completed! ")   
#         for name in conceptData: 
#             print name 


def HandleEachStockConcept(dboper):
    
    conceptid = 0
    
    codelist = DBDataHandle.GetStockCode(dboper)
    
    if codelist is not None and len(codelist) > 0:
         
        for code in codelist:
            
            conceptlist = GetStockConcept(code[1])
            
            if conceptlist is not None:
                
                LoggerFactory.info("HandleEachStockConcept", "It's dealing with the stock: %s" % code[1])
                
                for name in conceptlist: 
                    
                    sql = "select id from stockconcept where concept='%s'" % name
                    
                    results = dboper.queryOneData(sql)
                    
                    if results is not None and len(results)<2:
                    
                        conceptid = results[0]
                        
                        DBDataHandle.InsertEachStockConcept(dboper, code[1], conceptid)
                        
            time.sleep(1)           
                        
        LoggerFactory.info("HandleEachStockConcept", "HandleEachStockConcept has been completed!")                   
        
        
if __name__ == '__main__':

    dboper = DBOperation.DBOperation()
    
    
#     HandleStockConcept(dboper)
    HandleEachStockConcept(dboper)
    

    
    