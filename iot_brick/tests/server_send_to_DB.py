from datetime import datetime
from itertools import count, tee
import socket 
import threading
import time
import psycopg2
import psycopg2.extras

hostname = 'localhost'
database = 'iotBrick'
username = 'postgres'
pwd = 'postgres'
port_id = 5432
conn = None

HEADER = 64
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

telemetry = None

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    conn.settimeout(10)
    
    with psycopg2.connect(
                            host = hostname,
                            dbname = database,
                            user = username,
                            password = pwd,
                            port = port_id) as con:
    
        connected = True    
        while connected:    
            fmsg = ""
            try:
                fmsg = conn.recv(100).decode(FORMAT)
                #print('ADASDASDA ASDA '+ fmsg)
                if fmsg and fmsg[:1]=='&':   
                      
                    smsg = fmsg[1:]
                    #print(smsg)
                    msg = smsg.split('&')
                    #print(msg)
                    telemetry  = Convert(msg[0].split(" | "))
                    #print("aaa")
                                

                    with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

                            
                        insert_script  = 'INSERT INTO ftest (device, temp2, temp3, temp4, state1, time) VALUES ( %s, %s, %s, %s, %s, %s)'
                        insert_values = (telemetry["device"],telemetry["temp2"],telemetry["temp3"],telemetry["temp4"],telemetry["state1"],datetime.now())
                                
                        cur.execute(insert_script, insert_values)   
                    con.commit()

                                                    
                        
                    
                    #print(len(telemetry))
                    print(datetime.now(),telemetry)  
                    
                
            except socket.timeout as e:
                connected = False
                print(f"[DISCONNECTED {addr} disconnected.")
                break    
                
              
            
            
    if con is not None:
        con.close()
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        
        


print("[STARTING] server is starting...")
start()





