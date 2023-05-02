from flask import Flask,jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import plotly
import plotly_express as px
import plotly.graph_objects as go
import pandas as pd
import psycopg2
import psycopg2.extras
import json
import time
import datetime
from threading import Thread

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost:5432/iotBrick'  
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123@localhost:5432/iotBrick'  

db=SQLAlchemy(app)

class temps(db.Model):
  __tablename__='ftest'
  id=db.Column(db.Integer,primary_key=True)
  device=db.Column(db.String(40))
  temp1=db.Column(db.DECIMAL(5,2))
  temp2=db.Column(db.DECIMAL(5,2))
  temp3=db.Column(db.DECIMAL(5,2))
  temp4=db.Column(db.DECIMAL(5,2))
  state1=db.Column(db.BOOLEAN)
  time = db.Column(db.TIMESTAMP)


def getAllDeviceLatestTelemtry():
  dic = {}
  for i in getListOfAllDevices():
    dic[i] = float( '{}'.format(temps.query.order_by(temps.id.desc()).filter_by(device=i).first().temp2) )
  return dic  
  
def getListOfAllDevices():
  return set(Extract(temps.query.all(),'device'))

def Extract(lst,t):
    return ['{}'.format(getattr(item,t)) for item in lst]
  
# @app.route('/')
# def index():
#   return render_template('index.html')

@app.route('/')
def show():
  strur = temps.query.all() 
  
  time = Extract(strur,'time') 
  temp2 = Extract(strur,'temp2')
  temp3 = Extract(strur,'temp3')

  List = getAllDeviceLatestTelemtry()
  print("aaa")
  return render_template('success.html', temps=temp2, temps2=temp3, date = time, list = List.items())


@app.route('/device')
def pendel():
  #List = {'device1':15,'device2':20,'device3':30} 
  List = getAllDeviceLatestTelemtry()
  return render_template('device.html',list = List.items())



@app.get("/update")
def now():
  strur = temps.query.order_by(temps.id.desc()).first()
  return str(strur.temp2)

@app.get("/api/temp2")
def temp2():
  strur = temps.query.all()
  return {'temp2':Extract(strur,'temp2'), 'time':Extract(strur,'time'),'temp3':Extract(strur,'temp3'),'len':len(strur)}


if __name__ == '__main__':  #python interpreter assigns "__main__" to the file you run
  # thread = Thread(target = alarm, args = ('temp2', 10)) #uncoment to activate alarms
  # thread.start()                                        #uncoment to activate alarms  
  app.run(debug=True)





