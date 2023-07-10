import socket
# import threading
import subprocess
import flask

class Sock:

    def __init__(self, sock, count) -> None:
        self.sock = sock
        self.count = count

app = flask.Flask(__name__, template_folder='template', static_folder='static')
sock = {}
count = 0
# out = subprocess.getoutput("ipconfig").split("\n")
# for i in out:
#     if(i.strip().startswith("IPv4")):
#         out = i
#         break

HOST = "127.0.0.1"  # localhost
# HOST = out.split()[-1]    # ip address of pc
PORT = 9090

@app.route("/")
@app.route("/chat")
def home():
    global sock, count
    exit = False

    sock[count] = Sock(socket.socket(socket.AF_INET, socket.SOCK_STREAM), count)
    sock[count].sock.connect((HOST, PORT))
    count += 1
    print("connected")

    print(sock)
    return flask.render_template("./client.html", count = count-1)

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
    print("message is :", msg)
    sock[int(count)].sock.send(msg.encode())
    return msg

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=True)