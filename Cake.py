#!/usr/bin/env python
#support module for the cake router
import pickle
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from time import ctime
import string
import random
import os
from functools import partial
import hashlib

NODEFILE = "nodes.txt"
BUFSIZ = 4096
RSA_MOD = 2048 
DIVIDER = b"@@@"

def Cake():
	print("The cake is a lie!")
	return

def randomNodes(n):
	tcpSerSock = serverSocket("localhost", 1200)
	tcpSerSock.send([0])
	nodes = tcpSerSock.recv()
	tcpSerSock.close()
	random.SystemRandom().shuffle(nodes)
	if(len(nodes) < n): return nodes
	return nodes[:n]

def secondHalfByChar(char, addr):
	return addr.split(char)[1]

def nodeKeys(node_list):
	lines = map(lambda x: x.split(":")[1], node_list)
	pub_keys = map(lambda x: x+"pubkey.der", lines)
	return pub_keys

def symKeys(n):	#generate a random set of forward and backwards keys
	k = [[] for i in range(n)]
	for i in range(n):
		k[i] = [hashlib.sha256(os.urandom(16)).digest(),
		hashlib.sha256(os.urandom(16)).digest()]
		print("Node "+str(i)+" key: "+str(k[i]))
	return k

def encryptCake(cake, pub_key):
	key = RSA.importKey(pub_key)
	cipher = PKCS1_OAEP.new(key)
	for i in range(len(cake)):
		cake[i] = cipher.encrypt(cake[i])
	return cake 

def decryptCake(cake, key):
	cake=list(cake.split(DIVIDER))
	cipher = PKCS1_OAEP.new(key)
	for i in range(len(cake)):
	    cake[i] = cipher.decrypt(cake[i])
	return cake

def bakeCakes(pub_keys, sym_keys, nodes, node_list, addr):
	cakes = []
	for i in range(nodes):
		if i==nodes-1:
			cakes.append(encryptCake([sym_keys[i][0], 
			sym_keys[i][1], 
			addr.encode("utf-8")], 
			pub_keys[i]))
		else:
			cakes.append(encryptCake([sym_keys[i][0], 
			sym_keys[i][1], 
			node_list[i+1].encode("utf-8")], 
			pub_keys[i]))
	return cakes

def symEncrypt(msg, sym_keys, n):	#encrypt message with forward keys
	if(n == 0):
		return msg
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(sym_keys[n-1][0], AES.MODE_CFB, iv)
	msg = DIVIDER.join([iv, cipher.encrypt(msg)])
	return symEncrypt(msg, sym_keys, n-1)

def symDecrypt(msg, sym_keys, n, i):	#decrypt message with backward keys
	if(i==-1):
		return msg
	msg = msg.split(DIVIDER)
	iv = msg[0]
	cipher = AES.new(sym_keys[n-i-1][1], AES.MODE_CFB, iv)
	msg = cipher.decrypt(msg[1])
	return symDecrypt(msg, sym_keys, n, i-1)

def encMsg(msg, key):	#encrypt a message with the given AES key and add the IV
	iv = Random.new().read(16)
	cipher = AES.new(key, AES.MODE_CFB, iv)
	msg = DIVIDER.join([iv, cipher.encrypt(msg)])
	return msg

def sendMessage(sock, cake, sym_keys):
	sock.send(cake)
	ans = sock.recv(BUFSIZ)

	return ans

def serverSocket(host, port):
	tcpSerSock = Client((host, port))
	return tcpSerSock
