#!.env python
from Cake import *

HOST = "localhost"
PORT = 1200

node_list = [] 

def main():

	ADDR = (HOST, PORT)

	tcpSerSock = Listener(ADDR)

	while True:
		tcpCliSock= tcpSerSock.accept()
		data = tcpCliSock.recv()
		if len(data) == 2:	#node
			if not data:break
			node_list.append(data)
		else:				#client
			tcpCliSock.send(node_list)
	tcpCliSock.close
	tcpSerSock.close
	return

if __name__ == "__main__":
	main()
