import socket
import sys
from generator import Generator
import json
import threading
import time
import errno

generatorOne = Generator(name = sys.argv[3])

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
        s.send(('Generator' + sys.argv[3]).encode())

        listenThread = threading.Thread(target=receiveData)
        listenThread.setDaemon(True)
        listenThread.start()

        updateThread = threading.Thread(target=sendUpdate)
        updateThread.setDaemon(True)
        updateThread.start()

    except ConnectionRefusedError as e:
        print("Trying to connect on: ", port, "make sure the port is 1937 and server is running" )
        connectionFlag = False

value = (generatorOne.on)

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
        try:
            data = s.recv(1024)
        except OSError as e:
            break
        if not data:
            break
        msg = data.decode()
        parameters = msg.split()
        if parameters[0] == 'shutOff':
            old_out = sys.stdout
            new_out = stdout_(s)
            sys.stdout = new_out    
            generatorOne.shutDown()
            sys.stdout = old_out
            print("Shutting down generator from server.")
            s.send(("Generator" + sys.argv[3] + " is turned off.").encode())            

        if parameters[0] == 'turnOn':
            old_out = sys.stdout
            new_out = stdout_(s)
            sys.stdout = new_out
            generatorOne.startup()    
            sys.stdout = old_out
            print("Turning on from server.")

        if parameters[0] == 'setpoint':
            setpoint = int(parameters[1])
            print("Setting the unit's setpoint to:", setpoint)
            old_out = sys.stdout
            new_out = stdout_(s)
            sys.stdout = new_out    
            generatorOne.set_setpoint(setpoint)
            sys.stdout = old_out
            generatorOne.set_setpoint(setpoint)

        if msg[:4] == 'send':
            print(msg[4:])

        if msg == 'Already connected':
            print(msg)

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
            try:
                s.shutdown(socket.SHUT_RDWR)
                s.close()
            except OSError as e:
                pass
        if command == 'connect':
            connect()
        if command == "status":
            print(generatorOne.report())
            print("Connected to master station:", connectionFlag)
        if "change port" in command:
            sys.argv[2] = int(command[12:])
            print('changing port to ' + command[12:])


connectionFlag = False

commandThread = threading.Thread(target=command_thread)
commandThread.start()

print("Generator is on standby")
