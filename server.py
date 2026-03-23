# Skeleton program
import socket
import sys
import os

MAX_CONCURRENT_CONNECTIONS = 5
HOST = None               # Symbolic name meaning all available interfaces
PORT = 50000              # Arbitrary non-privileged port
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(sa)
        s.listen(6)
        print('Server is running. Waiting for connection...')
    except OSError as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(MAX_CONCURRENT_CONNECTIONS)
conn, addr = s.accept()
try:
    with conn:
        print('Connected by', addr)
        i = 0
        while (i < 10): #True:
            http_request = conn.recv(1024).decode('utf-8', errors='ignore')


            if not http_request: break

            http_request.split();


            print("===== Raw HTTP Request ====")
            print(http_request)
            i = i + 1

except Exception as e:
    print("Error:", e)
