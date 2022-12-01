import psycopg2
import psycopg2.extras
import time
import datetime
import requests
hostname = 'localhost'
database = 'iotBrick'
username = 'postgres'
pwd = 'postgres'
port_id = 5432
conn = None

startTime = '2022-12-01 00:00:00'
endTime =   '2022-12-10 15:50:00'


def alarm(a,strname, temp):
    count= 0
    for i in a:
        if i[strname]>temp:
            count+=1
            #print(i )#-datetime.timedelta(seconds=5) 
                        
        if len(a)*0.7<count:
            #requests.post("https://api.telegram.org/bot5495441993:AAFy_9ujooWqi5ZH2PiMXCAXoxxf6ZkvUeY/sendMessage?chat_id=-1001683799597&text={}".format(datetime.datetime.now()))
            #print("aa")        #do someting
            time.sleep(10)
            print(len(a),count,len(a)*0.7<count) 
    
try:
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
                        ORDER BY id DESC'''.format(datetime.datetime.now() - datetime.timedelta(minutes=5) , datetime.datetime.now()))
                
                fet= cur.fetchall()
                alarm(fet,'temp2',50)
                time.sleep(1)
                
                     
                
                
               

                
              
                
                
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
