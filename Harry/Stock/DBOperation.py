# -*- coding=UTF-8 -*-

'''
Created on 20180124

@author: HarryTu
'''

import pymysql
import DBConnection
import LoggerFactory
from pip._vendor.distlib._backport.tarfile import TUREAD


class DBOperation:
    
    def __init__(self):
        
        self.logger = LoggerFactory.getLogger("DBOperation") 
        
        self.pool = DBConnection.DBConnection().CreateConnectionPool()
        
        
    
    def poolvalidate(self):
        
        if self.pool is not None:
            
            return True
        
        else:
        
            self.logger.error("Connection Pool is Null object, please check connection Pool creation!")
                 
            return False
        
    
    def sqlExecute(self, sql):
        
        conn = self.pool.connection()
            
        if conn is not None: 
            
            try: 
                
                cursor = conn.cursor()
                
                cursor.execute( sql )
                
                conn.commit()
                
                cursor.close()
                
                conn.close()
                
                return True
            
            except Exception, e:
                
                conn.rollback()
                
                self.logger.error("SQL statement execution failed!" + "\n" + "Error message: " + str(e) + "\n" + sql )
                
                return False
        else: 
            
            self.logger.error("Cannot get DB connection!")
            
            return False
        
        
    def queryData(self, sql):
        
        conn = self.pool.connection()
        
        if conn is not None: 
            
            self.logger.debug( sql )
             
            cursor = conn.cursor()
            cursor.execute( sql )
            
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return results
        
        else: 
            
            self.logger.error("Cannot get DB connection!")
            
            return None
        
        
    def queryOneData(self, sql):
        
        conn = self.pool.connection()
        
        if conn is not None: 
            
            cursor = conn.cursor()
            cursor.execute( sql )
            
            results = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return results
        
        else: 
            
            self.logger.error("Cannot get DB connection!")
            
            return None       
            
        
if __name__ == '__main__':
    
    sql = "insert into test(id, name) values(%d, '%s')" %(1, 'commit')
    sql1 = "select code,name,circulated from stocks"
    
    dboper = DBOperation()
    
    if dboper.poolvalidate():
        
#         results =  dboper.sqlExecute(sql)
        
        results = dboper.queryData(sql1)
        
        for i in results:
            
            if i[2] <= 10:
                print i[0] + " ",
                print i[1] + " ",
                print i[2] 
        
        

        
        