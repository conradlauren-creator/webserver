# Project: Web Server
# Group: Lauren Conrad, Hudson Cho
# Class: COSC-350-001

# for testing: http://localhost:50000/index.txt

from pathlib import Path
from datetime import datetime, timezone
import socket
import sys
import os

class HTTPServer:
    MAX_CONCURRENT_CONNECTIONS = 5
    HOST = None               # Symbolic name meaning all available interfaces
    PORT = 50000              # Arbitrary non-privileged port
    s = None
    server_root = "server_files"

    def main():
        for res in socket.getaddrinfo(HTTPServer.HOST, HTTPServer.PORT, socket.AF_UNSPEC,
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
            sys.exit(HTTPServer.MAX_CONCURRENT_CONNECTIONS)
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


                    stripped_path = path.lstrip("/")
                    full_path = os.path.join(HTTPServer.server_root, stripped_path)

        #FEATURE: Secure directory so that users cannot access elements outside the servers files            
                
                # FORBIDDEN: 403 ERROR
                    if "..\\" in path or "../" in path:
                        print("403 Forbidden")
                        firstLine = "403 Forbidden"
                        response = HTTPServer.responses(firstLine, "")
                        
                #˙⊹° GET.°⊹˙⋆🖳₊˚⊹.
                    elif method == 'GET':
                        if os.path.exists(full_path):
                            body = Path(full_path).read_text()

                            firstLine = "200 OK"
                            response = HTTPServer.responses(firstLine, body)

                        else:
                            #note: it's prob always gonna produce a 404 error for favicon since we don't have one
                            print(full_path, " was expected but couldn't be found.\n")
                            firstLine = "404 Not Found"
                            response = HTTPServer.responses(firstLine, "")
                            

                #˙⊹° HEAD.°⊹˙⋆🖳₊˚⊹.
                    elif method == 'HEAD':
                        if os.path.exists(full_path):
                            body = Path(full_path).read_text()

                            firstLine = "200 OK"
                            response = HTTPServer.responses(firstLine, "")

                        else:
                            print(full_path, " was expected but couldn't be found.")
                            firstLine = "404 Not Found"
                            response = HTTPServer.responses(firstLine, "")

                # NEITHER: 501 ERROR
                    else:
                        print("501 Not Implemented")
                        firstLine = "501 Not Implemented"
                        response = HTTPServer.responses(firstLine, "")

                    #responses shared by all 
                    print(raw_http_request)
                    conn.send(response.encode('utf-8'))

        except Exception as e:
            print("Error:", e)




    #new method starts here and includes this
    def responses(pFirstLine, pBody):

        date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

        return (
            f"HTTP/1.1 {pFirstLine}\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {len(pBody)}\r\n"
            f"Server: HudsonAndLaurensServer\r\n"
            f"Date: {date}\r\n"
            f"\r\n"
            f"{pBody}"
            )
    

HTTPServer.main()