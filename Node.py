#!/usr/bin/env python
from Cake import *
import sys

my_key = RSA.generate(RSA_MOD)
public_key = my_key.publickey().exportKey('PEM')

PORT = int(sys.argv[1])
HOST = "localhost"

def registerWithNodeServer(host, port):
	tcpSerSock = serverSocket(host, port)
	tcpSerSock.send(["localhost:" + str(PORT), public_key])
	tcpSerSock.close()
	return

def main():
	registerWithNodeServer("localhost", 1200)

	ADDR = (HOST, PORT)

	tcpProSock = Listener(ADDR) 

	while True:
		print("node %s waiting for a connection....." % PORT)
		tcpCliSock = tcpProSock.accept()
		print("node %s established connection!" %PORT)

		cake = decryptCake(tcpCliSock.recv(), my_key)
		kf = cake[0]	#forward key
		kb = cake[1]	#backwards key
		nxt = cake[2].decode("utf-8")	#next node or server
		print("node %s confirming cake reception..." %PORT)
		tcpCliSock.send(encMsg(b"got it", kb))
		print("next address: %s" %nxt)
		tcpSerSock = serverSocket(nxt.split(":")[0],int(nxt.split(":")[1]))	#generate socket with next node or server's address

		while True:
			data = tcpCliSock.recv()	#receive encrypted message
			if not data:break
			print("node %s received a message!" %PORT)
			data = data.split(b"???")
			cipher = AES.new(kf, AES.MODE_CFB, data[0])
			msg = cipher.decrypt(data[1])   #decrypt message with AES forward key
			print("my message: %s" %msg)
			tcpSerSock.send(msg)
			print("sent my message: %s" %msg)
			ans = tcpSerSock.recv()   #receive answer
			tcpCliSock.send(encMsg(ans, kb))  #encrypt and send answer with AES backwards key
		tcpCliSock.close()
		tcpSerSock.close()
	tcpProSock.close()
	return

if __name__ == "__main__":
	main()
