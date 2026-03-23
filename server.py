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
            raw_http_request = conn.recv(1024).decode('utf-8', errors='ignore')
            lines = raw_http_request.split('\r\n')

            http_request_line = lines[0] 

            method, path, version = http_request_line.split()
         
            headers = {}
            for line in lines[1:]:
                if (line == ""): #Empty line signifies end of headers section
                    break
                key, value = line.split(":", 1)
                key.split()
                value.split()
                headers[key] = value


                body = "BALLS" 

                # Full HTTP response
                response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"\r\n"
                    f"{body}"
                )

            conn.send(response.encode('utf-8'))

    


#FEATURE: Secure directory so that users cannot access elements outside the servers files

            i = i + 1

# Method get_response() -> returns replies with standarad http format



except Exception as e:
    print("Error:", e)
