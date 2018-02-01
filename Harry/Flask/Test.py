# -*- coding=UTF-8 -*-

'''
Created on 20180201

@author: HarryTu
'''

from flask import Flask, request, render_template

import Harry.Stock.DBOperation as DBOperation
import Harry.Stock.MyReport as MyReport


app = Flask(__name__)


def TestData():
    
    dboper = DBOperation.DBOperation()
    
    stockList = MyReport.GetMyStockReport(dboper)
    
    return stockList


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/dashborad')
def dashborad():
    
    stockData = TestData()
    
    return render_template('Dashborad.html', stocks = stockData)            

if __name__=="__main__":

    app.run()
    

