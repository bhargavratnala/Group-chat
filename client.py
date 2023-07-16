import socket
# import threading
import subprocess
import flask

class Sock:

    def __init__(self, sock, count) -> None:
        self.sock = sock
        self.count = count
        self.name = None
        self.room = None
    
    def set_room(self, room):
        self.room = room
    
    def set_name(self, name):
        self.name = name

app = flask.Flask(__name__, template_folder='template', static_folder='static')
sock = {}
count = 0

HOST = "127.0.0.1"  # localhost
PORT = 9090

@app.route("/")
def index():
    global count, sock
    try:
        sock[count] = Sock(socket.socket(socket.AF_INET, socket.SOCK_STREAM), count)
        sock[count].sock.connect((HOST, PORT))
        count += 1
        print("connected")
        return flask.render_template("./index.html", count = count-1)
    except Exception as e:
        print(e)
        return flask.render_template("./ConnectFail.html")

@app.route("/setname/<count>/<name>")
def setname(count, name):
    global sock
    count = int(count)
    sock[count].set_name(name)
    sock[count].sock.send(name.encode())
    return flask.jsonify({})

@app.route("/createRoom/<count>")
def createRoom(count):
    global sock
    count = int(count)
    sock[count].sock.send("CreAteROoM@798199899".encode())
    room = sock[count].sock.recv(1024).decode()
    sock[count].set_room(room)
    return flask.jsonify({"msg" : room})

@app.route("/EnterExistingRoom/<count>/<room>")
def EnterExistingRoom(count, room):
    global sock
    count = int(count)
    sock[count].sock.send(f"{room}".encode())
    room = sock[count].sock.recv(1024).decode()
    sock[count].set_room(room)
    return flask.jsonify({"msg" : room})

@app.route("/msg/<count>")
def recive(count):
    print("tring to recive")
    try:
        msg = sock[int(count)].sock.recv(2048).decode()
        msg = {"msg": msg}
        return flask.jsonify(msg)
    except:
        return flask.jsonify({"msg" : ""})

@app.route("/sendmsg/<count>/<msg>")
def send(msg, count):
    global sock
    count = int(count)
    sock[count].sock.send(f"{msg} {sock[count].room}".encode())
    return flask.jsonify({"msg" : msg})

if __name__ == "__main__":
    app.run(host="", port=9999, debug=True)