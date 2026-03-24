# Skeleton program
# for testing: http://localhost:50000/index.txt

from pathlib import Path
from datetime import datetime, timezone
import socket
import sys
import os

MAX_CONCURRENT_CONNECTIONS = 5
HOST = None               # Symbolic name meaning all available interfaces
PORT = 50000              # Arbitrary non-privileged port
s = None
server_root = "server_files"

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
        while (True): 
            
            raw_http_request = conn.recv(1024).decode('utf-8', errors='ignore')
            if not raw_http_request:
                break

            lines = raw_http_request.split('\r\n')

            http_request_line = lines[0] 

            method, path, version = http_request_line.split()
         
            headers = {}
            for line in lines[1:]:
                if (line == ""): #Empty line signifies end of headers section
                    break
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                headers[key] = value


#FEATURE: Secure directory so that users cannot access elements outside the servers files

        

# Method get_response() -> returns replies with standarad http format

            stripped_path = path.lstrip("/")
            full_path = os.path.join(server_root, stripped_path)
            date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        #˙⊹° GET.°⊹˙⋆🖳₊˚⊹.
            if method == 'GET':
                if os.path.exists(full_path):

                    body = Path(full_path).read_text()
                    response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Server: HudsonAndLaurensServer\r\n"
                    f"Date: {date}\r\n"
                    f"\r\n"
                    f"{body}"
                    )

                else:
                    #note: it's always gonna produce a 404 error for favicon since we don't have one
                    print(full_path, " was expected but couldn't be found.")
                    response = (
                    f"HTTP/1.1 404 Not Found\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: 0\r\n"
                    f"Server: HudsonAndLaurensServer\r\n"
                    f"Date: {date}\r\n"
                    f"\r\n"
                    )

        #˙⊹° HEAD.°⊹˙⋆🖳₊˚⊹.
            elif method == 'HEAD':
                if os.path.exists(full_path):
                
                    body = Path(full_path).read_text()
                    response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    f"Server: HudsonAndLaurensServer\r\n"
                    f"Date: {date}\r\n"
                    f"\r\n"
                    )

                else:
                    print(full_path, " was expected but couldn't be found.")
                    response = (
                    f"HTTP/1.1 404 Not Found\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: 0\r\n"
                    f"Server: HudsonAndLaurensServer\r\n"
                    f"Date: {date}\r\n"
                    f"\r\n"
                    )

            else:
                print("501 Error: Not Implemented.")
                response = (
                f"HTTP/1.1 501 Not Implemented\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: 0\r\n"
                f"Server: HudsonAndLaurensServer\r\n"
                f"Date: {date}\r\n"
                f"\r\n"
                )

            print(raw_http_request)
            conn.send(response.encode('utf-8'))

except Exception as e:
   print("Error:", e)
