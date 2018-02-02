# -*- coding=UTF-8 -*-

'''
Created on 20180201

@author: HarryTu
'''

from flask import Flask, request, render_template

import Harry.Stock.DBOperation as DBOperation
import Harry.Stock.MyReport as MyReport
import Harry.Stock.LoggerFactory as LoggerFactory


app = Flask(__name__)


def GetReportData():
    
    dboper = DBOperation.DBOperation()
    
    stockList = MyReport.GetMyStockReport(dboper)
    
    return stockList

 
@app.route("/")
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    
    stockData = GetReportData()
    
    return render_template('dashboard.html', stocks = stockData)            

if __name__=="__main__":

    app.run()
    

