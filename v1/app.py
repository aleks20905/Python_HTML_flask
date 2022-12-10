from flask import Flask, render_template, request
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


hostname = 'localhost'
database = 'iotBrick'
username = 'postgres'
pwd = 'postgres'
port_id = 5432
conn = None

def a():
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

def alarm(strname, temp):
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
    
            while True:
                cur.execute('''SELECT * FROM ftest
                                    WHERE time BETWEEN '{}' and '{}'  
                                    ORDER BY id DESC'''.format(datetime.datetime.now() - datetime.timedelta(minutes=6) , datetime.datetime.now()))#set time to search in db
                            
                a= cur.fetchall()
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
                
    if conn is not None:
        conn.close()


# thread = Thread(target = alarm, args = ('temp2', 10)) #uncoment to activate alarms
# thread.start()                                        #uncoment to activate alarms


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost:5432/iotBrick'

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


def Extract(lst,t):
    return ['{}'.format(getattr(item,t)) for item in lst]
  
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def show():
  
  strur = temps.query.all() #print(strur[1].id)
  
  time = Extract(strur,'time') 
  temp2 = Extract(strur,'temp2')
  
  fig = go.Figure()
  fig.add_trace(go.Scatter(name='temp2', x=time, y=temp2, line_shape='spline',showlegend=True))
  fig.update_layout(height=500, width=1500)
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  
  #print(temp1)
  #print("aaa")
  return render_template('success.html', temps=temp2, date = time, graphJSON = graphJSON)

  

if __name__ == '__main__':  #python interpreter assigns "__main__" to the file you run
  app.run(debug=True)





