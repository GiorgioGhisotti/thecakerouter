#!/usr/bin/env python
#support module for the cake router
from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
import socket
from time import ctime
import string
import random
import os
from functools import partial

NODEFILE = "nodes.txt"
BUFSIZ = 2048

def Cake():
	print("The cake is a lie!")
	return

def randomNodes(n):
	nodes = open(NODEFILE, "r")
	lines = nodes.read().split('\n')
	if len(lines) < n+1:
		return lines
	lines = lines[:n]
	random.SystemRandom().shuffle(lines)
	if len(lines) < n:
		return lines
	return lines[:n]

def secondHalfByChar(char, addr):
	return addr.split(char)[1]

def nodeKeys(node_list):
	lines = map(lambda x: x.split(":")[1], node_list)
	pub_keys = map(lambda x: x+"pubkey.der", lines)
	return pub_keys

def symKeys(n):	#generate a random set of forward and backwards keys
	if n <= 1:
		return (os.urandom(16), os.urandom(16))
	return ((os.urandom(16), os.urandom(16)), symKeys(n-1))

def encryptCake(cake, pub_key):
	key = RSA.importKey(pub_key)
	cipher = PKCS1_v1_5.new(key)
	return cipher.encrypt(cake)

def decryptCake(cake, key):
	cipher = PKCS1_v1_5.new(key)
	return cipher.decrypt(cake)

def wrapcake(o, pub_keys, sym_keys, nodes, node_list, addr):
	kf = sym_keys[nodes][0]
	kb = sym_keys[nodes][1]
	if nodes == 0:
		return cake
	elif nodes > len(keys):
		cake = (kf, kb, addr, 0)
	else:
		cake = (kf, kb, node_list[node], o)
	return wrapcake(encryptCake(cake, pub_keys[nodes-1]), pub_keys, sym_keys, nodes-1, node_list, port)

def symEncrypt(msg, sym_keys, n):
	if(n == 0):
		return msg
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(sym_keys[n-1][0], AES.MODE_CFB, iv)
	msg = (iv, cipher.encrypt(msg))
	return symEncrypt(msg, sym_keys, n-1)

def symDecrypt(ans, sym_keys, n):

	return

def sendMessage(sock, cake, sym_keys):
	sock.send(cake)
	ans = sock.recv(BUFSIZ)

	return ans
