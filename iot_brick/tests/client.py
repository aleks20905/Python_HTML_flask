import socket

HEADER = 64
PORT = 8080
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.11.209"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
    
   
send("device | esp8266 | chaimber | -5.56 | freon | 20 | outsideT | 15 | outsidT | 10 ")
input() 
send("device | esp8266 | chaimber | -5.506 | freon | 25 | outsideT | 5 | outsidT | 10 ")
input() 

send(DISCONNECT_MESSAGE)