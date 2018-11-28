import socket
import sys
import threading
from telegram_parser import *
from telegram_generator import *

HOST, PORT = "localhost", 9999
MSG = '#MSG'

class client:
    def __init__(self,login):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection_online = False
        self._parser = telegram_parser()
        self._generator = telegram_generator()
        self._login = login
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
                received = str(self._sock.recv(1024), "utf-8")
            except:
                print('Connection broken')
                self._connection_online = False
                break
            self.process_server_responce(received)
    def process_server_responce(self, received):
        try:
            telegram_received = self._parser.parse_telegram(received)
            if telegram_received.header == MSG:
                print("{} > {}".format(telegram_received.arguments[0],telegram_received.message))
        except:
            print("NO TELGRAM, TEXT:{}".format(received))
    def process_input(self,data):
        telegram_to_send = self._generator.generate_telegram(telegram_types.MSG,data,message_types.broadcast,'Ingvar')
        self._sock.sendall(bytes(telegram_to_send, "utf-8"))
    def input_loop(self):
        while True:
            data = input()
            if self._connection_online:
                self.process_input(data)
            else:
                break
    def connect_to_server(self,host,port):
        try:
            self._sock.connect((host, port))
            print('Connection to server established')
            self._connection_online = True
            threading.Thread(target = self.listen_to_server_thread,args = ()).start()
            self.input_loop()
        finally:
            self._sock.close()        


cl = client('Ingvar')
cl.initialization_procedure()
cl.connect_to_server(HOST,PORT)



