import socket
import sys
from generator import Generator
import json

generatorOne = Generator()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = sys.argv[1]
port = int(sys.argv[2])
s.connect((host, port))

#output = sys.argv[3]
value = (generatorOne.on)

if(value):
    output = "True"
else:
    output = "False"

output = generatorOne.report()

s.send(json.dumps(output).encode())

i = 0
while(1):
    data = s.recv(1024)
    i += 1
    if (i < 5):
        print(data)
    if not data:
        break
    print('received ', len(data), " bytes" )

s.close