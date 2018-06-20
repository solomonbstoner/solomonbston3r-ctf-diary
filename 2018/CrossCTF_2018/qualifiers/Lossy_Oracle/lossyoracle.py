#!/usr/bin/python3
import os
import random
import base64
import pdb

def encrypt(data, key, func): # func performs OR
    length = len(key)
    output = []
    for i in range(len(data)):
        output.append(func(data[i],key[i%length]))
    return bytes(output)

def queryOracle():
    file_path = 'out.txt'
    with open(file_path, 'rb') as file:
        data = file.read()
    key = []
    for i in range(random.randrange(64,128)):
        key.append(random.randrange(0,255))
    key = bytes(key)
    function = [lambda x,y:x&y, lambda x,y:x|y]
    return(base64.b64encode(encrypt(data, key, function[1])).decode("utf-8"))

if __name__ == "__main__":
    # file_path = '/home/lossyoracleuser/flag'    
    file_path = 'out.txt'
    with open(file_path, 'rb') as file:
        data = file.read()

    key = []
    for i in range(random.randrange(64,128)):
        key.append(random.randrange(0,255))
    key = bytes(key) 
    # key = [0x41] * 64 # replace for testing

    # key is random byte array of random length in [64, 128)

    function = [lambda x,y:x&y, lambda x,y:x|y]

    print (base64.b64encode(encrypt(data, key, function[1])).decode("utf-8"))
