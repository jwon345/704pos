import socket
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import threading 


app = Flask(__name__)
CORS(app)

holder = []
class A:
    current = 0
    orderN = 0
    busy = False

# @app.route("/Status", methods=['GET'])
#     def theStatus():
        
@app.route("/Status", methods=['GET'])
def getStatus():
    if A.orderN == 0:
        return "System Ready"
    if A.current == A.orderN:
        return "Done " + str(A.current) + " of " + str(A.orderN) + " - System Ready" 
    else:
        return "Progress " + str(A.current) + " of " + str(A.orderN) + " - System Busy"

@app.route("/newBot", methods=['POST'])
def sendNewBottle():
    print("trest")  
    # clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # clientSocket.connect(("127.0.0.1",1234))
    data = "Hello Server!"
    print("trest")  
    print(request.json)
    a = request.json
    # clientSocket.send(bytes(request.data))

    if A.busy:
        return 'BUSY'

    A.busy = True
    A.current = 0
    A.orderN = a['number']
    for i in range(0,a['number'],1):
        holder.append(i)
    time_task = threading.Thread(target=sendit)
    time_task.start()

    return 'Submitted!'

def sendit():
    while len(holder) > 0:
        for e in holder:
            time.sleep(1)
            print(e)
            print(holder)
            holder.pop(0)
            A.current = A.orderN - len(holder)
    A.busy = False

app.run()
# clientSocket.send(data.encode())
# Send data to server
