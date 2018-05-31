#!/usr/bin/env python
from Cake import *

PORT = 21567

def main():
	node_list = randomNodes(3)
	sym_keys = symKeys(3)
	my_key = RSA.generate(2048)
	public_key = my_key.publickey().exportKey('PEM')

	HOST = 'localhost'
	BUFSIZ = 4096
	ADDR = (HOST, PORT)
	NODE = (node_list[0][0].split(":")[0], node_list[0][0].split(":")[1])

	tcp_cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_cli_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcp_cli_sock.connect(NODE)

	cake = wrapCake(0, map(lambda a:a[1], node_list), sym_keys, map(lambda a:a[0], node_list), ADDR)

	tcp_cli_sock.send(cake)	#send cake to first node

	while True:
		data = input("> ")
		if not data:break
		msg = symEncrypt(data, sym_keys)
		tcp_cli_sock.send(msg)
		data = symDecrypt(tcp_cli_sock.recv(BUFSIZ), sym_keys)
		if not data:break
		print(data.decode('utf-8'))
	tcp_cli_sock.close()
	return

if __name__ == "__main__":
	main()
