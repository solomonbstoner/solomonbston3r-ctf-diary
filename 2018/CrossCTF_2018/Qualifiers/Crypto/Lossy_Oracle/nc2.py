from pwn import *

HOST = 'ctf.pwn.sg'
PORT = 1401

def queryOracle():
    conn = remote(HOST, PORT)
    oracle = conn.recvuntil('\n')
    conn.close()
    return oracle

if __name__ == '__main__':
    conn = remote(HOST, PORT)
    oracle = conn.recvline()
    conn.close()
