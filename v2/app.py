from flask import Flask,jsonify, render_template, request, redirect, url_for, flash
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

# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

hostname = 'localhost'
database = 'iotBrick'
username = 'postgres'
pwd = 'postgres'
#pwd = '123'
port_id = 5432
conn = None

def comment():
### a = 0

# try:
#     with psycopg2.connect(
#                 host = hostname,
#                 dbname = database,
#                 user = username,
#                 password = pwd,
#                 port = port_id) as conn:

#         with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            
#                 cur.execute('''SELECT * FROM ftest
#                         ORDER BY id desc limit 100''')
#                 a = cur.fetchall()
              
                
                
# except Exception as error:
#     print(error)
# finally:
#     if conn is not None:
#         conn.close()
  print("aaa")

def alarm_main(DeviceName,strname, temp):
       
  a = temps.query.filter_by(device=DeviceName).filter(temps.time>=datetime.datetime.now() - datetime.timedelta(minutes=6)).all() # fetch all data for the last 6 min
  count= 0
  print(".") #printing ......
  
  for i in a:
      
      if i[strname]>temp:
          count+=1
          #print(i )#-datetime.timedelta(seconds=5) 
                      
      if len(a)*0.7<count:
          #requests.post("https://api.telegram.org/bot5495441993:AAFy_9ujooWqi5ZH2PiMXCAXoxxf6ZkvUeY/sendMessage?chat_id=-1001683799597&text={} {}".format(strname,datetime.datetime.now()))
          #print("aa")        #do someting
          print("well ") 
          print(len(a),count,len(a)*0.7<count) 
          time.sleep(30)
          
  time.sleep(2)
                
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
class alarms_sate(db.Model):
  __tablename__='alarms'
  id = db.Column(db.Integer,primary_key=True)
  device =  db.Column(db.String(40))
  temp1 =   db.Column(db.BOOLEAN) 
  temp2 =   db.Column(db.BOOLEAN)
  temp3 =   db.Column(db.BOOLEAN)
  temp4 =   db.Column(db.BOOLEAN)
  state1 =  db.Column(db.BOOLEAN)
  globalstatus = db.Column(db.BOOLEAN)
class alamrs_value(db.Model):
  __tablename__='alarmsvalue'
  id=db.Column(db.Integer,primary_key=True)
  device=db.Column(db.String(40))
  temp1=db.Column(db.DECIMAL(5,2))
  temp2=db.Column(db.DECIMAL(5,2))
  temp3=db.Column(db.DECIMAL(5,2))
  temp4=db.Column(db.DECIMAL(5,2))

def getAllDeviceLatestTelemtry():
  dic = {}
  for i in getListOfAllDevices():
    dic[i] = float( '{}'.format(temps.query.order_by(temps.id.desc()).filter_by(device=i).first().temp2) )
  return dic  

def getAllDeviceLatestRespons():
  dic = {}
  for i in getListOfAllDevices():
    dic[i] =  '{}'.format(temps.query.order_by(temps.id.desc()).filter_by(device=i).first().time)
  return dic 
  
def getListOfAllDevices(): # return list of all devices in DBtemp/ftest
  return list(set(Extract(temps.query.all(),'device')))

def Extract(lst,t): # extrakt data from db Extrakt(temps.query.all(),'time')
  # lst = from where to extrakt || t = what to extrakt
  return ['{}'.format(getattr(item,t)) for item in lst]

def globalstatus_alarms(): # return globalstatus Alarm dict with all devices
  a = alarms_sate.query.all()
  mylist = {}
  for i in a:
    mylist[i.device]={'temp1' :i.temp1,'temp2' :i.temp2,'temp3' :i.temp3,'temp4' :i.temp4,'state1':i.state1,'globalstatus' :i.globalstatus}
  
  for i in getListOfAllDevices(): # chek if all devices in DBalarms_sate are in DBtemps 
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
  for i in getListOfAllDevices():
    dic[i] = count
    count +=1
  return dic 
  
def alarms_values_list():
  a = alamrs_value.query.all()
  
  mylist = {}
  for i in a:
    mylist[i.device]={'temp1' :i.temp1,'temp2' :i.temp2,'temp3' :i.temp3,'temp4' :i.temp4}
  
  for i in getListOfAllDevices(): # chek if all devices in DBalarms_sate are in DBtemps 
    if (i not in mylist):         # and if not it create virtial just for buffer just to NOT CRASH !!!
      mylist[i]={'temp1' :None,'temp2' :None,'temp3' :None,'temp4' :None}
      print("create new alarms cuz doesnt exist")
      
  return mylist

@app.route('/device/')
@app.route('/device/<DeviceName>')
def device(DeviceName = 'None' ):
  if (DeviceName == 'None'): DeviceName = getListOfAllDevices()[0]
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
  List = getAllDeviceLatestTelemtry()
  a = get_ifConnected()
  b = get_latestResponse()
  curentConut = dicCount()
  
  ks = [k for k in List.keys()]
  d_merged = {k: (List[k], a[k], b[k], curentConut[k]) for k in ks}
  #print(d_merged) 
  return render_template('devices.html' ,list = d_merged.items())


@app.route('/alarms/') ## TO DO 
def alarms():
  ##strur = alarms_sate.query.all() #print(strur[1].id)
  
  
  List = getAllDeviceLatestTelemtry()
  #a = get_ifConnected()
  a = globalstatus_alarms()
  b = get_latestResponse()
  curentConut = dicCount()
  
  ks = [k for k in List.keys()]
  d_merged = {k: (List[k], a[k], b[k], curentConut[k]) for k in ks}
  
  return render_template('alarms.html', list = d_merged.items(),lenth = len(d_merged))

@app.route('/alarm/')
@app.route('/alarm/<DeviceName>', methods=['POST','GET']) ## TO DO 
def alarm(DeviceName = 'None'):
  if (DeviceName == 'None'): DeviceName = getListOfAllDevices()[0]
  d_base = alamrs_value.query.filter_by(device=DeviceName).first()

  if request.method == 'POST':
    req_form = request.form.to_dict() # request form the site gets the atribute and returns dict of it
    for i,y in req_form.items(): # using req_form updates the DB 
      setattr(d_base, i, y) #this secificli update the DB (ref_to_DB, atribute_name, atribute_value)
      db.session.commit()
      flash("deta update succesfuly","success")  
      
    
  if (d_base is None): # if device doest exist in alarms_value it creates one
    print("alamrs_value add new element")
    user = alamrs_value(device = DeviceName ,temp1='50', temp2='50',temp3='50',temp4='50') 
    db.session.add(user)
    db.session.commit() 
   
  d_merged = {
    "temp1": (None, 'On', d_base.temp1, 1),
    "temp2": (None, 'On', d_base.temp2, 2),
    "temp3": (None, 'On', d_base.temp3, 3),
    "temp4": (None, 'On', d_base.temp4, 4),
              }
  
  return render_template('alarm.html', list = d_merged.items(),lenth = len(d_merged),DeviceName = DeviceName)



@app.get("/update")
def now():
  strur = temps.query.order_by(temps.id.desc()).first()
  return str(strur.temp2)

@app.get("/api/temp2")
def temp2():
  strur = temps.query.all()
  
  time = Extract(strur,'time') 
  temp2 = Extract(strur,'temp2')
  temp3 = Extract(strur,'temp3')
  
  return {'temp2':temp2, 'time':time,'temp3':temp3,'len':len(strur)}

@app.get("/api/ttest")
@app.get("/api/ttest/<name>")
def temptest(name = 'None'):
  if (name == 'None' or not name in getListOfAllDevices()): name = getListOfAllDevices()[0]
  #print( not name in getListOfAllDevices())
  #strur = temps.query.all()
  strur = temps.query.filter_by(device=name).all()
  
  time = Extract(strur,'time') 
  temp1 = Extract(strur,'temp1')
  temp2 = Extract(strur,'temp2')
  temp3 = Extract(strur,'temp3')
  temp4 = Extract(strur,'temp4')
  
  return {'temp1':temp1,'temp2':temp2, 'time':time,'temp3':temp3, 'temp4': temp4,'len':len(strur)}


@app.get("/test")
def test_1():
  temp2 = temps.query.order_by(temps.id.desc()).filter_by(device='esp32Unknow123').first().temp2
  return str(temp2)  


@app.get("/get/telemetry/<name>")
def get_telemetry(name = 'None'):
  if (name == 'None'): name = getListOfAllDevices()[0]
  #print('get stuff ### - {} - ####'.format(name))
  strur = temps.query.order_by(temps.id.desc()).filter_by(device=name).first() # can bug if device doesnt exist in db
  return {'temp2': float(strur.temp2),'temp3':float(strur.temp3),'temp4':float(strur.temp4)}

@app.get("/get/latestResponse")
def get_latestResponse():
  a = getAllDeviceLatestRespons()
 
  for i in a:
    a[i] = a[i][:-7]
   
  return a

@app.get("/get/ifConnected")
def get_ifConnected():
  
  a = getAllDeviceLatestRespons()
  a = {i:datetime.datetime.strptime(a[i], '%Y-%m-%d %H:%M:%S.%f') for i in a} 
  # {'Esp8266N2': datetime.datetime(2023, 1, 19, 18, 32, 29, 848165), 'Esp8266': datetime.datetime(2023, 1, 19, 19, 8, 47, 745108), 'Esp8266new': datetime.datetime(2023, 1, 19, 19, 8, 49, 751757)}
  #print(a) 
  for i in a:
    a[i] = 'connected' if a[i] > datetime.datetime.now() -  datetime.timedelta(minutes=1) else 'disconnected' # datetime.timedelta(minutes=1) set the time to get connected stament
    #a[i] = a[i] > datetime.datetime.now() -  datetime.timedelta(minutes=1)
  return a

if __name__ == '__main__':  #python interpreter assigns "__main__" to the file you run
  # thread = Thread(target = alarm, args = ('temp2', 10)) #uncoment to activate alarms
  # thread.start()                                        #uncoment to activate alarms  
  
  
  db.create_all() # create new tables if needed
  app.run(host='0.0.0.0', port=5000,debug=True)
  #app.run(host='0.0.0.0', port=5000,debug=True, use_debugger=False, use_reloader=False)





