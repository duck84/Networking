import socket
import sys
from generator import Generator
import json
import threading
import time
import errno

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = sys.argv[1]
port = int(sys.argv[2])

def connect():
    global s
    global connectionFlag
    
    connectionFlag = True

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = sys.argv[1]
        port = int(sys.argv[2])
        s.connect((host, port))
        s.send(('Power Authority'.encode()))

        listenThread = threading.Thread(target=receiveData)
        listenThread.setDaemon(True)
        listenThread.start()

#        updateThread = threading.Thread(target=sendUpdate)
#        updateThread.setDaemon(True)
#        updateThread.start()

    except ConnectionRefusedError as e:
        print("Trying to connect on: ", port, "make sure the port is 1937 and server is running" )
        connectionFlag = False




def sendUpdate():
    while(s):
        try:
            if not connectionFlag:
                break
            output = generatorOne.report()
            s.send(json.dumps(output).encode())
            time.sleep(1)
        except socket.error as e:
            if e == errno.EPIPE:
                print("Disconnected from server")
            break
    print("No longer sending updates")

class stdout_():

    def __init__(self, sock_resp):
        self.sock_resp = sock_resp

    def write(self, mes):
        self.sock_resp.send(mes.encode())

def receiveData():
    while s:
        data = s.recv(1024)
        if not data:
            break
        msg = data.decode()

        try:
            msg = json.loads(msg)
            print('Total MW at the plant are: ' + str(msg[0]))
            print('Total Flow at the plant are: ' + str(msg[1]))
        except ValueError as e:           
            if msg[:4] == 'send':
                print(msg[4:])
            if msg == 'connected':
                print('Connected to master station on', host, port)

    print("Closing the connection")
    s.close()
    global connectionFlag
    connectionFlag = False



def command_thread():
    global connectionFlag
    while(True):
        command = input('>>')
        if "send" in command:
            s.send(command[5:].encode())
        if command == "disconnect":
            connectionFlag = False
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        if command == 'connect' and connectionFlag == False:
            connect()
        elif command == 'connect' and connectionFlag == True:
            print('already connected')
        if command == "status":
            print("Getting report from power plant.")
            s.send(command.encode())
        if "change port" in command:
            sys.argv[2] = int(command[12:])
            print('changing port to ' + command[12:])
        if "set" in command:
            s.send(command.encode())


connectionFlag = False

commandThread = threading.Thread(target=command_thread)
commandThread.start()

print("Connected to Power Plant.")
