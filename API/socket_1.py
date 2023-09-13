import socket
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import threading 

path = "../../704/Project1/input.txt"

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
    try:
        clientSocket.connect(("127.0.0.1",1234))
    except:
        return 'issue connecting socket'
    try:
        response = int(clientSocket.recv(1024).decode())
        print(response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    webPosJsonData = request.json

    clientSocket.close()

    if A.busy:
        return 'BUSY'

    A.busy = True
    A.current = 0
    A.orderN = webPosJsonData['number']

    with open(path, 'w') as file:
        file.write(str(webPosJsonData['liquid1']) + "," + str(webPosJsonData['liquid2']) + "," + str(webPosJsonData['liquid3']) + "," + str(webPosJsonData['liquid4']))

    for i in range(0,webPosJsonData['number'],1):
        holder.append(i)
    time_task = threading.Thread(target=sendit)
    time_task.start()

    return 'Submitted!'

def sendit():
    while len(holder) > 0:
        for e in holder:
            #maybe should add some error handling
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect(("127.0.0.1",1234))
            try:
                response = int(clientSocket.recv(1024).decode())
                print("got response : " + str(response))
                if (response == 1) or (response == 2): 
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
            time.sleep(0.01)

    A.current -= 1

    # wait for last
    exitTrigger = False
    while not exitTrigger:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect(("127.0.0.1",1234))
            try:
                response = int(clientSocket.recv(1024).decode())
                print("got response : " + str(response))
                if response == 2: 
                    A.current += 1
                    exitTrigger = True
            except Exception as e:
                print(f"An error occurred: {str(e)}")

            clientSocket.close()
            time.sleep(0.1)

    #turn back to default values
    print("fill done")
    with open(path, 'w') as file:
        file.write('25,25,25,25')
    A.busy = False
    A.iterateFlag = True

app.run()
# clientSocket.send(data.encode())
# Send data to server
