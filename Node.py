#!/usr/bin/env python
from Cake import *

my_key = RSA.generate(2048)
public_key = my_key.publickey().exportKey('PEM')

PORT = 4001
HOST = "localhost"

def registerWithNodeServer(host, port):
	tcpSerSock = serverSocket(host, port)
	return

def writePubKey():
	filename = "%spubkey.der" % PORT
	f = open(filename,'w')
	f.write(public_key)
	return

def keyExchange(sock):	#exchange keys with client
	key = RSA.importKey(sock.receive(BUFSIZ))
	sock.send(public_key)
	return key

def forwardMessage(msg, sock):	#forward message to server
	sock.send(msg)
	ans = sock.receive(BUFSIZ)
	return ans

def serverSocket(host, port):
	ADDR = (host, port)
	tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpSerSock.connect(ADDR)
	return tcpSerSock

def registerWithNodeServer(host, port):
	tcpSerSock = serverSocket(host, port)
	tcpSerSock.send((HOST + ":" + string(PORT), my_key.publickey()))
	tcpSerSock.close()
	return

def main():

	registerWithNodeServer("localhost", 1200)

	writeKey()
	ADDR = (HOST, PORT)

	tcpProSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpProSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpProSock.bind(ADDR)
	tcpProSock.listen(5)

	while True:
		print("node %s waiting for a connection....." % PORT)
		tcpCliSock, addr = tcpProSock.accept()
		print("...connected from:", addr)

		cake = decryptCake(tcpCliSock.recv(BUFSIZ), my_key)
		kf = cake[0]	#forward key
		kb = cake[1]	#backwards key
		next = cake[2]	#next node or server
		fw_cake = cake[3]	#cake to forward

		if(fw_cake == 0):	#exit node
			tcpSerSock = serverSocket(next.split(":"))
			while True:
				data = tcpCliSock.recv(BUFSIZ)	#receive encrypted message
				if not data:break
				cipher = AES.new(kf, AES.MODE_CFB, data[0])
				msg = cipher.decrypt(data[1])
				tcpSerSock.send(msg)
				ans = tcpSerSock.recv(BUFSIZ)
				iv = Random.new().read(AES.block_size)
				cipher = AES.new(kb, AES.MODE_ECB, iv)
				tcpCliSock.send((iv, cipher.encrypt(ans)))
		else:

			while True:
				data = tcpCliSock.recv(BUFSIZ)	#receive encrypted message
				if not data:break
				cipher = PKCS1_v1_5.new(my_key)
				data = cipher.decrypt(data, "b")	#decrypt message with private key
				data = exitNode("localhost", 21567, data)
				cipher = PKCS1_v1_5.new(client_key)
				data = cipher.encrypt(data)	#encrypt message with client's public key
				tcpCliSock.send(data)
		tcpCliSock.close
	tcpProSock.close()
	return

if __name__ == "__main__":
	main()
