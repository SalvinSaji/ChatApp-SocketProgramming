import socket
import threading

PORT = 9095
IP = socket.gethostbyname(socket.gethostname())
HEADER = 64
FORMAT = 'utf-8'
DISC_MSG = '!DISCONNECT'

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((IP,PORT))

client_list = []

def send(msg,client):
    msglen = len(msg)
    len_enc = str(msglen).encode(FORMAT)
    len_enc += b' '*(HEADER - len(len_enc))
    client.send(len_enc)
    client.send(msg.encode(FORMAT))

def broadcast(msg,conn):
    for client in client_list:
        if client!=conn:
            send(msg,client)

def handle_client(conn,addr):
    print(f'[SERVER]{addr} connected')
    client_list.append(conn)
    connected = True

    while connected:
        msglen = conn.recv(HEADER).decode(FORMAT)
        if msglen:
            mlen = int(msglen)
            msg = conn.recv(mlen).decode(FORMAT)
            print(f"{msg}")
            broadcast(msg,conn)
            if(msg.split(' ')[-1] == DISC_MSG):
                connected = False
                client_list.remove(conn)
    conn.close()  
    print(f"[SERVER] active connections = {threading.activeCount() - 2}")

def start():
    server.listen()
    print(f"[SERVER] server started at {IP}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn,addr))
        thread.start()
        print(f"[SERVER] active connections = {threading.activeCount() - 1}")

print('[SERVER] Starting ...')
start()
