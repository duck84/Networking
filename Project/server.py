import socket
import sys
import json
import threading

clientDict = {}

class PowerPlant():
    def __init__(self):
        self.MW = 0
        self.flow = 0
        self.head = 0

    def setTotalMW(self):
        new_total = 0
        for generator, values in generator_data.items():
            new_total += int(values["MW"])
        self.MW = new_total

    def setTotalFlow(self):
        new_total = 0
        for generator, values in generator_data.items():
            new_total += int(values["flow"])
        self.flow = new_total
    
    def getMW(self):
        print('MW: ', self.MW)

    def getFlow(self):
        print('Flow: ', self.flow)

    def getStatus(self):
        for generator, values in generator_data.items():
            print("Unit: ", values['name'], 'is on: ', values['status'])



generatorList = ['Generator1','Generator2','Generator3',
                 'Generator4','Generator5','Generator6',
                 'Generator7','Generator8','Generator9',
                 'Generator10']

generator_data = {}

hydro = PowerPlant()

def command_thread():
    while(True):
        command = input('>>')
        if command == "set":
            hydro.setTotalMW()
            hydro.setTotalFlow()
        if command == "status":
            hydro.getStatus()
        if command == "get":
            hydro.setTotalMW()
            hydro.setTotalFlow()
            hydro.getMW()
            hydro.getFlow()
        if command == "send":
            for keys, connects in clientDict.items():
                connects.send("Test message!".encode())
        if "exit" in command:
            generator = command[5:]
            if generator in generatorList:
                print('Removing: ', generator)
                clientDict[generator].shutdown(socket.SHUT_RDWR)
                clientDict[generator].close()
                del clientDict[generator]
            else:
                clients = list(clientDict.keys())
                print("Please select a generator currently connected: ", clients)
        if "shut off" in command:
            generator = command[9:]
            if generator in generatorList:
                print('Shutting down: ', generator)
                client = clientDict[generator]
                client.send('shutOff'.encode())
            else:
                clients = list(clientDict.keys())
                print("Please select a generator currently connected: ", clients)
        if "turn on" in command:
            generator = command[8:]
            if generator in generatorList:
                print('Turning on: ', generator)
                client = clientDict[generator]
                client.send('turn on'.encode())
            else:
                clients = list(clientDict.keys())
                print("Please select a generator currently connected: ", clients)
        if command == "power down":
            print("Shutting down the Plant")
            for generator, values in generator_data.items():
                clientDict[generator].shutdown(socket.SHUT_RDWR)
                clientDict[generator].close()
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            break
        

def new_client(clientsocket,addr, name):
    while name in clientDict:
        msg = clientsocket.recv(1024)
        if not msg:
            break
        msg = msg.decode("utf-8")
        msg = json.loads(msg)
        generator_data[name] = msg
    clientsocket.close()
    print('Removing ', name, ' from generator data')
    del generator_data[name]

def listen_thread():
    while(True):
        try:
            conn, addr = s.accept()
            msg = conn.recv(1024)
            name = msg.decode()
            if name in generatorList and name not in clientDict:
                clientDict[name] = conn
                print(name, " has connected from ", addr)
                conn.send("Connection to Power Plant".encode())
                threading.Thread(target=new_client, args=(conn, addr, name)).start()
            elif name in clientDict:
                print(name, " is already connected!")
                conn.close()
            else:
                print("A non generator tried to connect: ", name)
                conn.close()
        except OSError as e:
            pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = int(sys.argv[1])
s.bind((host, port))

s.listen(5)
commandThread = threading.Thread(target=command_thread)
commandThread.start()

listeningThread = threading.Thread(target=listen_thread)
listeningThread.setDaemon(True)
listeningThread.start()


#while(True):
#    conn, addr = s.accept()
#    msg = conn.recv(1024)
#    name = msg.decode()
#    if name in generatorList and name not in clientDict:
#        clientDict[name] = conn
#        print(name, " has connected from ", addr)
#        conn.send("Connection to Power Plant".encode())
#        threading.Thread(target=new_client, args=(conn, addr, name)).start()
#    elif name in clientDict:
#        print(name, " is already connected!")
#        conn.close()
#    else:
#        print("A non generator tried to connect: ", name)
#        conn.close()


print("Ending Program")


