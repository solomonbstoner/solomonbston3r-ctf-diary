"""
Encoding modules for cryptography.
"""

import sys
import base64
import binascii

"""
Convert a Base 64 String to Integer.
"""
def b64toInt(input_string):
    bytes_ = base64.b64decode(input_string)
    if sys.version[0] == '2':
        # Python 2.X
        return int(bytes_.encode('hex'), 16)
    else:
        # Python 3.X
        return int.from_bytes(bytes_, 'big')


'''
Converts an integer into a string of bytes (an Octet String).

As defined in PKCS #1 v2.1: RSA Cryptography Standard (June 14, 2002)

References:
* https://zzundel.blogspot.sg/2011/02/rsa-implementation-using-python.html
'''
def I2OSP(longint):
    return binascii.unhexlify(hex(longint)[2:])


"""
Unit tests
"""
if __name__ == '__main__':

    string = 'ABCD' # ord('A') = 0x41, ord('B') = 0x42, ...

    ### [1] convert a string <--> bytes

    bytes_ = string.encode('utf-8') # b'ABCD'
    if sys.version[0] == '3':
        # Python 3.X
        bytes_2 = bytes(string, 'utf-8') # b'ABCD'

    string2 = bytes_.decode('utf8') # 'ABCD'

    ### [2] convert bytes <--> hex string

    if sys.version[0] == '3':
        # Python 3.X
        hex_string = bytes_.hex() # '41424344'

    hex_string2 = binascii.hexlify(bytes_).decode('utf-8') # '41424344'
    hex_string3 = binascii.b2a_hex(bytes_).decode('utf-8') # '41424344'

    if sys.version[0] == '3':
        # Python 3.X
        bytes_3 = bytes.fromhex(hex_string3) # b'ABCD'
    bytes_4 = binascii.unhexlify(hex_string3) # b'ABCD'

    ### [3] convert bytes <--> bytes representation of hex string (confusing!)

    bytes_hex = binascii.hexlify(bytes_) # b'41424344'

    bytes_5 = binascii.unhexlify(bytes_hex) # b'ABCD'

    ### [7] convert string <--> bytearray

    byte_array_1 = bytearray(string, 'utf-8')
    string3 = byte_array_1.decode('utf-8')

    ### [8] convert bytes to bytearray

    byte_array_2 = bytearray(bytes_)
    bytes_6 = bytes(byte_array_2)
