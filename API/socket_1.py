import socket
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/newBot", methods=['POST'])
def sendNewBottle():
    print("trest")  
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("127.0.0.1",1234))
    data = "Hello Server!"
    print("trest")  
    print(request.data)
    clientSocket.send(bytes(request.data))
    return 'Submitted!'


app.run()
# clientSocket.send(data.encode())
# Send data to server
