from pwn import *
import binascii

HOST = 'ctf.pwn.sg'
PORT = 4003

def probe(password, times, noisy = False):

    conn = remote(HOST, PORT, typ='tcp')

    # Receive data
    data = conn.recvuntil('Password: ')
    data = conn.recvuntil('Password: ')

    # Send data
    message = password
    if noisy:
        print('sending %s' % message)
    conn.sendline(message)

    data = conn.recvuntil('How many times do you want to test: ')
    if noisy:
        print('received:\n{!r}'.format(data))

    # Send data
    message = times
    if noisy:
        print('sending %s' % message)
    conn.sendline(message)

    # receive data
    data = conn.recvline()
    if noisy:
        print('received {!r}'.format(data))

    # receive data
    data = conn.recvline()
    if noisy:
        print('received {!r}'.format(data))

    result = int(data.split('(')[-1].split(')')[0])

    if noisy:
        print('>> result is %d' % result)

    conn.close()

    return result

if __name__ == '__main__':

    # probe('4321', 1, noisy = True)

    length = 38
    times = 1
    password = ''
    result_thres = length * 8
    for l in range(length):
        for c in string.printable:
            password_tmp = password + '{0:0{1}X}'.format(ord(c),2)
            print('>> trying ord %s (%s)' % (ord(c), password_tmp))
            result = probe(password_tmp, str(times))
            print('>> result = %d' % (result))
            if result <= result_thres - 8:
                print('>> found one char: %s' % c)
                password = password_tmp
                result_thres -= 8
                print('>> SOLVED: password is %s' % password)
                print('>> In plaintext, %s' % binascii.unhexlify(password))
                break

