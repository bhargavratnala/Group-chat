import random
import socket
import threading

def room_key_generate():
    return random.randint(1000, 9999)

HOST = "127.0.0.1"  # localhost
PORT = 9090
clients = {}

class Client:

    def __init__(self, client, name = "") -> None:
        self.client = client[0]
        self.address = client[1]
        self.name = name
    
    def set_name(self, name):
        self.name = name

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen()
print("listening...")

def broadcast(msg, room, client = None):
    for i in clients[room]:
        if(i == client):
            continue
        print("message sent to :", i.name)
        i.client.send(f"<div class=\"msg{' recivemsg' if client!=None else ' servermsg'}\"><span class=\"sendername\">{client.name if client!=None else 'server '}</span>{'<br>' if client!=None else ''}<span>{msg}</span></div>".encode("utf-8"))

def handle(client : Client):
    while True:
        try:
            print(client.name, "checking for message")
            msg = client.client.recv(2048).decode()
            print(msg, "recived from", client.name)
            room = int(msg[-4:])
            msg = msg[:-5]
            print(client.name, "recived")
            if(msg == "9989eXiT7981@closeTHEuser"):
                print(f"{client.name} leaving...")
                clients[room].remove(client)
                broadcast(f"{client.name} leaving...", room)
                if(clients[room] == []):
                    print("deleting room", room)
                    del clients[room]
                break
            print("broadcast iniated by :", client.name)
            broadcast(msg, room, client)
        except Exception as e:
            print("error occured in handle", e, client.name)

while True:
    try:
        client = Client(sock.accept())
        name = client.client.recv(1024).decode()
        client.set_name(name)

        print(name, "connected..")

        while True:
            code = client.client.recv(1024).decode()
            if(code == "CreAteROoM@798199899"):
                room = room_key_generate()
                while(room in clients):
                    room = room_key_generate()
                clients[room] = [client]
            else:
                if(int(code) in clients):
                    clients[int(code)].append(client)
                    room = int(code)
                else:
                    room = 'false'
            client.client.send(f"{room}".encode("utf-8"))
            if(room!='false'):
                break

        broadcast(f"{client.name} joined in the room", room)

        thread = threading.Thread(target= handle, args=(client,))
        thread.start()
        print("thread started..")
    except Exception as e:
        print("error occured in connecting", e)