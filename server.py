import socket
import threading
import subprocess

out = subprocess.getoutput("ipconfig").split("\n")
for i in out:
    if(i.strip().startswith("IPv4")):
        out = i
        break

# HOST = "127.0.0.1"  # localhost
HOST = out.split()[-1]    # ip address of pc
PORT = 9090
clients = []

class Client:

    def __init__(self, client) -> None:
        self.client = client[0]
        self.address = client[1]
        self.name = None
    
    def set_name(self, name):
        self.name = name

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen()
print("listening...")

def broadcast(msg, client):
    for i in clients:
        if(i == client):
            continue
        print("message sent to :", i.name)
        i.client.send(f"<span class=\"sendername\">{client.name}</span><br>{msg}".encode("utf-8"))

def handle(client : Client):
    while True:
        try:
            print(client.name, "checking for message")
            msg = client.client.recv(2048).decode()
            print(client.name, "recived")
            if(msg == "exit"):
                print(f"{client.name} leaving...")
                clients.remove(client)
                break
            print("broadcast iniated by :", client.name)
            broadcast(msg, client)
        except:
            print("error occured in handle", client.name)

while True:
    try:
        client = Client(sock.accept())
        name = client.client.recv(1024).decode()
        client.set_name(name)
        clients.append(client)

        print(name, "connected..")

        client.client.send("Connected...".encode())

        thread = threading.Thread(target= handle, args=(client,))
        thread.start()
        print("thread started..")
    except:
        print("error occured in connecting")