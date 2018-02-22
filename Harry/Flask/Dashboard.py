# -*- coding=UTF-8 -*-

'''
Created on 20180201

@author: HarryTu
'''

from flask import Flask, request, render_template

# import sys
# sys.path.append("C:\Harry\My Working\GitHub\PyStock\Harry\Stock\DBOperation")

import Harry.Stock.DBOperation as DBOperation
import Harry.Stock.MyReport as MyReport
import Harry.Stock.LoggerFactory as LoggerFactory
from pymysql import NULL


app = Flask(__name__)
logger = LoggerFactory.getLogger("Reporting")

def GetReportData():
    
    dboper = DBOperation.DBOperation()
    
    stockList = MyReport.GetMyStockReport(dboper)
    
    if stockList is None or len( stockList ) < 1:
        
        stockList = ""
        
    return stockList


def GetJJReportData():
    
    dboper = DBOperation.DBOperation()
    
    stockList = MyReport.GetJJMyStockReport(dboper)
    
    if stockList is None or len( stockList ) < 1:
    
        stockList = ""
    
    return stockList

 
@app.route("/")
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    
    stockData = GetReportData()
    
    return render_template('dashboard.html', stocks = stockData)       



@app.route('/jjdashboard')
def jjdashboard():
    
    stockData = GetJJReportData()

    return render_template('jjdashboard.html', stocks = stockData)


if __name__=="__main__":

#     app.run("10.35.83.34")
    app.run("192.168.1.3")
    

