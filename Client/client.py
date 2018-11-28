import socket
import sys
import threading
import time
from telegram_parser import *
from telegram_generator import *

HOST, PORT = 'localhost', 9999
LOGIN_DELAY_SECONDS = 2
GUEST = 'UNLOGGED'
MSG = '#MSG'
LGN = '#LGN'



class client:
    def __init__(self,login):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection_online = False
        self._logged_in = False
        self._parser = telegram_parser()
        self._generator = telegram_generator()
        self._login = login
        self._visible_login = GUEST
        self._mode = 'broadcast'
        self._override_communication = threading.Lock()
        self.list_of_client_commands = {'PRIVATE':self.switch_to_private, 'BROADCAST':self.switch_to_broadcast}
        self._private_user = GUEST

    def check_login(self,login):
        return True

    def initialization_procedure(self):
        print('Client program operational, enter Login')
        while True:
            login = input()
            if self.check_login(login):
                print('Login acquired')
                self._login = login
                break
            else:
                print('Invalid login, try again')

    def listen_to_server_thread(self):
        while True:
            try:
                received = str(self._sock.recv(1024), 'utf-8')
                self.process_server_responce(received)
            except:
                print('\nConnection broken')
                self._connection_online = False
                break 

    def process_server_responce(self, received):
        try:
            telegram_received = self._parser.parse_telegram(received)
            if telegram_received.header == MSG:
                if telegram_received.arguments[1] != self._visible_login:
                    print('\r{} | {} > {}'.format(telegram_received.arguments[0],telegram_received.arguments[1],telegram_received.message))
                    print('\r{} | {} > '.format(self._mode,self._visible_login),end='')
            elif telegram_received.header == LGN:
                if telegram_received.arguments[0]=='status' and telegram_received.arguments[1]=='online':
                    self._logged_in = True
                    self._visible_login = self._login
                    print('Login succesful')
                elif telegram_received.arguments[0]=='status' and telegram_received.arguments[1]=='offline':
                    print('Login credentials declined')
                    self._visible_login = GUEST
        except:
            raise

    def process_input(self,data):
        if len(data)>0: 
            if data[0] == '/':
                data_split = data.split(' ')
                command = data_split[0][1:]
                params = data_split[1:]
                if command in self.list_of_client_commands:
                    self.list_of_client_commands[command](params)
                    return
        message_type = message_types.broadcast
        if self._mode == 'broadcast':
            message_type = message_types.broadcast
        elif self._mode == 'private':
            message_type = message_types.private
        telegram_to_send = self._generator.generate_telegram(telegram_types.MSG,data,message_type,self._private_user)
        self.send_data(telegram_to_send)

    def switch_to_private(self,params):
        print('\rCLIENT | MODE > SWITCHING TO PRIVATE WITH USER {}'.format(params[0]))
        self._mode = 'private'
        self._private_user = params[0]

    def switch_to_broadcast(self,params):
        print('\rCLIENT | MODE > SWITCHING TO BROADCAST')
        self._mode = 'broadcast'
        self._private_user = GUEST

    def send_data(self,data_str):
        self._override_communication.acquire()
        self._sock.sendall(bytes(data_str, 'utf-8'))
        self._override_communication.release()

    def login_procedure(self):
        print('Enter password')
        password = input()
        telegram_to_send = self._generator.generate_login_string([self._login,password])
        if self._connection_online:
            self.send_data(telegram_to_send)
            time.sleep(LOGIN_DELAY_SECONDS)
            if not self._logged_in:
                print('No success logging in')
        else:
            print('Cannot authorize, no connection')

    def input_loop(self):
        while True:
            if self._mode == 'private':
                print('\r{}:{} | {} > '.format(self._mode,self._private_user,self._visible_login),end='')
            else:
                print('\r{} | {} > '.format(self._mode,self._visible_login),end='')
            data = input()
            if self._connection_online:
                self.process_input(data)
            else:
                break

    def connect_to_server(self,host,port):
        try:
            self._sock.connect((host, port))
            print('Connection to server {}:{} established'.format(host, port))
            self._connection_online = True
            threading.Thread(target = self.listen_to_server_thread,args = ()).start()
            self.login_procedure()
            self.input_loop()
        finally:
            self._sock.close()        


cl = client('Ingvar')
cl.initialization_procedure()
cl.connect_to_server(HOST,PORT)




