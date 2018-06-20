from pwn import *
import binascii
import pycryptonight
import pdb

HOST = 'ctf.pwn.sg'
PORT = 1502

conn = remote(HOST, PORT)

clues = str(conn.recvline().rstrip()).split(' ') # ignore for this script

enc = conn.recvline().rstrip()[:-1]

res_byte_string = pycryptonight.cn_slow_hash(binascii.unhexlify(enc), variant=1)

sol = binascii.hexlify(res_byte_string)

sol += b'\n'

print(">> sending %s" % sol)
conn.send(sol)

print(">> received:\n%s" % conn.recvline())

conn.close()
