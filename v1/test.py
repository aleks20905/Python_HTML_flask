import psycopg2
import psycopg2.extras
import time
import datetime
import requests
from threading import Thread
hostname = 'localhost'
database = 'iotBrick'
username = 'postgres'
pwd = 'postgres'
port_id = 5432
conn = None

startTime = '2022-12-01 00:00:00'# not in use
endTime =   '2022-12-10 15:50:00'# not in use

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
                                    ORDER BY id DESC'''.format(datetime.datetime.now() - datetime.timedelta(minutes=5) , datetime.datetime.now()))#set time to search in db
                            
                a= cur.fetchall()
                count= 0
                print(".", end=" ") #printing ......
                for i in a:
                    print(len(a),count,len(a)*0.7<count) 
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


thread = Thread(target = alarm, args = ('temp2', 10))
thread.start()  
# thread1 = Thread(target = alarm, args = ('temp3', 50))
# thread1.start() 
                     
                
                
               

                
              
                

  
