import socket
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import threading 

#Relative path to he Input.txt needed or liquid fill in Sysj 
path = "../../704/Project1/input.txt"

app = Flask(__name__)
CORS(app)

ff

holder = []
class A:
    current = 0
    orderN = 0
    busy = False
    iterateFlag = True

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
        return 'issue connecting socket' #send fail back
    try:
        response = int(clientSocket.recv(1024).decode())
        print(response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    #extract the request data
    webPosJsonData = request.json

    clientSocket.close()

    #cancel request retrun BUSY
    if A.busy:
        return 'BUSY'

    #effectively Else. -> sets to busy and starts the rocess
    A.busy = True
    A.current = 0
    A.orderN = webPosJsonData['number']

    #Write liquid numberse to .txt file as a cvs
    with open(path, 'w') as file:
        file.write(str(webPosJsonData['liquid1']) + "," + str(webPosJsonData['liquid2']) + "," + str(webPosJsonData['liquid3']) + "," + str(webPosJsonData['liquid4']))

    for i in range(0,webPosJsonData['number'],1):
        holder.append(i)

    #start thread to handle the 
    time_task = threading.Thread(target=sendit)
    time_task.start()

    return 'Submitted!'

def sendit():
    while len(holder) > 0:
        for e in holder:
            #maybe should add some error handling
            try:
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.connect(("127.0.0.1",1234))
                response = int(clientSocket.recv(1024).decode())
                print("got response : " + str(response))
                    # system is Busy
                if (response == 1) or (response == 2): 
                    A.iterateFlag = False
                    clientSocket.send(b"newBottle")
                    print(e)
                    print(holder)
                    holder.pop(0)
                    A.current = A.orderN - len(holder)
                if response != 0:
                    A.iterateFlag = True

            #Reset if fail
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                A.current = 0
                A.busy = False
                A.iterateFlag = False
                A.orderN = 0

            clientSocket.close()
            time.sleep(0.1)
    #scuffy logic to prevent premature exit
    A.current -= 1

    # wait for last bottle
    exitTrigger = False
    while not exitTrigger:
            time.sleep(0.25)
            try:
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.connect(("127.0.0.1",1234))
                response = int(clientSocket.recv(1024).decode())
                print("got response : " + str(response))
                # bottle not on conveyor
                if response == 2: 
                    A.current += 1
                    exitTrigger = True
            except Exception as e:
                print(f"An error occurred: {str(e)}")


            clientSocket.close()

    #turn back to default values
    print("fill done")
    with open(path, 'w') as file:
        file.write('25,25,25,25')
    A.busy = False
    A.iterateFlag = True

app.run()
