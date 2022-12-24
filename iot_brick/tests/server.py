from datetime import datetime
import socket 
import threading
import time


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

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    
    
    while connected:        
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if msg == DISCONNECT_MESSAGE:
                
                connected = False
                print(f"[DISCONNECTED {addr} disconnected.")
                break
                
                
            
                              
            else:
                telemetry  = Convert(msg.split(" | "))
                
            
            
            print(datetime.now(),telemetry)    
            
            

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print("a")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        
        


print("[STARTING] server is starting...")
start()