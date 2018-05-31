#!/usr/bin/env python
from Cake import *

my_key = RSA.generate(2048)
public_key = my_key.publickey().exportKey('PEM')

HOST = ""
PORT = 21567
ADDR = (HOST, PORT)

tcpSerSock = Listener(ADDR) 

while True:
	print("server waiting for a connection.....")
	tcpCliSock= tcpSerSock.accept()
	print("....server connected")
	while True:
		data = tcpCliSock.recv().decode("utf-8")	#receive encrypted message
		if not data:break
		tcpCliSock.send(("I got this message: %s" %data).encode("utf-8"))
	tcpCliSock.close
tcpSerSock.close()
