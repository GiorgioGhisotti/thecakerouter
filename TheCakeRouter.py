#!/usr/bin/env python
from Cake import *
import time
from termios import tcflush, TCIFLUSH
from typing import Tuple 

# find a suitable route between the client and the server,
# passing through NODE_COUNT nodes;
# returns a "route" tuple that can be passed to the routing function
def TCR_FindRoute(ADDR :Tuple[str, str], NODE_COUNT :int = 3):
	node_list = randomNodes(NODE_COUNT)
	sym_keys = symKeys(NODE_COUNT)
	
	NODE = (node_list[0][0].split(":")[0], node_list[0][0].split(":")[1])

	cakes = bakeCakes(list(map(lambda a:a[1], node_list)), 
	sym_keys, 
	len(node_list), 
	list(map(lambda a:a[0], node_list)), 
	":".join(ADDR))

	tcpNodeSocket = serverSocket(str(NODE[0]), int(NODE[1]))	#first node
	for i in range(len(node_list)):
		msg = cakes[i]
		for a in range(i):
			msg = encMsg(msg, sym_keys[i-1-a][0])

		tcpNodeSocket.send(msg)
		tcpNodeSocket.recv() #receive confirmation
        
	return [node_list, sym_keys, tcpNodeSocket]

# tell nodes in the route to wait for a new connection
# and close the current route's socket
def TCR_CloseRoute(route):
	route[2].send(b"quit")
	route[2].close()
	return

# route a message through the given route and return the answer
def TCR_Route(route, msg :str):
	if msg == "quit":
		TCR_CloseRoute(route)
		return ""	
	node_list = route[0]
	sym_keys = route[1]
	tcpNodeSocket = route[2]

	msg = symEncrypt(msg.encode("utf-8"), sym_keys, len(sym_keys))
	tcpNodeSocket.send(msg)
	data = tcpNodeSocket.recv()
	if data: 
		data = symDecrypt(data,
		sym_keys,
		len(sym_keys),
		len(sym_keys)-1)
		return data.decode("utf-8")
	else:
		return "Void answer!"
