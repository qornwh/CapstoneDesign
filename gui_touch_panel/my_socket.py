import socket
import threading
import time

ip = '192.168.137.1'
port = 55555
size = 1024

client = None

def setting():
    global client
    while(True):
        try:
            print("connecting~~")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.settimeout(3)
            print("connect on")
            break

        except:
            print('Time out : connecting fail')

def sendNrecv(msg):
    global client
    try:
        client.send(msg.encode())
        data = client.recv(size)
        print(data.decode())
        return data.decode()

    except socket.timeout:
        data = _recv()
        if(data == -102):
            data = _recv()
        return data

def _recv():
    global client
    try:
        data = client.recv(size)
        return data.decode()
        
    except socket.timeout:
        print('time out')
        return -102
    
        
def sockClosing():
    global client
    client.close()
    print('disconnected')
