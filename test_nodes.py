#!/usr/bin/env python
import os

os.system("python NodeServer.py&")
for i in range(6):
    os.system("python Node.py "+str(4000+i)+"&")

