import fitblips
import binascii
import string

length = 12
times = 1
password = ''
result_thres = length * 8
for l in range(length):
    for c in string.printable:
        password_tmp = password + '{0:0{1}X}'.format(ord(c),2)
        print('>> trying ord %s (%s)' % (ord(c), password_tmp))
        (elapsed, result) = fitblips.main(password_tmp, str(times))
        print('>> elapsed = %f, result = %d' % (elapsed, result))
        if result <= result_thres - 8:
            print('>> found one char: %s' % c)
            password = password_tmp
            result_thres -= 8
            print('>> SOLVED: password is %s' % password)
            print('>> In plaintext, %s' % binascii.unhexlify(password))
            break

