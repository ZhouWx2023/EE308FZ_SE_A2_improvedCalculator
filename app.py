# -*- coding: utf-8 -*-
from calculate import *
from flask import Flask, jsonify, render_template, request
#import sqlite3 as sql


app = Flask(__name__)

num=0
conn = sqlite3.connect('hist.db')   // connect to database
conn.execute('DROP TABLE histCal')  // delete previous history table
conn.execute('CREATE TABLE histCal (id INT PRIMARY KEY NOT NULL, expr TEXT NOT NULL, results TEXT NOT NULL)')  // create a new table

@app.route('/_calculate')   
def calculate():    // calculation
    exp = request.args.get('exp')
    try:
        result = count(exp)
    except:
        result = '#'
    return jsonify(result=result)

def addtohist():   // add a new item to the table in database
    num = num+1
    exp = request.args.get('exp')  
    result = count(exp)  
    try:
        with sqlite3.connect(hist.db) as con:
           cur = con.cursor()
           cur.execute("INSERT INTO histCal(id, expr, results) VALUES (?,?,?)",(num,exp,result))
           con.commit()
           msg = "data is added successfully"
    except:
        con.rollback()
        msg= "data saving is failed."
    finally:
        conn.close()
        
def readlist():  // read all the items from the database
   con = sql.connect("hist.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from history")
   
   rows = cur.fetchall();
   return jsonify(history=rows)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()