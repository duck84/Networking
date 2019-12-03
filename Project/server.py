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
            print("Generator", values['name'], 'is on:', values['status'], " MW are:", values['MW'], ' Flow is:', values['flow'])



generatorList = ['Generator1','Generator2','Generator3',
                 'Generator4','Generator5','Generator6',
                 'Generator7','Generator8','Generator9',
                 'Generator10']

generator_data = {}

commandList = {'set:':"Sends a setpoint to a generator",
               'status:':'Returns the status of all the generators',
               'send:':'Sends a message to the generator',
               'disconnect:':'Disconnects a generator',
               'shut off:':'Turns a generator off',
               'turn on:':'Turns a generator on',
               'power down:':'Powers down the power plant',
               'exit':'Closes all connections and disconnects the server'}

hydro = PowerPlant()

def command_thread():
    while(True):
        command = input('>>')
        if command == "help":
            for order, description in commandList.items():
                print(order, description)
        if "set" in command:
            try:
                generator = command[4:14]
                setpoint = int(command[15:])
            except:
                print("Input error with command. Please enter set <Generator#> <setpoint>")
            if generator in clientDict:
                print("Setting ", generator, " to ", setpoint)
                client = clientDict[generator]
                client.send(('setpoint ' + str(setpoint)).encode())
            else:
                clients = list(clientDict.keys())
                print("Please select a generator currently connected: ", clients)
        if command == "status":
            hydro.getStatus()
        if "send" in command:
            for keys, connects in clientDict.items():
                connects.send(command.encode())
        if "disconnect" in command:
            generator = command[5:]
            if generator in clientDict:
                print('Removing: ', generator)
                clientDict[generator].shutdown(socket.SHUT_RDWR)
                clientDict[generator].close()
                del clientDict[generator]
            else:
                clients = list(clientDict.keys())
                print("Please select a generator currently connected: ", clients)
        if "shut off" in command:
            generator = command[9:]
            if generator in clientDict:
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
        if command == "exit":
            print("Shutting down the Plant")
            for generator, values in generator_data.items():
                clientDict[generator].shutdown(socket.SHUT_RDWR)
                clientDict[generator].close()
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            break
        if "power down" in command:
            for generator, values in generator_data.items():
                print('Shutting down: ', generator)
                client = clientDict[generator]
                client.send('shutOff'.encode())
        

def new_client(clientsocket,addr, name):
    while name in clientDict:
        msg = clientsocket.recv(1024)
        if not msg:
            break
        msg = msg.decode("utf-8")
        try:
            msg = json.loads(msg)
        except ValueError as e:
            print(msg)
        generator_data[name] = msg
    clientsocket.close()
    print('Removing ', name, ' from generator data')
    del generator_data[name]
    if name in clientDict:
        del clientDict[name]

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


print("Power plant started")


