"""
References:
- https://wiremask.eu/writeups/hackingweek-2015-crypto-2/
"""
from pwn import *
from fractions import gcd
import numpy as np
import math
import binascii
import pdb
import gmpy2

HOST = '192.168.51.15'
PORT = 11001

def factor(n):
    assert n % 2 != 0

    a = gmpy2.isqrt(n)
    b2 = gmpy2.square(a) - n

    while not gmpy2.is_square(b2):
        a += 1
        b2 = gmpy2.square(a) - n

    factor1 = a + gmpy2.isqrt(b2)
    factor2 = a - gmpy2.isqrt(b2)
    return int(factor1), int(factor2)

def queryN(N_prev = None, noisy = False):

    conn = remote(HOST, PORT, typ='tcp')

    while True:

        # Receive data
        data = conn.recvline()
        if noisy:
            print('received:\n%s' % data)

        data = conn.recvline()
        if noisy:
            print('received:\n%s' % data)

        data = conn.recvline()
        if noisy:
            print('received:\n%s' % data)

        N = gmpy2.mpz(data.rstrip().split(b' ')[1])

        (p, q) = factor(N)

        if p * q != N:
            print('>> error')

        data = conn.recv()
        if noisy:
            print('received:\n%s' % data)

        if noisy:
            print('sending %s' % p)
        conn.sendline(str(p))

        data = conn.recv()
        if noisy:
            print('received:\n%s' % data)

        if noisy:
            print('sending %s' % q)
        conn.sendline(str(q))

        data = conn.recvline()
        if noisy:
            print('received:\n%s' % data)

    conn.close()

queryN(noisy = True)
