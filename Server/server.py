import socket
import threading
import logger
import sys
import time
from client_data import client_data 
from singleton import singleton

class chat_server(metaclass = singleton):
    def __init__(self):
        self.logger = logger.logger()
        self.HOST, self.PORT = "localhost", 9999
        self.MAX_USERS = 20
        self.socket = socket.socket()
        self.socket.bind((self.HOST,self.PORT))
        self.client_list = {}
        self.running = True
    def terminate(self):
        pass
    def listen(self):
        self.socket.listen(self.MAX_USERS)
        while True:
            conn, addr = self.socket.accept()
            conn.settimeout(60)
            identifier = hash(conn)
            self.logger.log('New connection from '+str(addr))
            thread = threading.Thread(target = self.listen_to_client,args = (conn,addr,identifier), daemon=True).start()
            self.client_list[identifier] = client_data(conn,addr,thread)
    def broadcast_to_all(self, data):
        for identifier in self.client_list:
            self.logger.log('Sending data to '+str(self.client_list[identifier]._addr))
            self.client_list[identifier]._conn.send(data)
    def process_command(self,client,command):
        if command.startswith('/LIST'):
            self.logger.log('LIST command acquired')
            for identifier in self.client_list:
                print('ID: '+str(identifier)+', ADDR: '+str(self.client_list[identifier]._addr))
                data_to_send = 'ID: '+str(identifier)+', ADDR: '+str(self.client_list[identifier]._addr)
                client.send(data_to_send.encode('UTF-8'))
        elif command.startswith('/TERMINATE'):
            client.send(b'Server termination imminent')
            self.terminate()
        else:
            client.send(b'UNKNOWN COMMAND')
    def listen_to_client(self, client, address, identifier):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    if data[0]==47:
                        self.logger.log('Received command from '+str(address))
                        self.process_command(client,data.decode('utf-8'))
                    else:
                        self.logger.log('Received data from '+str(address))
                        self.broadcast_to_all(data)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                self.logger.log('Client '+str(address)+' disconnected')
                del self.client_list[identifier]
                return False

server = chat_server()
server.listen()
