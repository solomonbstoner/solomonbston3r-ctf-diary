from pwn import *

f = open('flag_page','w')

flag = "CrossCTF{Hi}".strip()
content = ""

for c in flag:
    content += c * 31
    content += "\x00"

f.write(content)
