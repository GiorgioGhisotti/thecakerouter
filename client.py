#!/usr/bin/env python
from Cake import *

PORT = "21567"

def main():
	node_list = randomNodes(3)
	sym_keys = symKeys(3)
	my_key = RSA.generate(RSA_MOD)
	public_key = my_key.publickey().exportKey('PEM')
	
	print(list(sym_keys))
	HOST = 'localhost'
	BUFSIZ = 4096
	ADDR = (HOST, PORT)
	NODE = (node_list[0][0].split(":")[0], node_list[0][0].split(":")[1])

	cakes = bakeCakes(list(map(lambda a:a[1], node_list)), sym_keys, len(node_list), list(map(lambda a:a[0], node_list)), ":".join(ADDR))
	
	tcp_cli_sock = serverSocket(str(NODE[0]), int(NODE[1]))	#first node
	for i in range(len(node_list)):
		msg = b"???".join(cakes[i])
		for a in range(i):
			iv = Random.new().read(AES.block_size)
			cipher = AES.new(sym_keys[len(sym_keys)-1-a][0], AES.MODE_CFB, iv)
			msg = b"???".join([iv, cipher.encrypt(msg)])

		tcp_cli_sock.send(msg)

	while True:
		data = input("> ")
		if not data:break
		msg = symEncrypt(data, sym_keys, len(sym_keys))
		tcp_cli_sock.send(msg)
		data = symDecrypt(tcp_cli_sock.recv(BUFSIZ), sym_keys)
		if not data:break
		print(data.decode('utf-8'))
	tcp_cli_sock.close()
	return

if __name__ == "__main__":
	main()
