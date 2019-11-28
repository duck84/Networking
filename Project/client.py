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
s.connect((host, port))
s.send(('Generator' + sys.argv[3]).encode())

value = (generatorOne.on)
generatorOne.startup()
generatorOne.set_setpoint(50)


def sendUpdate():
    while(True):
        try:
            output = generatorOne.report()
            s.send(json.dumps(output).encode())
            time.sleep(1)
        except socket.error as e:
            if e == errno.EPIPE:
                print("Disconnected from server")

def receiveData():
    while True:
        data = s.recv(1024)
        if not data:
            break
        msg = data.decode()
        if msg == 'shutOff':
            generatorOne.shutDown()
        if msg == 'turn on':
            generatorOne.startup()
    print("Closing the connection")
    s.close()


updateThread = threading.Thread(target=sendUpdate)
updateThread.setDaemon(True)
updateThread.start()

listenThread = threading.Thread(target=receiveData)
listenThread.start()

time.sleep(30)
generatorOne.set_setpoint(0)
