import base64
import binascii
import numpy as np
import gmpy
import fractions

def chinese_remainder(n, a):
    sum_ = 0
    prod = np.product(n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum_ += a_i * mul_inv(p, n_i) * p
    return sum_ % prod

"""
Find the GCD of two or more integers.
"""
def xgcd(x_):
    if len(x_) < 2:
        raise Exception('Require at least two integers')
    gcd = x_[0]
    for i in range(0,len(x_)-1):
        gcd = fractions.gcd(x_[i+1], gcd)
    return gcd

"""
Extended Euclidean algorithm

Given positive integers a, b, return a triple (g, x, y), such that x * a + y * b = g = gcd(a, b).

Source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python

"""
def extendedEuclid(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  a, x0, y0

"""
Find x such that:

    b x = 1 (mod n)

That is, x is the multiplicative inverse of a under modulo b.

Source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
"""
def mul_inv(b, n):
    g, x, _ = extendedEuclid(b, n)
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

"""
Try prime factorization
"""
def factors(n):
    result = set()
    n = gmpy.mpz(n)
    for i in range(1, gmpy.sqrt(n)+1):
        div, mod = gmpy.fdivmod(n, i)
        if not mod:
            result |= {gmpy.mpz(i), div}
        return result

"""
Calculate Bezout Coefficients for two or more integers via the repeated application of the extended Euclidean algorithm.

Source: https://math.stackexchange.com/questions/735093/method-of-solving-extended-euclidean-algorithm-for-three-numbers
"""
def calculateBezoutCoefficients(x_):
    if len(x_) < 2:
        raise Exception('Require at least two integers')
    gcds = [x_[0]]
    for i in range(0,len(x_)-1):
        gcds.append(fractions.gcd(x_[i+1], gcds[i]))
    coefs = [1]
    for i in range(0,len(x_)-1):
        tmp = extendedEuclid(gcds[i], x_[i+1])
        for j in range(0, i+1):
            coefs[j] *= tmp[1]
        coefs.append(tmp[2])
        ### internal validation
        tmp = 0
        for j in range(0, i+2):
            tmp += coefs[j] * x_[j]
        if tmp != gcds[i+1]:
            raise Exception('error in calculating Bezout coefficients')
    return coefs

if __name__ == '__main__':

    n1 = int('00d2a955e1e8b61302b9b83a2203ba9195', 16)
    c1 = b64toInt('pAvH0C8oeAF0PUX4ntQOJw==')

    n2 = int('00c4b5649412f9c888a52b01bf41a84edb', 16)
    c2 = b64toInt('p+XoMuN1JKzZI2L/EDF2xQ==')

    n3 = int('00d0389dd24e4c4e28658da7f1930b04bf', 16)
    c3 = b64toInt('a+GgTrVXCGWWL9JO7CPhxA==')

    crt = chinese_remainder([n1, n2, n3], [c1, c2, c3])

    r = nthroot(3, crt)
    print(I2OSP(r))

    fac = factors(12345678901234567)

    # test = [240, 46]
    # res = calculateBezoutCoefficients(test)
    # print('>> calculateBezoutCoefficients for %s: %s' % (test, res))

    # test = [181, 113, 167, 199, 233]
    test = [50734392291911, 197276336925781, 156766473933809, 184841710386187, 64271800149937]
    res = calculateBezoutCoefficients(test)
    print('>> calculateBezoutCoefficients for %s: %s' % (test, res))

    tmp = 0
    for i in range(len(test)):
        tmp += test[i] * res[i]
    if tmp == 1:
        print('>> test passed')
    else:
        print('>> test failed')

