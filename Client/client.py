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
        self._parser = telegram_parser()
        self._generator = telegram_generator()
        self._login = login
    def listen_to_server_thread(self):
        while True:
            received = str(self._sock.recv(1024), "utf-8")
            self.process_server_responce(received)
    def process_server_responce(self, received):
        telegram_received = self._parser.parse_telegram(received)
        if telegram_received.header == MSG:
            print("{} > {}".format(telegram_received.arguments[1],telegram_received.message))
    def process_input(self,data):
        telegram_to_send = self._generator.generate_telegram(telegram_types.MSG,data,message_types.broadcast,'Ingvar')
        self._sock.sendall(bytes(telegram_to_send, "utf-8"))
    def input_loop(self):
        while True:
            data = input()
            self.process_input(data)
    def connect_to_server(self,host,port):
        try:
            self._sock.connect((host, port))
            threading.Thread(target = self.listen_to_server_thread,args = ()).start()
            self.input_loop()
        finally:
            sock.close()        

cl = client('Ingvar')
cl.connect_to_server(HOST,PORT)



