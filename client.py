#!.env python
from TheCakeRouter import *
import sys

PORT = "21567"
HOST = "localhost"
NODE_COUNT = int(sys.argv[1])

def main():
	route = TCR_FindRoute((HOST, PORT), NODE_COUNT)

	while True:
		tcflush(sys.stdin, TCIFLUSH)
		data = input("> ")
		while not data:
			tcflush(sys.stdin, TCIFLUSH)
			data = input("> ")
		if data == "quit":
			TCR_CloseRoute(route)
			return
		ans = TCR_Route(route, data)
		print("Answer => %s" %ans)
	return

if __name__ == "__main__":
	main()
