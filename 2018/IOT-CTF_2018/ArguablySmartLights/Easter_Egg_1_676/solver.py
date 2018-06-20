import binascii

FILENAME = 'easter_egg'

light = True
with open(FILENAME) as f:
    bits = ''
    for line in f:
        if len(line.rstrip()) > 2:
            continue
        if line[1] == 'L':
            if light:
                light = False
            else:
                print('[DEBUG] error!')
            for i in range(int(line[0])):
                bits += '1'
        else:
            if not light:
                light = True
            else:
                print('[DEBUG] error!')
            for i in range(int(line[0])):
                bits += '0'

### Truncate

bits = bits[0:len(bits)//8*8] # round down to multiple of 8

### Convert bit string to ascii

n = int('0b' + bits, 2)
msg = binascii.unhexlify('%x' % n)

print('>> msg is:\n%s' % msg)
