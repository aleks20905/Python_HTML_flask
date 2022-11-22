from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import plotly
import plotly_express as px
import plotly.graph_objects as go
import pandas as pd
import psycopg2
import psycopg2.extras


hostname = 'localhost'
database = 'iotBrick'
username = 'postgres'
pwd = 'postgres'
port_id = 5432
conn = None

a = 0

try:
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            
                cur.execute('''SELECT * FROM ftest
                        ORDER BY id desc limit 100''')
                a = cur.fetchall()
              
                
                
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()



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



@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def show():
  
  strur = temps.query.all() #print(strur[1].id)
  
  time = [] 
  for i in strur:
    time.append('{}'.format(i.time))
    
  temp1 = []
  for i in strur:
    temp1.append('{}'.format(i.temp2) )
    
  #print(temp1)
  
  import pandas as pd
  df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

  fig = go.Figure([go.Scatter(x=df['Date'], y=df['AAPL.High'])])
 
  print("aaa")
  return render_template('success.html', gif1 = fig, temps=temp1, date = time)

  
  
# @app.route('/submit', methods=['POST'])
# def submit():
#   fname= request.form['fname']
#   lname=request.form['lname']
#   pet=request.form['pets']

#   student=Student(fname,lname,pet)
  
#   db.session.add(student)
#   db.session.commit()
  
#   strur = Student.query.all()

#   return render_template('success.html', student=strur)



if __name__ == '__main__':  #python interpreter assigns "__main__" to the file you run
  app.run(debug=True)





