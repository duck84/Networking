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

def receiveData():
    while s:
        data = s.recv(1024)
        if not data:
            break
        msg = data.decode()
        if msg == 'shutOff':
            generatorOne.shutDown()
        if msg == 'turn on':
            generatorOne.startup()
        if msg[:8] == 'setpoint':
            setpoint = int(msg[9:])
            generatorOne.set_setpoint(setpoint)
        if msg[:4] == 'send':
            print(msg[5:])
    print("Closing the connection")
    s.close()

def command_thread():
    while(True):
        command = input('>>')
        if "send" in command:
            s.send(command[5:].encode())
        if command == "disconnect":
            connectionFlag = False
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        if command == 'connect':
            connectionFlag = True
            connect()
        if command == "status":
            print(generatorOne.report())


connectionFlag = True

commandThread = threading.Thread(target=command_thread)
commandThread.start()

print("Generator is on and running")
