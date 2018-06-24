import base64
from nc2 import queryOracle
import numpy as np
import pdb

def isBit(candidate, position):
    mask = 1 << (position)
    return (candidate & mask > 0)

ATTEMPTS = 20 # arbitrarily chosen number of repeats

FLAG_LENGTH = 14160 # should always be constant
# FLAG_LENGTH = 67 should always be constant

MASKS = [
    0b11111110,
    0b11111101,
    0b11111011,
    0b11110111,
    0b11101111,
    0b11011111,
    0b10111111,
    0b01111111]

### initialization of data structure

guesses = []
for byte_index in range(FLAG_LENGTH):
    guesses.append(255)

### query oracle

for i in range(ATTEMPTS):

    oracle = base64.b64decode(queryOracle())
    for c in oracle:
        if c > 255:
            print(">> found %s with ord %d" % (c, chr(c)))
    if len(oracle) != FLAG_LENGTH:
        raise Exception('Error in process!')

    for byte_index in range(FLAG_LENGTH):
        for bit_index in range(8):
            if not isBit(oracle[byte_index], bit_index):
                guesses[byte_index] &= MASKS[bit_index] # confirmed bit is unset!

    # print(">> %s" % oracle[0])

### reconstruct guess

sol = bytes(guesses)

print(">> sol is:\n%s" % sol)

# print(">> is flag present? %s" % sol.decode('utf-8').find('CrossCTf'))
