import socket
import threading

PORT = 9095
IP = socket.gethostbyname(socket.gethostname())
HEADER = 64
FORMAT = 'utf-8'
DISC_MSG = '!DISCONNECT'

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((IP,PORT))


def send(msg):
    msglen = len(msg)
    len_enc = str(msglen).encode(FORMAT)
    len_enc += b' '*(HEADER - len(len_enc))
    client.send(len_enc)
    client.send(msg.encode(FORMAT))

def receive():
    global connected
    while connected:
        msglen = client.recv(HEADER).decode(FORMAT)
        if msglen:
            mlen = int(msglen)
            msg = client.recv(mlen).decode(FORMAT)
            print(msg)

def send_msg():
    global connected
    while connected:
        m = input()
        if m == '!DISCONNECT':
            connected = False
        m = f'[{name}] : {m}'
        send(m)

print("Welcome to chatroom")
name = input("Enter your name : ")
connected = True

s_thread = threading.Thread(target = send_msg)
s_thread.start()

r_thread = threading.Thread(target = receive)
r_thread.start()