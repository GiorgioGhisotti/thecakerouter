#!/usr/bin/env python
import os

os.system("python NodeServer.py&")
for i in range(20):
    os.system("python Node.py "+str(4000+i)+"&")
print("starting server...")
os.system("python server.py&")
os.system("clear")
