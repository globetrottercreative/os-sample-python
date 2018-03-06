import socket
import threading
import os

from flask import Flask
application = Flask(__name__)

@application.route("/")
def GetFile(name, sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        sock.send(bytes("EXISTS" + str(os.path.getsize(filename)), 'utf-8'))
        userResponse = sock.recv(1024)
        if userResponse[:2].decode('utf-8') == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send(bytes("ERR", 'utf-8'))
    sock.close()

def Main():
    s = socket.socket()
    host = socket.gethostname()
    port = 8080
    s.bind((host, port))
    s.listen(5)
    print("Server Started.")
    while True:
        c, addr = s.accept()
        print("Client Connected: " + str(addr))
        t = threading.Thread(target=GetFile, args=("retrThread", c))
        t.start()
    s.close()
    
if __name__ == "__main__":
    application.run()
