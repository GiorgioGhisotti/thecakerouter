#!/usr/bin/env python
#support module for the cake router
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
import hashlib
import sys

RSA_MOD = 2048 
DIVIDER = b"@@@"    #used to temporarily unite the elements of a list so they can be sent together

def Cake():
	print("The cake is a lie!")
	return

#obtains the list of nodes from the node server and returns a random selection of n different nodes
def randomNodes(n):
	tcpSerSock = serverSocket("localhost", 1200)
	tcpSerSock.send([0])
	nodes = tcpSerSock.recv()
	tcpSerSock.close()
	random.SystemRandom().shuffle(nodes)
	if(len(nodes) < n): return nodes
	return nodes[:n]

#generate a random set of forward and backwards keys
def symKeys(n):	
	k = [[] for i in range(n)]
	for i in range(n):
		k[i] = [hashlib.sha256(os.urandom(16)).digest(),
		hashlib.sha256(os.urandom(16)).digest()]
	return k

#joins and encrypts the elements of a cake with the target node's public RSA key
def encryptCake(cake, pub_key):
	cake = DIVIDER.join(cake)
	key = RSA.importKey(pub_key)
	cipher = PKCS1_OAEP.new(key)
	cake = cipher.encrypt(cake)
	return cake

#decrypts and splits cake 
def decryptCake(cake, key):
	cipher = PKCS1_OAEP.new(key)
	cake = cipher.decrypt(cake)
	cake=list(cake.split(DIVIDER))
	return cake

#create list of cakes to be sent to each node
def bakeCakes(pub_keys, sym_keys, nodes, node_list, addr):
	cakes = []
	for i in range(nodes):
		if i == nodes-1:
			cakes.append(
			encryptCake([sym_keys[i][0],sym_keys[i][1],addr.encode("utf-8")], 
			pub_keys[i]))
		else:
			cakes.append(
			encryptCake([sym_keys[i][0],sym_keys[i][1],node_list[i+1].encode("utf-8")],
			pub_keys[i]))
	return cakes

#encrypt message with forward keys
def symEncrypt(msg, sym_keys, n):	
	if(n == 0):
		return msg
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(sym_keys[n-1][0], AES.MODE_CFB, iv)
	msg = DIVIDER.join([iv, cipher.encrypt(msg)])
	return symEncrypt(msg, sym_keys, n-1)

#decrypt message with backward keys
def symDecrypt(msg, sym_keys, n, i):
	if(i==-1):
		return msg
	msg = msg.split(DIVIDER)
	iv = msg[0]
	if(sys.getsizeof(iv) != 49): return b"Error! Message got corrupted in transit"
	cipher = AES.new(sym_keys[n-i-1][1], AES.MODE_CFB, iv)
	msg = cipher.decrypt(msg[1])
	return symDecrypt(msg, sym_keys, n, i-1)

#encrypt a message with the given AES key and add the IV
def encMsg(msg, key):
	iv = Random.new().read(16)
	while(sys.getsizeof(iv) != 49):
		iv = Random.new().read(16)
	cipher = AES.new(key, AES.MODE_CFB, iv)
	msg = DIVIDER.join([iv, cipher.encrypt(msg)])
	return msg

def serverSocket(host, port):
	tcpSerSock = Client((host, port))
	return tcpSerSock
