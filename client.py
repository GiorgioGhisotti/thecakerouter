#!/usr/bin/env python
from Cake import *

PORT = 21567

def main():
	node_list = randomNodes(3)
	sym_keys = symKeys(3)
	my_key = RSA.generate(2048)
	public_key = my_key.publickey().exportKey('PEM')

	HOST = 'localhost'
	BUFSIZ = 2048
	ADDR = (HOST, PORT)

	tcp_cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_cli_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcp_cli_sock.connect(ADDR)

	tcp_cli_sock.send(public_key)	#send public key to server
	server_key = RSA.importKey(tcp_cli_sock.recv(BUFSIZ))	#receive server's public key
	while True:
		data = input("> ")
		cipher = PKCS1_v1_5.new(server_key)
		data = cipher.encrypt(data.encode())
		if not data:break
		tcp_cli_sock.send(data)
		cipher = PKCS1_v1_5.new(my_key)
		data = cipher.decrypt(tcp_cli_sock.recv(BUFSIZ), "b")
		if not data:break
		print(data.decode('utf-8'))
	tcp_cli_sock.close()
	return
if __name__ == "__main__":
	main()
