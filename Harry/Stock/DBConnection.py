# -*- coding=UTF-8 -*-

'''
Created on 20180122

@author: HarryTu
'''

from DBUtils import PooledDB
import pymysql
import string
import LoggerFactory

class DBConnection:

    def __init__(self):
        self.__hostname = '127.0.0.1'
        self.__username = 'root'
        self.__password = 'SHr1ng3r'
        self.__port = 3306
        self.__db = 'pystock'
        self.__charset = 'utf8'
        self.__mincached = 5  
        self.__maxcached = 3000 
        self.__maxshared = 3000 
        self.__maxconn = 3000 
        
        self.logger = LoggerFactory.getLogger("DBConnection")
            
            
    def CreateConnectionPool(self):
        
        try:

            pool = PooledDB.PooledDB(pymysql,mincached=self.__mincached, maxconnections=self.__maxconn, maxcached=self.__maxcached,
                                     user=self.__username, passwd=self.__password, host=self.__hostname, port=self.__port, db=self.__db,charset=self.__charset)

                               
            return pool
         
        except Exception, e:
            
            self.logger.error("Failed to create connection pool with exception: " + str(e) )
              
            return None
 
     
    def CreateConnection(self):
              
        try: 
            conn = pymysql.connect(host=self.__hostname, user=self.__username, passwd=self.__password, db=self.__db, port=self.__port)
           
            return conn
        
        except Exception, e: 
            
            self.logger.error( "Failed to create DB connection with exception error: " + str(e) )
            
            return None
    
        
   
if __name__=='__main__':

    sqldbhandle = DBConnection()
     
    pool = sqldbhandle.CreateConnectionPool()
   
    if pool is not None: 
        
        conn = pool.connection()
           
        cur = conn.cursor()
              
        cur.execute("select * from test;")
                
        results = cur.fetchall()
                
        print results 
                
        cur.close()
        conn.close()
#     
#     CreateConnection();
