from flask import Flask,jsonify, render_template, request, redirect, url_for, make_response, flash
from flask_sqlalchemy import SQLAlchemy
import plotly
import plotly.graph_objects as go
import pandas as pd
import psycopg2
import psycopg2.extras
import json
import time
from datetime import datetime, timedelta
import csv
from threading import Thread
import requests

# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

def alarm_main(DeviceName,strname, temp):
       
  a = temps.query.filter_by(device=DeviceName).filter(temps.time>=datetime.now() - timedelta(minutes=6)).all() # fetch all data for the last 6 min
  count= 0
  print(".") #printing ......
  
  for i in a:
      
      if i[strname]>temp:
          count+=1
          #print(i )#-timedelta(seconds=5) 
                      
      if len(a)*0.7<count:
          #requests.post("https://api.telegram.org/bot5495441993:AAFy_9ujooWqi5ZH2PiMXCAXoxxf6ZkvUeY/sendMessage?chat_id=-1001683799597&text={} {}".format(strname,datetime.now()))
          #print("aa")        #do someting
          print("well ") 
          print(len(a),count,len(a)*0.7<count) 
          time.sleep(30)
          
  time.sleep(2)


def get_average_temp(device,row,time_ago):
    # Query the database for the average value of "temp1" for the last 5 minutes
    result = db.session.query(db.func.avg(getattr(temps,row))).filter(temps.device == device).filter(temps.time > time_ago).first()
    
    # Return the average temperature value rounded to 2 decimal places
    return round(result[0], 2) if result[0] is not None else None
       

def test_alarm():
  
  while True:
    
    time_ago = datetime.now() - timedelta(days=306)
    data = {'temp1','temp2','temp3','temp4'}
  
    alarm_state = [{"device":rec.device, 'temp1' :rec.temp1,'temp2' :rec.temp2,'temp3' :rec.temp3,'temp4' :rec.temp4,'globalstatus':rec.globalstatus} for rec in alarms_state.query.all()]
    all_on_devices = [ sub['device'] for sub in alarm_state if sub["globalstatus"]] # list of all devices witch alarms_state is turn 'On'
    
    
    # all_records = temps.query.filter(temps.device.in_(all_on_devices)).filter(temps.time>=time_ago).all() # fetch all data for the last 6 min
    # mylist = [{"device": rec.device, 'temp1': rec.temp1, 'temp2': rec.temp2, 'temp3': rec.temp3, 'temp4': rec.temp4} for rec in all_records]
    
    db_alarm_value = alarms_value.query.all()
    alarm_value = {i.device: {'temp1': i.temp1, 'temp2': i.temp2, 'temp3': i.temp3, 'temp4': i.temp4} for i in db_alarm_value}
    
    
    selected_devices = get_all_devices(temps.query.filter(temps.device.in_(all_on_devices)).all())  
    average_of_devices = {dev:{row: get_average_temp(dev,row, time_ago) for row in data} for dev in selected_devices}
    
    
    # print(average_of_devices)
    # print(alarm_value)
    
    request_status = False
    time.sleep(5)  
    for key, value in average_of_devices.items():
      if key in alarm_value:
        for subkey, subvalue in value.items():
          if subkey in alarm_value[key]:
            if subvalue > alarm_value[key][subkey]:
              request_status = True
              time.sleep(1) 
              #requests.post("https://api.telegram.org/bot5495441993:AAFy_9ujooWqi5ZH2PiMXCAXoxxf6ZkvUeY/sendMessage?chat_id=-1001683799597&text= {}".format(f"device: {key} | temperature is {subvalue} settet limit is {alarm_value[key][subkey]} and exceed the target by[{subvalue - alarm_value[key][subkey]}]"))
              print(f"device: {key} | temperature is {subvalue} settet limit is {alarm_value[key][subkey]} and exceed the target by[{subvalue - alarm_value[key][subkey]}]")   
    db.session.commit()                           
    if request_status:
      time.sleep(30)  
    time.sleep(5)  
      
            
app = Flask(__name__)
app.secret_key = "padeaznam"

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
class alarms_state(db.Model):
  __tablename__='alarms'
  id = db.Column(db.Integer,primary_key=True)
  device =  db.Column(db.String(40))
  temp1 =   db.Column(db.BOOLEAN) 
  temp2 =   db.Column(db.BOOLEAN)
  temp3 =   db.Column(db.BOOLEAN)
  temp4 =   db.Column(db.BOOLEAN)
  state1 =  db.Column(db.BOOLEAN)
  globalstatus = db.Column(db.BOOLEAN)
class alarms_value(db.Model):
  __tablename__='alarmsvalue'
  id=db.Column(db.Integer,primary_key=True)
  device=db.Column(db.String(40))
  temp1=db.Column(db.DECIMAL(5,2))
  temp2=db.Column(db.DECIMAL(5,2))
  temp3=db.Column(db.DECIMAL(5,2))
  temp4=db.Column(db.DECIMAL(5,2))

def getAllDeviceLatestTelemtry():
  dic = {}
  for i in get_all_devices(temps.query.all()):
    dic[i] = float( '{}'.format(temps.query.order_by(temps.id.desc()).filter_by(device=i).first().temp2) )
  return dic  

def getAllDeviceLatestRespons():
  dic = {}
  for i in get_all_devices(temps.query.all()):
    dic[i] =  '{}'.format(temps.query.order_by(temps.id.desc()).filter_by(device=i).first().time)
  return dic 
  
def get_all_devices(db): # return list of all devices in selected db "DBtemp/ftest"
  return list(set(Extract(db,'device')))

def Extract(lst,t): # extrakt data from db Extrakt(temps.query.all(),'time')
  # lst = from where to extrakt || t = what to extrakt
  return ['{}'.format(getattr(item,t)) for item in lst]

def globalstatus_alarms(): # return globalstatus Alarm dict with all devices
  a = alarms_state.query.all()
  mylist = {}
  for i in a:
    mylist[i.device]={'temp1' :i.temp1,'temp2' :i.temp2,'temp3' :i.temp3,'temp4' :i.temp4,'state1':i.state1,'globalstatus' :i.globalstatus}
  
  for i in get_all_devices(temps.query.all()): # chek if all devices in DBalarms_state are in DBtemps 
    if (i not in mylist):         # and if not it create virtial just for buffer just to NOT CRASH !!!
      mylist[i]={'temp1' :False,'temp2' :False,'temp3' :False,'temp4' :False,'state1':False,'globalstatus' :False}
      print("create new alarms cuz doesnt exist")
        
  dic = {}
  #print(mylist)
  for i,y in mylist.items(): # conver the the dict from False/True to Off/On
    for b in y:
      dic[i] = 'On' if y['globalstatus'] == True else 'Off' 
      
  #print(dic)    
  return dic # return dict with all devices: globalstatus || {device: Off/On, device: Off/On}

def dicCount(): # return dict with device: count || {device1: 1, devic2: 2}
  dic = {}
  count = 1
  for i in get_all_devices(temps.query.all()):
    dic[i] = count
    count +=1
  return dic 
  
def alarms_values_list():
  a = alarms_value.query.all()
  
  mylist = {}
  for i in a:
    mylist[i.device]={'temp1' :i.temp1,'temp2' :i.temp2,'temp3' :i.temp3,'temp4' :i.temp4}
  
  for i in get_all_devices(temps.query.all()): # chek if all devices in DBalarms_state are in DBtemps 
    if (i not in mylist):         # and if not it create virtial just for buffer just to NOT CRASH !!!
      mylist[i]={'temp1' :None,'temp2' :None,'temp3' :None,'temp4' :None}
      print("create new alarms cuz doesnt exist")
      
  return mylist

@app.route('/device/')
@app.route('/device/<DeviceName>')
def device(DeviceName = 'None' ):
  if (DeviceName == 'None'): DeviceName = get_all_devices(temps.query.all())[0]
  #print('route somteint ###- {} -###'.format(DeviceName))
  #strur = temps.query.all() #print(strur[1].id)
  
  # time = Extract(strur,'time') 
  # temp2 = Extract(strur,'temp2')
  # temp3 = Extract(strur,'temp3')
  # temp4 = Extract(strur,'temp4') 
  telemetry =  temptest(DeviceName)
  List = get_telemetry(DeviceName)
  print("started main")
  return render_template('device.html',telemetry = telemetry, list = List.items(),DeviceName = DeviceName)

@app.route('/devices') ## MAIN
def devices():
  db.create_all() # create new tables if needed
  List = getAllDeviceLatestTelemtry()
  a = get_ifConnected()
  b = get_latestResponse()
  curentConut = dicCount()
  
  ks = [k for k in List.keys()]
  d_merged = {k: (List[k], a[k], b[k], curentConut[k]) for k in ks}
  #print(d_merged) 
  return render_template('devices.html' ,list = d_merged.items())


@app.route('/alarms/') 
def alarms():
  ##strur = alarms_state.query.all() #print(strur[1].id)
  
  
  List = getAllDeviceLatestTelemtry()
  #a = get_ifConnected()
  a = globalstatus_alarms()
  b = get_latestResponse()
  curentConut = dicCount()
  
  ks = [k for k in List.keys()]
  d_merged = {k: (List[k], a[k], b[k], curentConut[k]) for k in ks}
  
  return render_template('alarms.html', list = d_merged.items(),lenth = len(d_merged))

@app.route('/alarm/')
@app.route('/alarm/<DeviceName>', methods=['POST','GET']) 
def alarm(DeviceName = 'None'):
  if (DeviceName == 'None'): DeviceName = get_all_devices(temps.query.all())[0]
  db.create_all() # create new tables if needed
  d_base = alarms_value.query.filter_by(device=DeviceName).first()

  if request.method == 'POST':
    req_form = request.form.to_dict() # request form the site gets the atribute and returns dict of it
    for i,y in req_form.items(): # using req_form updates the DB 
      setattr(d_base, i, y) #this secificli update the DB (ref_to_DB, atribute_name, atribute_value)
      db.session.commit()
      
      flash("deta update succesfuly","success")  
      
    
  if (d_base is None): # if device doest exist in alarms_value it creates one
    print("alarms_value add new element")
    user = alarms_value(device = DeviceName ,temp1='50', temp2='50',temp3='50',temp4='50') 
    db.session.add(user)
    db.session.commit() 
    d_base =  alarms_value.query.filter_by(device=DeviceName).first()
  
  d_merged = {
    "temp1": (None, 'On', d_base.temp1, 1),
    "temp2": (None, 'On', d_base.temp2, 2),
    "temp3": (None, 'On', d_base.temp3, 3),
    "temp4": (None, 'On', d_base.temp4, 4),
              }
  
  return render_template('alarm.html', list = d_merged.items(),lenth = len(d_merged),DeviceName = DeviceName)



@app.get("/update") # test not in use
def now():
  strur = temps.query.order_by(temps.id.desc()).first()
  return str(strur.temp2)

@app.get("/api/temp2") # not in use 
def temp2():
  strur = temps.query.all()
  
  time = Extract(strur,'time') 
  temp2 = Extract(strur,'temp2')
  temp3 = Extract(strur,'temp3')
  
  return {'temp2':temp2, 'time':time,'temp3':temp3,'len':len(strur)}

@app.get("/api/ttest")
@app.get("/api/ttest/<name>")
def temptest(name = 'None'): #MAIN FETCHING DATA TO main Chart
  if (name == 'None' or not name in get_all_devices(temps.query.all())): name = get_all_devices(temps.query.all())[0]
  #print( not name in get_all_devices(temps.query.all()))
  #strur = temps.query.all()
  strur = temps.query.filter_by(device=name).all()
  
  time = Extract(strur,'time') 
  temp1 = Extract(strur,'temp1')
  temp2 = Extract(strur,'temp2')
  temp3 = Extract(strur,'temp3')
  temp4 = Extract(strur,'temp4')
  
  return {'temp1':temp1,'temp2':temp2, 'time':time,'temp3':temp3, 'temp4': temp4,'len':len(strur)}


@app.get("/test") # TEST NOT IN USE CHEK FOR SPEC DEVICE MANUALY
def test_1():
  temp2 = temps.query.order_by(temps.id.desc()).filter_by(device='esp32Unknow123').first().temp2
  return str(temp2)  


@app.get("/get/telemetry/<name>")
def get_telemetry(name = 'None'): # GET SPEC TELEMETRY DATA
  if (name == 'None'): name = get_all_devices(temps.query.all())[0]
  #print('get stuff ### - {} - ####'.format(name))
  strur = temps.query.order_by(temps.id.desc()).filter_by(device=name).first() # can bug if device doesnt exist in db
  return {'temp2': float(strur.temp2),'temp3':float(strur.temp3),'temp4':float(strur.temp4)}

@app.get("/get/latestResponse")
def get_latestResponse(): # GET list of latest response form the devices
  a = getAllDeviceLatestRespons()
 
  for i in a:
    a[i] = a[i][:-7]
   
  return a

@app.get("/get/ifConnected")
def get_ifConnected(): # get list of if devices i connected
  
  a = getAllDeviceLatestRespons()
  a = {i:datetime.strptime(a[i], '%Y-%m-%d %H:%M:%S.%f') for i in a} 
  # {'Esp8266N2': datetime(2023, 1, 19, 18, 32, 29, 848165), 'Esp8266': datetime(2023, 1, 19, 19, 8, 47, 745108), 'Esp8266new': datetime(2023, 1, 19, 19, 8, 49, 751757)}
  #print(a) 
  for i in a:
    a[i] = 'connected' if a[i] > datetime.now() -  timedelta(minutes=1) else 'disconnected' # timedelta(minutes=1) set the time to get connected stament
    #a[i] = a[i] > datetime.now() -  timedelta(minutes=1)
  return a

@app.route('/csv/')  
def download_csv():  
  data = temps.query.all()
  a = []
  headers = ['device', 'temp1', 'temp2', 'temp3', 'temp4', 'state1','time']  # replace with your own model's column names
  a.append(headers)
   
  for row in data:
    a.append([row.device, row.time, row.temp1, row.temp2, row.temp3, row.temp4, row.state1]) 
  
  csv = str(a) 
  response = make_response(csv)
  cd = 'attachment; filename=mycsv.csv'
  response.headers['Content-Disposition'] = cd 
  response.mimetype='text/csv'
  return response

if __name__ == '__main__':  #python interpreter assigns "__main__" to the file you run
                                       
  t = Thread(target=test_alarm,daemon=True)
  t.start() 
  
  app.run(host='0.0.0.0', port=5000,debug=True)
  #app.run(host='0.0.0.0', port=5000,debug=True, use_debugger=False, use_reloader=False)





