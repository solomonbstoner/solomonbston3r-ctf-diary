import base64
import binascii
import numpy as np
import gmpy

def chinese_remainder(n, a):
    sum = 0
    prod = np.product(n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

"""
Extended Euclidean algorithm

take positive integers a, b as input, and return a triple (g, x, y), such that ax + by = g = gcd(a, b).

Source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python

"""
def xgcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

"""
Find x such that:

    b x = 1 (mod n)

That is, x is the multiplicative inverse of a under modulo b.

Source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
"""
def mul_inv(b, n):
    g, x, _ = xgcd(b, n)
    if g == 1:
        return x % n

def b64toInt(input_string):
    byte_string = base64.b64decode(input_string)
    return int.from_bytes(byte_string, 'big')

'''
I2OSP(longint) -> byte string

I2OSP converts a long integer into a string of
bytes (an Octet String). It is defined in the
PKCS #1 v2.1: RSA Cryptography Standard (June 14, 2002)

source: https://zzundel.blogspot.sg/2011/02/rsa-implementation-using-python.html
'''
def I2OSP(longint):
    return binascii.unhexlify(hex(longint)[2:])

"""
Compute the n-th root of a (without modulo).
"""
def nthroot(n, a, NOISY = False):
    m0 = gmpy.mpz(a)
    res = m0.root(n)
    if NOISY:
        print(">> success? %s" % res[1])
    return res[0]

if __name__ == '__main__':

    n = [3, 5, 7]
    a = [2, 3, 2]
    print(chinese_remainder(n, a))

    n1 = int('00d2a955e1e8b61302b9b83a2203ba9195', 16)
    c1 = b64toInt('pAvH0C8oeAF0PUX4ntQOJw==')

    n2 = int('00c4b5649412f9c888a52b01bf41a84edb', 16)
    c2 = b64toInt('p+XoMuN1JKzZI2L/EDF2xQ==')

    n3 = int('00d0389dd24e4c4e28658da7f1930b04bf', 16)
    c3 = b64toInt('a+GgTrVXCGWWL9JO7CPhxA==')

    crt = chinese_remainder([n1, n2, n3], [c1, c2, c3])

    r = nthroot(3, crt)

    print(I2OSP(r))
