import socket
import os
from threading import Thread

class Proxy2Server(Thread):
    def __init__(self, host, port):
        super(Proxy2Server, self).__init__()
        self.client = None
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
    
    def run(self):
        while True:
            data = self.client.recv(2048)
            if data:
                self.client.sendall(data)

class Client2Proxy(Thread):
    def __init__(self, host, port):
        super(Client2Proxy, self).__init__()
        self.client = None
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host,port))
        sock.listen(1)
        self.client, addr = sock.accept()
    
    def run(self):
        while True:
            data = self.client.recv(2048)
            if data:
                self.client.sendall(data)
            
class Proxy(Thread):
    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__()   
        self.from_host = from_host
        self.to_host = to_host
        self.port = port

    def run(self):
        while True:
            print(f"[proxy({self.port})] Setting Up")
            self.c2p = Client2Proxy(self.from_host, self.port)
            self.p2s = Proxy2Server(self.to_host, self.port)
            print(f"[proxy({self.port})] Connection Established")
            self.c2p.server = self.p2s.server
            self.p2s.client = self.c2p.client

            self.c2p.start()
            self.p2s.start()

main_server = Proxy('0.0.0.0', '127.0.0.1', 2344)
main_server.start()

for port in range(3000,3006):
    client_server = Proxy('0.0.0.0', '127.0.0.1', port)
    client_server.start()
