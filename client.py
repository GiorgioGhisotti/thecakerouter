#!/usr/bin/env python
from Cake import *
import sys

PORT = "21567"
NODE_COUNT = int(sys.argv[1])

def main():
	node_list = randomNodes(NODE_COUNT)
	sym_keys = symKeys(NODE_COUNT)
	my_key = RSA.generate(RSA_MOD)
	public_key = my_key.publickey().exportKey('PEM')
	
	HOST = 'localhost'
	BUFSIZ = 4096
	ADDR = (HOST, PORT)
	NODE = (node_list[0][0].split(":")[0], node_list[0][0].split(":")[1])

	cakes = bakeCakes(list(map(lambda a:a[1], node_list)), 
	sym_keys, 
	len(node_list), 
	list(map(lambda a:a[0], node_list)), 
	":".join(ADDR))

	print("Cakes: %s" %len(list(cakes)))
	
	tcp_cli_sock = serverSocket(str(NODE[0]), int(NODE[1]))	#first node
	for i in range(len(node_list)):
		msg = b"???".join(cakes[i])
		for a in range(i):
			msg = encMsg(msg, sym_keys[len(sym_keys)-1-a][0])

		tcp_cli_sock.send(msg)
		print("sent cake #%s!" %(i+1))
		tcp_cli_sock.recv() #receive confirmation

	while True:
		data = input("> ")
		if not data:break
		msg = symEncrypt(data.encode("utf-8"), sym_keys, len(sym_keys))
		tcp_cli_sock.send(msg)
		data = symDecrypt(tcp_cli_sock.recv(), sym_keys, len(sym_keys), len(sym_keys)-1)
		if not data:break
		print(data.decode("utf-8"))
	tcp_cli_sock.close()
	return

if __name__ == "__main__":
	main()
