#!/usr/bin/env python
from Cake import *

my_key = RSA.generate(2048)
public_key = my_key.publickey().exportKey('PEM')

HOST = ""
PORT = 21567
BUFSIZ = 2048
ADDR = (HOST, PORT)

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(1)

while True:
	print("waiting for a connection.....")
	tcpCliSock, addr= tcpSerSock.accept()
	print("....connected from:", addr)

	client_key = RSA.importKey(tcpCliSock.recv(BUFSIZ))
	tcpCliSock.send(public_key)
	while True:
		data = tcpCliSock.recv(BUFSIZ)	#receive encrypted message
		if not data:break
		cipher = PKCS1_v1_5.new(my_key)
		data = cipher.decrypt(data, "b")	#decrypt message with private key
		cipher = PKCS1_v1_5.new(client_key)
		data = cipher.encrypt(data)	#encrypt message with client's public key
		tcpCliSock.send(data)
	tcpCliSock.close
tcpSerSock.close()
