from Cake import *

PORT = 1200
BUFSIZ = 4096

node_list

def addNode(data):
	node_list.append(data)
	return

def main():

	ADDR = (HOST, PORT)

	tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpSerSock.bind(ADDR)
	tcpSerSock.listen(1)

	while True:
		data = tcpCliSock.recv(BUFSIZ)	#receive encrypted message
		if len(data) == 2:	#node
		if not data:break
			node_list.append(data)
		else:				#client
			tcpCliSock.send(node_list)
	tcpCliSock.close
	return

if __name__ == "__main__":
	main()
