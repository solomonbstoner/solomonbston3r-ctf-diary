#!/usr/bin/env python

import sys
flag = 'cysec16-In05'
from bitstring import BitArray
import time
import signal
import pdb


def write(data, endl='\n'):
    sys.stdout.write(data + endl)
    sys.stdout.flush()


def readline():
    return sys.stdin.readline().strip()


def convert_to_bitstream(data):
    return BitArray(bytes=data).bin


"""
Return difference in bits
"""
def check(a, b, user_times): # user_times is ignored
    # print('[DEBUG] a is %s, b is %s' % (a, b))
    bs_a = convert_to_bitstream(a) # string of bits
    bs_b = convert_to_bitstream(b) # string of bits
    bs_a = bs_a.ljust(len(bs_b), "0") # justify to be of the same length
    bs_b = bs_b.ljust(len(bs_a), "0") # justify to be of the same length
    counter = 0
    # pdb.set_trace()
    for i in range(len(bs_a)):
        if bs_a[i] != bs_b[i]:
            # print('[DEBUG] counter is %d' % counter)
            return counter
        counter += 1
    # print('[DEBUG] counter is %d' % counter)
    return counter


def main(password=None, times=None):
    # signal.alarm(4)

    secret_key = flag
    # write(open(__file__).read())
    if not password:
        write("Password: ", endl="")
        user_supplied = readline()
    else:
        user_supplied = password

    if not times:
        write("How many times do you want to test: ", endl="")
        user_times_supplied = readline()
    else:
        user_times_supplied = times

    # print('[DEBUG] user_supplied is %s of type %s, user_times_supplied is %s of type %s' % (user_supplied, type(user_supplied), user_times_supplied, type(user_times_supplied)))

    try:
        int(user_supplied, 16)
        user_data = user_supplied.decode("hex")
        user_times = int(user_times_supplied)
    except Exception as e:
        print('[DBEUG] exception is %s' % e)
        write("Evil.")
        return

    # print('[DEBUG] user_data is %s of type %s, user_times is %s of type %s' % (user_data, type(user_data), user_times, type(user_times)))

    if user_times > 5000:
        write("Too many times.")
        return

    # print('[DEBUG] processing password %s for %d times' % (user_data, user_times))

    result = len(flag) * 8 * user_times
    start = time.time()
    for i in range(user_times):
        tmp = check(user_data, secret_key, user_times)
        result -= tmp
    # print('[DEBUG] deducting %d' % tmp)
    end = time.time()
    elapsed = end - start

    if result == 0: # this only happens when the guess is correct
        write("Flag is %s" % flag)
    else:
        write("Impossible.")

    write("Request completed in: %.4fs (%d)" % (elapsed, result))

    return (elapsed, result)

if __name__ == "__main__":
    main()
