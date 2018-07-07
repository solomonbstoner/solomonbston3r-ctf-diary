from scapy.all import rdpcap
from Crypto.Cipher import Blowfish # https://www.dlitz.net/software/pycrypto/api/current/Crypto.Cipher.Blowfish-module.html
import binascii
import string
import pdb

FILENAME = 'agent_comm.pcap'

### Parse pcap file and extract paylaods

pkts = rdpcap(FILENAME)

Mobile_IP_payloads = []
for pkt in pkts:
    UDP = pkt['UDP']
    Mobile_IP_payloads.append(bytes(UDP[1]))

### Brute-force decrypt payloads using blowfish

def I2OSP(longint):
    def hex2(n):
        x = '%x' % (n,)
        return ('0' * (len(x) % 2)) + x
    return binascii.unhexlify(hex2(longint))

def is_printable(s):
    for c in s:
        if chr(c) not in string.printable:
            return False
    return True

KEY_LEN_BYTES = 2 # from hint given

ciphertext = b''
for p in Mobile_IP_payloads:
    ciphertext += p

for i in range(0,(2**8)**KEY_LEN_BYTES):
    key = I2OSP(i)
    assert len(key) <= KEY_LEN_BYTES
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    msg = cipher.decrypt(ciphertext)
    if b'sctf' in msg:
        print('>> found key: %s' % key)
        print('>> decrypted to: %s' % msg)
        break
