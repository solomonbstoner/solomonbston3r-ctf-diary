"""
I took a walk around the world to ease my troubled mind.

Lyrics from song "Kryptonite" by "3 Doors Down"

Requires py-cryptonight (https://github.com/ph4r05/py-cryptonight)

process output of:

    nc ctf.pwn.sg 1502

"""

import string
import binascii
import pycryptonight

FILENAME = 'out.txt'

clues = []
with open(FILENAME, 'r') as f:
    clues = f.readline().rstrip().split(' ')
    clues.append(f.readline().rstrip()[:-1])

# clues[0] --> length of 86

byte_string = bytes.fromhex(clues[0])

res_byte_string = pycryptonight.cn_slow_hash(byte_string, variant = 1)

res_hex_string = binascii.hexlify(res_byte_string)

if res_hex_string.decode('utf-8') == clues[2]:
    print(">> found the right hash algorithm!")
else:
    print(">> wrong hash algorithm")
