import socket
import sys
from generator import Generator
import json
import threading
import time
import errno

generatorOne = Generator(name = sys.argv[3])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    global s
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

value = (generatorOne.on)


def sendUpdate():
    while(s):
        try:
            if not connectionFlag:
                print('breaking')
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
        if msg == 'shutOff':
            generatorOne.shutDown()
            print("Shutting down generator from server.")
        if msg == 'turn on':
            generatorOne.startup()
            print("Turning on from server.")
        if msg[:8] == 'setpoint':
            setpoint = int(msg[9:])
            old_out = sys.stdout
            new_out = stdout_(s)
            sys.stdout = new_out    
            generatorOne.set_setpoint(setpoint)
            sys.stdout = old_out
        if msg[:4] == 'send':
            print(msg[4:])
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
            connectionFlag = True
            connect()
        elif command == 'connect' and connectionFlag == True:
            print('already connected')
        if command == "status":
            print(generatorOne.report())
        if "change port" in command:
            sys.argv[2] = int(command[12:])
            print('changing port to ' + command[12:])


connectionFlag = False

commandThread = threading.Thread(target=command_thread)
commandThread.start()

print("Generator is on and running")
