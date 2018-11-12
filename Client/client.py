import socket
import sys
import threading

HOST, PORT = "localhost", 9999

def listen_to_server(sock):
	while True:
		received = str(sock.recv(1024), "utf-8")
		print("Received: {}".format(received))

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    threading.Thread(target = listen_to_server,args = (sock,)).start()
    while True:
        data = input()
        sock.sendall(bytes(data, "utf-8"))
finally:
    sock.close()
