import socket
import threading
import logger
import sys
import time
from client_manager import client_manager
from user_manager import user_manager
from singleton import singleton
from telegram_parser import telegram, telegram_parser

class chat_server(metaclass = singleton):

    def __init__(self):
        self.logger = logger.logger()
        self.HOST, self.PORT = "localhost", 9999
        self.MAX_USERS = 20
        self.socket = socket.socket()
        self.socket.bind((self.HOST,self.PORT))
        self.client_manager = client_manager()
        self.user_manager =user_manager()
        self.parser = telegram_parser()
        self.running = True
        self.termination_in_progress = False
        self.listen_thread = 0 
        self.wathcdog_thread = threading.Thread(target = self.watchdog_function, args = (), daemon=True).start()

    def watchdog_function(self):
        while True:
            if self.termination_in_progress:
                self.terminate_chat_server()
                break;
            time.sleep(1)

    def terminate_chat_server(self):
        self.client_manager.terminate_all_connections()
        self.socket.close()
        self.logger.log('Connection termination complete')

    def listen_thread_function(self):
        self.socket.listen(self.MAX_USERS)
        while True:
            try:
                conn, addr = self.socket.accept()
                conn.settimeout(60)
                self.logger.log('New connection from '+str(addr))
                identifier = self.client_manager.add_user(conn,addr)
                thread = threading.Thread(target = self.listen_to_client, args = (identifier,), daemon=True).start()
            except:
                self.logger.log('Listen cycle interruption')
                break     

    def terminate(self):
        self.logger.log('Terminating sequence initated')
        self.termination_in_progress = True

    def listen(self):
        self.listen_thread = threading.Thread(target = self.listen_thread_function(), args = (), daemon=True).start()

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
                    received_telegram = self.parser.parse_telegram(data.decode('UTF-8'))
                    if received_telegram.header=='#MSG':
                        if received_telegram.message[0] == '/':
                            self.logger.log('Received command from '+str(address))
                            self.process_command(identifier,data.decode('utf-8'))
                        else:
                            self.logger.log('Received message from '+str(address))
                            self.broadcast_to_all(data)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                self.logger.log('Client '+str(address)+' disconnected')
                if not self.termination_in_progress:
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
