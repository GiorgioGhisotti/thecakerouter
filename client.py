#!/usr/bin/env python
from Cake import *
import sys
import time
from termios import tcflush, TCIFLUSH

PORT = "21567"
NODE_COUNT = int(sys.argv[1])

def main():
	node_list = randomNodes(NODE_COUNT)
	sym_keys = symKeys(NODE_COUNT)
	my_key = RSA.generate(RSA_MOD)
	public_key = my_key.publickey().exportKey('PEM')
	
	HOST = 'localhost'
	ADDR = (HOST, PORT)
	NODE = (node_list[0][0].split(":")[0], node_list[0][0].split(":")[1])

	cakes = bakeCakes(list(map(lambda a:a[1], node_list)), 
	sym_keys, 
	len(node_list), 
	list(map(lambda a:a[0], node_list)), 
	":".join(ADDR))

	tcp_cli_sock = serverSocket(str(NODE[0]), int(NODE[1]))	#first node
	for i in range(len(node_list)):
		msg = DIVIDER.join(cakes[i])
		for a in range(i):
			msg = encMsg(msg, sym_keys[i-1-a][0])
			print("key #"+str(a)+": "+str(sym_keys[i-a][0]))

		tcp_cli_sock.send(msg)
		tcp_cli_sock.recv() #receive confirmation

	while True:
		tcflush(sys.stdin, TCIFLUSH)
		data = input("> ")
		while not data:
			tcflush(sys.stdin, TCIFLUSH)
			data = input("> ")
		if data == "quit":
			tcp_cli_sock.send(b"quit")
			break
		msg = symEncrypt(data.encode("utf-8"), sym_keys, len(sym_keys))
		tcp_cli_sock.send(msg)
		data = tcp_cli_sock.recv()
		if data: 
			data = symDecrypt(data,
			sym_keys,
			len(sym_keys),
			len(sym_keys)-1)
			print(data.decode("utf-8"))
		else:
			print("Strange, I got a void answer...")
	tcp_cli_sock.close()
	return

if __name__ == "__main__":
	main()
