from pwn import *
from fractions import gcd
import numpy as np
import math
import binascii
import pdb
import gmpy2
from gmpy2 import mpz

HOST = '192.168.51.15'
PORT = 11003

def solver(N1_, N2_):
    N1 = mpz(N1_)
    N2 = mpz(N2_)
    common_p = gcd(N1, N2)
    q1 = gmpy2.c_div(N1, common_p)
    q2 = gmpy2.c_div(N2, common_p)
    return (common_p, q1, q2)


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

        N1 = data.rstrip().split(b' ')[1]

        data = conn.recvline()
        if noisy:
            print('received:\n%s' % data)

        N2 = data.rstrip().split(b' ')[1]

        (common_p, q1, q2) = solver(N1, N2)

        if common_p * q1 != mpz(N1):
            print('>> verification failed')
            pdb.set_trace()

        if common_p * q2 != mpz(N2):
            print('>> verification failed')
            pdb.set_trace()

        data = conn.recv()
        if noisy:
            print('received:\n%s' % data)

        conn.sendline(str(common_p))

        data = conn.recv()
        if noisy:
            print('received:\n%s' % data)

        conn.sendline(str(int(q1)))

        data = conn.recv()
        if noisy:
            print('received:\n%s' % data)

        conn.sendline(str(common_p))

        data = conn.recv()
        if noisy:
            print('received:\n%s' % data)

        conn.sendline(str(int(q2)))

        data = conn.recvline()
        if noisy:
            print('received:\n%s' % data)

        if b'flag' in data:
            print('>> found flag!:\n%s' % data)
            break

    conn.close()

queryN(noisy = False)
