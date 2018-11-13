import socket
import threading
import logger
import sys
import time
from client_data import client_manager
from user_manager import user_manager
from singleton import singleton

class chat_server(metaclass = singleton):
    def __init__(self):
        self.logger = logger.logger()
        self.HOST, self.PORT = "localhost", 9999
        self.MAX_USERS = 20
        self.socket = socket.socket()
        self.socket.bind((self.HOST,self.PORT))
        self.client_manager = client_manager()
        self.user_manager =user_manager()
        self.running = True

    def terminate(self):
        pass

    def listen(self):
        self.socket.listen(self.MAX_USERS)
        while True:
            conn, addr = self.socket.accept()
            conn.settimeout(60)
            self.logger.log('New connection from '+str(addr))
            identifier = self.client_manager.add_user(conn,addr)
            thread = threading.Thread(target = self.listen_to_client, args = (identifier,), daemon=True).start()

    def broadcast_to_all(self, data):
        for identifier in self.client_manager:
            self.logger.log('Sending data to '+str(self.client_manager[identifier]._addr))
            self.client_manager[identifier]._conn.send(data)

    def process_command(self,identifier,command):
        client = self.client_manager[identifier]._conn
        if command.startswith('/LIST'):
            self.logger.log('LIST command acquired')
            for identifier in self.client_manager:
                print('ID: '+str(identifier)+', ADDR: '+str(self.client_manager[identifier]._addr))
                data_to_send = 'ID: '+str(identifier)+', ADDR: '+str(self.client_manager[identifier]._addr)
                client.send(data_to_send.encode('UTF-8'))
        elif command.startswith('/TERMINATE'):
            client.send(b'Server termination imminent')
            self.terminate()
        elif command.startswith('/LOGIN'):
            self.login_client(identifier)
        else:
            client.send(b'UNKNOWN COMMAND')

    def listen_to_client(self, identifier):
        size = 1024
        client = self.client_manager[identifier]._conn
        address = self.client_manager[identifier]._addr
        while True:
            try:
                data = client.recv(size)
                if data:
                    if data[0]==47:
                        self.logger.log('Received command from '+str(address))
                        self.process_command(identifier,data.decode('utf-8'))
                    else:
                        self.logger.log('Received data from '+str(address))
                        self.broadcast_to_all(data)
                else:
                    raise error('Client disconnected')
            except error:
                client.close()
                self.logger.log('Client '+str(address)+' disconnected')
                self.client_manager.remove_user(identifier)
                return False
    def login_client(self,identifier):
        size = 1024
        socket = self.client_manager[identifier]._conn
        socket.send(b'Enter login')
        login = socket.recv(size)
        if self.user_manager.user_exists(login):
            salt = self.user_manager[login]._salt
            socket.send(salt.encode('UTF-8'))
            password = socket.recv(size)
            if self.user_manager.validate_user(login,password):
                self.client_manager[identifier]._user = login
            else:
                socket.send(b'Wrong password')
        else:
            socket.send(b'User not found. Create new user [Y/N]?')
            answer = socket.recv(size).decode('UTF-8').upper()
            if answer=='Y':
                salt = self.user_manager.add_user(login)
                socket.send(salt.encode('UTF-8'))
                socket.send(b'Enter password')
                password = socket.recv(size)
                self.user_manager.set_user_password(login,password)
                self.client_manager[identifier]._user = login
                socket.send(b'Login succesful')
            else:
                return


server = chat_server()
server.listen()
