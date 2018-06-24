#!/usr/bin/env python

import sys
flag = 'flag'
from bitstring import BitArray
import time
import signal


def write(data, endl='\n'):
    sys.stdout.write(data + endl)
    sys.stdout.flush()


def readline():
    return sys.stdin.readline().strip()


def convert_to_bitstream(data):
    return BitArray(bytes=data).bin


def check(a, b, user_times):
    bs_a = convert_to_bitstream(a)
    bs_b = convert_to_bitstream(b)
    bs_a = bs_a.ljust(len(bs_b), "0")
    bs_b = bs_b.ljust(len(bs_a), "0")
    counter = 0
    for i in range(len(bs_a)):
        if bs_a[i] != bs_b[i]:
            return counter
        counter += 1
    return counter


def main():
    # signal.alarm(4)

    secret_key = flag
    write(open(__file__).read())
    write("Password: ", endl="")
    user_supplied = readline()
    write("How many times do you want to test: ", endl="")
    user_times_supplied = readline()

    print('[DEBUG] user_supplied is %s of type %s, user_times_supplied is %s of type %s' % (user_supplied, type(user_supplied), user_times_supplied, type(user_times_supplied)))

    try:
        int(user_supplied, 16)
        user_data = user_supplied.decode("hex")
        user_times = int(user_times_supplied)
    except Exception:
        write("Evil.")
        return

    if user_times > 5000:
        write("Too many times.")
        return

    result = len(flag) * 8 * user_times
    start = time.time()
    for i in range(user_times):
        result -= check(user_data, secret_key, user_times)
    end = time.time()
    elapsed = end - start

    if result == 0:
        write("Flag is %s" % flag)
    else:
        write("Impossible.")

    write("Request completed in: %.4fs (%d)" % (elapsed, result))


if __name__ == "__main__":
    main()
