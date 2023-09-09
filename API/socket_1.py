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
    iterateFlag = True

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
    if A.busy:
        return 'BUSY'

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("127.0.0.1",1234))
    try:
        response = int(clientSocket.recv(1024).decode())
        print(response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    a = request.json

    clientSocket.close()

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
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect(("127.0.0.1",1234))
            try:
                response = int(clientSocket.recv(1024).decode())
                if response == 0 and A.iterateFlag:
                    A.iterateFlag = False
                    clientSocket.send(b"newBottle")
                    print(e)
                    print(holder)
                    holder.pop(0)
                    A.current = A.orderN - len(holder)
                if response != 0:
                    A.iterateFlag = True

            except Exception as e:
                print(f"An error occurred: {str(e)}")

            clientSocket.close()
            time.sleep(1)
    A.busy = False
    A.iterateFlag = True

app.run()
# clientSocket.send(data.encode())
# Send data to server
