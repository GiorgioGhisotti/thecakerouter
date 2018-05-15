from Cake import *

def main():
	HOST = ""
	PORT = 4000
	BUFSIZ = 2048
	ADDR = (HOST, PORT)

	tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpSerSock.bind(ADDR)
	tcpSerSock.listen(5)

	while true:	#accept connection from a new client
		tcpCliSock, addr= tcpSerSock.accept()
		server_address = tcpCliSock.recv(BUFSIZ)
		message = tcpCliSock.recv(BUFSIZ)
		while message:	#route messages from client until

			message = tcpCliSock.recv(BUFSIZ)
		tcpCliSock.close()
	tcpSerSock.close()
	return

main()
