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
        return self.MW

    def getFlow(self):
        return self.flow

    def getStatus(self):
        for generator, values in generator_data.items():
            print("Generator", values['name'], 'is on:', values['status'], " MW are:", values['MW'], ' Flow is:', values['flow'])

    def setPowerPlant(self, MW):                
        for generator, values in generator_data.items():
            MW = int(MW)
            setpoint = values['highLimit']
            lowLimit = values['lowLimit']
            if generator not in clientDict:
                continue
            client = clientDict[generator]
            if MW <= 0:
                client.send(('setpoint ' + str(0)).encode())
                print("Setting " + generator + " to: " + str(0))
                continue
            elif MW < setpoint and MW > lowLimit:
                setpoint = MW
            elif MW < setpoint and MW < lowLimit:
                setpoint = lowLimit
            if not values['status']:
                client.send('turn on'.encode())
                print("Turning on: " + generator)
            client.send(('setpoint ' + str(setpoint)).encode())
            print("Setting " + generator + " to: " + str(setpoint))
            MW -= int(setpoint)


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
               'exit:':'Closes all connections and disconnects the server',
               'total:':'Returns the total MW and Flow of the plant.'}

hydro = PowerPlant()

def command_thread():
    while(True):
        command = input('>>')
        if command == "help":
            for order, description in commandList.items():
                print(order, description)
        if "set" in command:
            try:
                parameters = command.split()
                generator = parameters[1]
                setpoint = parameters[2]
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
            generator = command[11:]
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
            if generator in clientDict.keys():
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
        if command == 'total':
            hydro.setTotalFlow()
            hydro.setTotalMW()
            print('The total MW generator for the plant is: ' + str(hydro.getMW()))
            print('The total Flow for the plant is: ' + str(hydro.getFlow()))
        

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

def new_power_authority(clientsocket,addr, name):
    while name in clientDict:
        msg = clientsocket.recv(1024)
        if not msg:
            break
        msg = msg.decode("utf-8")
        try:
            msg = json.loads(msg)
        except ValueError as e:
            if msg == "status":
                hydro.setTotalFlow()
                hydro.setTotalMW()
                output = (hydro.getMW(), hydro.getFlow())
                clientsocket.send(json.dumps(output).encode())
            elif 'set' in msg:
                paramaters = msg.split()
                hydro.setPowerPlant(paramaters[1])
            else:
                print(msg)
    clientsocket.close()
    print('Disconnecting from', name)
    if name in clientDict:
        del clientDict[name]


def listen_thread():
    while(True):
        try:
            conn, addr = s.accept()
            msg = conn.recv(1024)
            name = msg.decode()
            if name in clientDict:
                print(name, " is already connected!")
                conn.close()
            elif name in generatorList and name not in clientDict:
                clientDict[name] = conn
                print(name, " has connected from ", addr)
                conn.send("connected".encode())
                threading.Thread(target=new_client, args=(conn, addr, name)).start()
            elif name == "Power Authority" and name not in clientDict:
                clientDict[name] = conn
                print(name, " has connected from ", addr)
                conn.send("connected".encode())
                threading.Thread(target=new_power_authority, args=(conn, addr, name)).start()
            else:
                print("A non generator tried to connect: ", name)
                conn.close()
        except OSError as e:
            pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = int(1937)
s.bind((host, port))

s.listen(5)
commandThread = threading.Thread(target=command_thread)
commandThread.start()

listeningThread = threading.Thread(target=listen_thread)
listeningThread.setDaemon(True)
listeningThread.start()


print("Power plant started")


