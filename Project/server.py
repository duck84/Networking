import socket
import sys
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = int(sys.argv[1])
s.bind((host, port))

s.listen(1)
conn, addr = s.accept()
print('client is at ', addr)

data = conn.recv(1024)

print(json.loads(data.decode()))
conn.send(data)
conn.close()


